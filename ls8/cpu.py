"""
1. Register Table
"""
PC_IDX      = 0
IR_IDX      = 1
MAR_IDX     = 2
MDR_IDX     = 3
FL_IDX      = 4
IM_IDX      = 5
IS_IDX      = 6
SP_IDX      = 7

"""
2. Instructions Table
"""
HLT         = 0b00000001

# pending
LDI         = 0b00000001
PRN         = 0b00000001
# HLT         = 0b00000001


def create_8bit_register():
  return [0] * 8


"""
CPU functionality.


"""

import sys
# from reg import *
# import reg


class CPU:
    """Main CPU class."""

    def __init__(self):
        # Registers
        self.reg = [0] * 8  # this is the CPU's register
        # self.reg[MAR_IDX]


        self.ram = [0] * 0b11111111
        self.reg = [0] * 8
        self.pc = 0

    def get_MAR(self):
        return cpu.reg[MAR_IDX]

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        PC = self.reg[PC_IDX]
        IR = PC
        self.reg[IR_IDX] = IR

        instruction = self.ram_read(PC)
        operand_a = self.ram_read(PC+1)
        operand_b = self.ram_read(PC+2)

        running = True
        while running:

            if instruction == HLT:
                print("exiting...")
                running = False

            elif instruction == 1:
                pass

            else:
                print("Unknown opcode")




    def ram_read(self, address = None):
        if not address:
            address = self.reg[MAR_IDX]

        return self.ram[address]

    def ram_write(self, address = None, value = None):
        if not address:
            address = self.reg[MAR_IDX]
        if not value:
            value = self.reg[MDR_IDX]

        self.ram[address] = value


if __name__ == "__main__":
    cpu = CPU()
    print(len(cpu.ram))

    # test
    # self.MAR = self.reg[3]
    # self.MDR = self.reg[4]

    cpu.ram_write()
    print(cpu.ram[3])

