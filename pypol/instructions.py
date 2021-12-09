import time, math, string, random

CONSTANTS = {
  "↹": "PyPOL APOL interpreter v0.1.0 by Ginger Industries 2021",
  "T": True, 
  "F": False, 
  "ĥ": "Hello, World!", 
  "ó": 1000000,
  "ò": 1000000000,
  "π": math.pi,
  "ε": math.e,
  "Ⓠ": "qwertyuiop",
  "⒬": list("qwertyuiop"),
  "Ⓐ": string.ascii_letters,
  "⒜": list(string.ascii_letters),
  "①": "".join([str(_) for _ in list(range(10))]),
  "⑴": list(range(10)),
  "⑩": list(range(1, 100)),
  "⑽": "".join([str(_) for _ in list(range(1, 100))]),
  "⑨": list(range(100)),
  "⑼": "".join([str(_) for _ in list(range(100))]),
  "⒈": 16,
  "⒉": 32,
  "⒊": 64,
  "⒋": 128,
  "⒌": 256,
  "⒍": 512,
  "⒎": 1024,
  "⒏": 2048,
  "⒐": 4096,
  "⒑": 8192,
  "⒒": 16384,
  "⒓": 32768,
  "⒔": 65536,
  "⒕": 2147483648,
  "⒖": 4294967296
}



class Instruction():
  def __init__(self, interpreter):
    pass
class ConstantInstruction(Instruction):
  def __init__(self, constant):
    self.constant = constant
  def execute(self):
    return self.constant

class PrintInstruction(Instruction):
  def __init__(self, interpreter, output, end="\n"):
    self.output = output
    self.end = end
  def execute(self):
    o = None
    try:
      o = self.output.execute()
    except AttributeError:
      o = self.output
    try:
      e = self.end.execute()
    except AttributeError:
      e = self.end
    print(o, end=e)
class StringSplitInstruction(Instruction):
  def __init__(self, interpreter, string, sep=" "):
    self.string = string
    self.sep = sep
  def execute(self):
    o = None
    try:
      o = self.string.execute()
    except AttributeError:
      o = self.string
    try:
      e = self.sep.execute()
    except AttributeError:
      e = self.sep
    return o.split(e)
class InputInstruction(Instruction):
  def __init__(self, interpreter, prompt=""):
    self.prompt = prompt
  def execute(self):
    try:
      prompt = self.prompt.execute()
    except AttributeError:
      prompt = self.prompt
    return input(prompt)

