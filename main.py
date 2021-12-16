import argparse
import repl
from pypol.interpreter import Interpreter

parser = argparse.ArgumentParser(description='PyPOL APOL interpreter by Ginger Industries 2021')
parser.add_argument('file', default="", type=str, nargs="?", help='A path to a file to load')
a = parser.parse_args()
name = a.file
if name:
  try:
    kc = open(name)
  except FileNotFoundError:
    print("No such file:", name)
  except OSError as e:
    print("Error loading file \"", name, "\":", str(e))
  program = kc.read()
  kc.close()
  repl.run(program, Interpreter(), False, True)
  
else:
  repl.repl()