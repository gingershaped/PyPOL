from .instructions import *
import sys

conversionTable = {
  "p": PrintInstruction,
  "i": InputInstruction,

  "+": AdditionInstruction,
  "-": SubtractionInstruction,
  "*": MultiplicationInstruction,
  "x": MultiplicationInstruction,
  "/": DivisionInstruction,
  "^": ExponentInstruction,
  "%": ModuloInstruction,
  "∸": FloorDivisionInstruction,

  "v": MemoryWriteInstruction,

  "I": CastToNumberInstruction,
  "⌬": ReverseInstruction,
  "l": StringLengthInstruction,
  "⌕": StringFindInstruction,
  "s": StringSplitInstruction,

  "a": ListAppendInstruction,
  "⊕": ListSumInstruction,

  "w": WhileLoopInstruction,
  "f": ForLoopInstruction,
  "∈": ForCounterInstruction,
  "∋": ForItemInstruction,
  "?": IfInstruction,
  ":": FunctionInstruction,
  "⍭": DelayInstruction,

  "<": LessThanComparison,
  ">": GreaterThanComparison,
  "≤": LessThanOrEqualToComparison,
  "≥": GreaterThanOrEqualToComparison,
  "=": EqualComparison,
  "≠": UnequalComparison,
  "≬": BetweenInstruction,


  "∆": IncreaseInstruction,
  "∇": DecreaseInstruction,
  #"±": SetSignInstruction,
  "≐": GetEvenInstruction,
  "∓": GetSignInstruction,
  "⌿": AbsoluteValueInstruction,
  "∿": RandomNumberInstruction,
  "≀": RandomFloatInstruction,
  "≖": RoundInstruction,
}

altNames = {
  "print": "p",
  "input": "i",
  "add": "+",
  "subtract": "-",
  "multiply": "*",
  "divide": "/",
  "exponent": "^",
  "modulo": "%",
  "floordiv": "∸",
  "write": "v",
  "castnumber": "I",
  "reverse": "⌬",
  "length": "l",
  "stringfind": "⌕",
  "stringsplit": "s",
  "while": "w",
  "forcounter": "∈",
  "foritem": "∋",
  "for": "f",
  "delay": "⍭",
  "lessthan": "<",
  "greaterthan": ">",
  "lessorequal": "≤",
  "greaterorequal": "≥",
  "unequal": "≠",
  "equal": "=",
  "between": "≬",
  "increase": "∆",
  "decrease": "∇",
  "geteven": "≐",
  "getsign": "∓",
  "abs": "⌿",
  "append": "a",
  "listsum": "⊕",
  "if": "?",
  "function": ":",
  "randnum": "∿",
  "randfloat": "≀",
  "round": "≖",
}

class Interpreter():
  @classmethod
  def prepare(self, program):
    program = program.replace("\n", ";")
    for altName in altNames:
      program = program.replace(altName, altNames[altName])
    return program.split(";")
  def __init__(self):
    self.memory = {}
    self.lastError = None
    self._forLoopCounter = None
    self._forLoopItem = None
  
  def interpret(self, program):
    instructions = []
    def parseInstruction(instruction):
      if instruction[0] in CONSTANTS:
        return ConstantInstruction(CONSTANTS[instruction[0]])
      try:
        t = conversionTable[instruction[0]]
      except KeyError:
        raise SyntaxError("Invalid instruction: " + instruction[0])
      argStr = instruction[1:].split("(", 1)[-1]
      if not len(argStr):
        return t(self)
      args = []
      i = ""
      l = []
      ignore = 0
      inString = False
      inList = False
      class String():
        def __init__(self, r):
          self.r = r
        
      for c, char in enumerate(argStr):
        if (char == '"' or char == "'") and argStr[c-1] != "\\" and ignore == 0:
          inString = not inString
          continue
        if char == "(" and argStr[c-1] != "\\":
          ignore += 1
        elif char == ")" and argStr[c-1] != "\\":
          ignore -= 1
        if ((char == " " and ignore == 0) or (c == len(argStr)-1)) and (not inString):
          if argStr[c-1] == "'" or argStr[c-1] == '"':
            if inList:
              if i.lstrip() != "":
                l.append(i.lstrip())
            else:
              args.append(String(i.lstrip()))
          else:
            if inList:
              try:
                l.append(float(i.lstrip()))
              except ValueError:
                if i.lstrip() != "":
                  l.append(i.lstrip())
            else:
              args.append(i.lstrip())
          i = ""
        if char == "[" and argStr[c-1] != "\\":
          inList = True
          continue
        elif char == "]" and argStr[c-1] != "\\":
          inList = False
          try:
            l.append(float(i.lstrip()))
          except ValueError:
            if i.lstrip() != "":
              l.append(i.lstrip())
          args.append(l)
          l = []
          i = ""
          continue
        if not (char == "\\" and argStr[c+1] in ["(", ")", "'", '"']):
          i += char
      args = [c for c in args if c != ""]
      if inList:
        raise SyntaxError("Unclosed list")
      if ignore > 0:
        raise SyntaxError("Unclosed parenthesis")
      if inString:
        raise SyntaxError("Unclosed string")
      parsedArgs = []
      for arg in [i for i in args if i != '']:
        if type(arg) == list:
          parsedArgs.append(arg)
        elif type(arg) == String:
          parsedArgs.append(arg.r.replace("\\n", "\n"))
        elif arg[0] in CONSTANTS:
          parsedArgs.append(ConstantInstruction(CONSTANTS[arg[0]]))
        elif arg[0] in conversionTable:
          parsedArgs.append(parseInstruction(arg))
        elif all([c in "-1234567890" for c in arg]):
          parsedArgs.append(float(arg))
        elif any(c in "⁰¹²³⁴⁵⁶⁷⁸⁹" for c in arg):
          try:
            parsedArgs.append(MemoryReadInstruction(self, int("".join([str("⁰¹²³⁴⁵⁶⁷⁸⁹".find(c)) for c in arg]))))
          except ValueError:
            raise ValueError("Error processing cell id: " + arg + " Make sure you're not using superscript numbers to refer to cells, or that you mistyped an instruction.") from None
        else:
          #It's a command I guess
          parsedArgs.append(arg)
      try:
        return t(self, *parsedArgs)
      except TypeError as e:
        raise TypeError(str(e) + " in instruction " + instruction) from None
    for instruction in program:
      instructions.append(parseInstruction(instruction))
    return instructions
  
  def run(self, program, implicitPrint = True):
    _ = None
    try:
      instructions = self.interpret(self.prepare(program))
      for instruction in instructions:
        _ = instruction.execute()
    except:
      self.lastError = sys.exc_info()
      raise
    if implicitPrint and _ != None:
      print(_)
    return _
  def restart(self):
    self.memory = {}