class AdditionInstruction(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 + n2
class SubtractionInstruction(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 - n2
class MultiplicationInstruction(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    if type(n1) == float or type(n1) == int:
      return n1 * n2
    else:
      return n1 * int(n2)
class DivisionInstruction(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 / n2
class FloorDivisionInstruction(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 // n2
class ModuloInstruction(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 % n2
class ExponentInstruction(Instruction):
  def __init__(self, interpreter, n1, n2=2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 ** n2

class ListAppendInstruction(Instruction):
  def __init__(self, interpreter, address, data):
    self.address = address
    self.data = data
    self.interpreter = interpreter
  def execute(self):
    try:
      address = self.address.execute()
    except AttributeError:
      address = self.address
    try:
      data = self.data.execute()
    except AttributeError:
      data = self.data
    if type(self.interpreter.memory.get(address)) == list:
      self.interpreter.memory.get(address).append(data)
    else:
      raise ValueError("Value at cell index " + str(address) + " isn't a list!")
class ListSumInstruction(Instruction):
  def __init__(self, interpreter, data):
    self.data = data
    self.interpreter = interpreter
  def execute(self):
    try:
      data = self.data.execute()
    except AttributeError:
      data = self.data
    if type(data) == list:
      return sum(data)
    else:
      raise ValueError("Unable to interpret \'" + str(data) + "\' as list!")

class MemoryWriteInstruction(Instruction):
  def __init__(self, interpreter, address, data):
    self.address = address
    self.data = data
    self.interpreter = interpreter
  def execute(self):
    try:
      address = self.address.execute()
    except AttributeError:
      address = self.address
    try:
      data = self.data.execute()
    except AttributeError:
      data = self.data
    self.interpreter.memory[int(address)] = data
class MemoryReadInstruction(Instruction):
  # This class is not meant to be created directly, use the superscript numbers instead
  def __init__(self, interpreter, address):
    self.address = int(address)
    self.interpreter = interpreter
  def execute(self):
    return self.interpreter.memory.get(self.address)
class ReverseInstruction(Instruction):
  def __init__(self, interpreter, string):
    self.string = string
  def execute(self):
    try:
      s = self.string.execute()
    except AttributeError:
      s = self.string
    if type(s) == list:
      return list(reversed(s))
    return s[::-1]
class StringLengthInstruction(Instruction):
  def __init__(self, interpreter, string):
    self.string = string
  def execute(self):
    try:
      s = self.string.execute()
    except AttributeError:
      s = self.string
    return len(s)
class StringFindInstruction(Instruction):
  def __init__(self, interpreter, string, toFind):
    self.string = string
    self.toFind = toFind
  def execute(self):
    try:
      s = self.string.execute()
    except AttributeError:
      s = self.string
    try:
      f = self.toFind.execute()
    except AttributeError:
      f = self.toFind
    return s.find(f)



class CastToNumberInstruction(Instruction):
  def __init__(self, interpreter, value):
    self.value = value
  def execute(self):
    try:
      value = self.value.execute()
    except AttributeError:
      value = self.value
    try:
      return float(value)
    except ValueError:
      return None

class LessThanComparison(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 < n2
class GreaterThanComparison(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 > n2
class LessThanOrEqualToComparison(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 <= n2
class GreaterThanOrEqualToComparison(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 >= n2
class EqualComparison(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 == n2
class UnequalComparison(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return n1 != n2
class BetweenInstruction(Instruction):
  def __init__(self, interpreter, n1, n2, n3):
    self.n1 = n1
    self.n2 = n2
    self.n3 = n3
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    try:
      n3 = self.n3.execute()
    except AttributeError:
      n3 = self.n3
    return n1 < n2 < n3

class IncreaseInstruction(Instruction):
  def __init__(self, interpreter, address):
    self.interpreter = interpreter
    self.address = address
  def execute(self):
    try:
      a = self.address.execute()
    except AttributeError:
      a = self.address
    self.interpreter[a] += 1
class DecreaseInstruction(Instruction):
  def __init__(self, interpreter, address):
    self.interpreter = interpreter
    self.address = address
  def execute(self):
    try:
      a = self.address.execute()
    except AttributeError:
      a = self.address
    self.interpreter[a] -= 1
class GetSignInstruction(Instruction):
  def __init__(self, interpreter, n1):
    self.n1 = n1
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    return n1 >= 0
class GetEvenInstruction(Instruction):
  def __init__(self, interpreter, n1):
    self.n1 = n1
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    return not bool(n1 % 2)
class AbsoluteValueInstruction(Instruction):
  def __init__(self, interpreter, n1):
    self.n1 = n1
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    return abs(n1)
class RoundInstruction(Instruction):
  def __init__(self, interpreter, n):
    self.n = n
  def execute(self):
    try:
      n = self.n.execute()
    except AttributeError:
      n = self.n
    return round(n)
class RandomNumberInstruction(Instruction):
  def __init__(self, interpreter, n1, n2):
    self.n1 = n1
    self.n2 = n2
  def execute(self):
    try:
      n1 = self.n1.execute()
    except AttributeError:
      n1 = self.n1
    try:
      n2 = self.n2.execute()
    except AttributeError:
      n2 = self.n2
    return random.randint(n1, n2)
class RandomFloatInstruction(Instruction):
  def execute(self):
    return random.random()

class WhileLoopInstruction(Instruction):
  def __init__(self, interpreter, comparison, *args):
    self.interpreter = interpreter
    self.comparison = comparison
    self.instructions = args
  def execute(self):
    try:
      v = self.comparison.execute()
    except AttributeError:
      v = self.comparison
    while v:
      try:
        v = self.comparison.execute()
      except AttributeError:
        v = self.comparison
      for i in self.instructions:
        try:
          i.execute()
        except AttributeError:
          pass
class ForLoopInstruction(Instruction):
  def __init__(self, interpreter, iterations, *args):
    self.interpreter = interpreter
    self.iterations = iterations
    self.instructions = args
  def execute(self):
    try:
      i = self.iterations.execute()
    except AttributeError:
      i = self.iterations
    if type(i) == float or type(i) == int:
      i = range(int(i))

    for c, x in enumerate(i):
      self.interpreter._forLoopCounter = c
      self.interpreter._forLoopItem = x
      for l in self.instructions:
        try:
          l.execute()
        except AttributeError:
          pass
    self.interpreter._forLoopCounter = None
    self.interpreter._forLoopItem = None
class ForCounterInstruction(Instruction):
  def __init__(self, interpreter):
    self.interpreter = interpreter
  def execute(self):
    if self.interpreter._forLoopCounter != None:
      return self.interpreter._forLoopCounter
    else:
      raise ValueError("Cannot use this instruction outside of a for loop!")
class ForItemInstruction(Instruction):
  def __init__(self, interpreter):
    self.interpreter = interpreter
  def execute(self):
    if self.interpreter._forLoopItem != None:
      return self.interpreter._forLoopItem
    else:
      raise ValueError("Cannot use this instruction outside of a for loop!")
class FunctionInstruction(Instruction):
  def __init__(self, interpreter, *args):
    self.instructions = args
  def execute(self):
    for l in self.instructions:
      try:
        l.execute()
      except AttributeError:
        pass
class IfInstruction(Instruction):
  def __init__(self, interpreter, condition, true, false=None):
    self.condition = condition
    self.true = true
    self.false = false
  def execute(self):
    try:
      c = self.condition.execute()
    except AttributeError:
      c = self.condition
    if c == True:
      try:
        self.true.execute()
      except AttributeError:
        pass
    else:
      try:
        self.false.execute()
      except AttributeError:
        pass

class DelayInstruction(Instruction):
  def __init__(self, interpreter, duration=1):
    self.duration = duration
  def execute(self):
    try:
      d = self.duration.execute()
    except AttributeError:
      d = self.duration
    time.sleep(d)