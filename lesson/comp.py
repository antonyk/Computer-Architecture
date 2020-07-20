"""
CPU
  - executes instructions
  - gets them out of RAM
  - has registers (like variables)
      - fixed names: R0-R7 (registers 0 - 7)
      - fixed number of them
      - fixed size -- 8 bits

MEMORY (RAM)
  - a big array of bytes
  - each memory slot has an index, and a value stored at that index
  - that index into memory is also known as:
    - pointer
    - location
    - address


"""

register = [0] * 8

memory = [
  1,  # PRINT_BEEJ
  3,  # SAVE_REG (R2, 99) -- save value 99 in register 2
  2,  #  1st parameter of previous instruction(3): -> R2
  99, # 2nd parameter of previous instruction(3): -> 99
  4,  # PRINT_REG R2  -- prints register 2
  2,  # 1st parameter of previous instruction(4): -> R2
  2,  # HALT
]



pc = 0  # Program Counter, index into memory of the current instruction
        # AKA a pointer to the current instruction

running = True

while running:
  instruction = memory[pc]

  if instruction == 1:  # PRINT_BEEJ
    offset = 1
    print("Beej")

    pc += offset

  elif instruction == 2:  # HALT
    running = False

  elif instruction == 3:
    offset = 3 # how much to jump for the next instruction

    reg_num = memory[pc+1]
    value = memory[pc+2]
    register[reg_num] = value

    pc += offset

  elif instruction == 4:
    offset = 2 # how much to jump for the next instruction

    reg_num = memory[pc+1]
    print(register[reg_num])

    pc += offset

  else:
    print(f"Unknown instruction: {instruction}")

  
# print(register)
# print(memory)