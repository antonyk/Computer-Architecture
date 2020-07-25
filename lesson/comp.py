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

SP = 7
register[SP] = 0xF4 # init R7 with stack pointer

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


  elif instruction == 5:  # PUSH
    # decrement stack ptr
    register[SP] -= 1
    register[SP] &= 0xff  # protect against out of bounds; cause a wrap around

    # get register value
    reg_num = memory[pc+1]
    value = register[reg_num]

    # store in mem
    address_to_push_to = register[SP]
    memory[address_to_push_to] = value

    pc += 2

  elif instruction == 6:
    # pop
    pass


  elif instruction == CALL:
    # get address of next instruction
    return_addr = pc + 2

    # push that on the stack
    register[SP] -= 1
    address_to_push_to = register[SP]
    memory[address_to_push_to] = return_addr

    # set the pc to that subroutine address
    reg_num = memory[pc + 1]
    subroutine_addr = register[reg_num]

    pc = subroutine_addr

  elif instruction == RET:
    address_to_pop_from = register[SP]
    return_addr = memory[address_to_pop_from]
    register[SP] += 1

    pc = return_addr


  else:
    print(f"Unknown instruction: {instruction}")

  
# print(register)
# print(memory)


