#!/usr/bin/env python3
"""Main."""
"""
command line arguments:
- program file
- program code's number base
- 
"""
import sys
from cpu import *

cliargs = {}
# commands = 

if len(sys.argv) > 1:
  for i in range(1,len(sys.argv)):
    cliarg = sys.argv[i]

    res = cliarg.split('=', 1)

    # parse out the leading dashes ('-' or '--')
    if res[0].startswith('-'):
      pass
    if res[0].startswith('--'):
      pass

    if len(res) == 2:
      # has value
      cliargs[res[0]] = res[1]
    elif len(res) == 1:
      cliargs[res[0]] = 1
    else:
      pass # skip invalid ones


print("CLI ARGS:", cliargs)

cpu = CPU()


filename = cliargs.get('file', None)
base = cliargs.get('base', 2)  # default base to 2

if filename:
  try:
    memory = [0] * 256
    address = 0

    with open(filename) as f:
      for line in f:
        line = line.strip()
        line = line.split("#", 1)[0]
        print(repr(line))
        if address < len(memory):
          try:
            line = int(line, base) # take the base as an input
            memory[address] = line
            address += 1
          except ValueError:
            pass
        else:
          print("MEMORY OVERFLOW. Stopping Load")
          break

    print(memory)
    # sys.exit(0)
    cpu.load(memory)

  except FileNotFoundError:
    print(f"Couldn't find file {filename}")
    sys.exit(1)

else:
  cpu.load()


cpu.run()


