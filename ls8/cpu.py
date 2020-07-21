"""
CPU functionality.

"""

import sys
# import ops
from ops import *
# from reg import *
# import reg


class CPU:
    """Main CPU class."""

    def __init__(self):
        # Internal Registers
        self.pc     = 0b00000000
        self.ir     = NOP
        self.mar    = 0b00000000
        self.mdr    = 0b00000000
        self.fl     = 0b00000000  # 00000LGE - only last 3 bits matter

        # General Purpose Registers
        self.reg = [0] * 8  # this is the CPU's register

        # Memory
        self.ram = [0] * 265 # size of the computer's memory


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

    def trace(self, location="not set"):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"[TRACE] (INT) PC: %02X, IR: %02X | RAM: %02X %02X %02X %02X | REG:" % (
            self.pc,
            self.ir,
            # self.mar,
            # self.mdr,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2),
            self.ram_read(self.pc + 3),
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        # running = True  # maybe use break to halt??
        while True:
            # self.trace("Loop Start")
            self.ir = self.ram_read(self.pc)
            # self.reg[2] = self.ram_read(self.pc+1)
            # self.reg[3] = self.ram_read(self.pc+2)
            
            # increment pc after reach of its reads, thus moving the machine's head
            # print(f"PRE: {self.ir} (self.ir), {LDI} (LDI)")
            self.trace("If Start")

            if self.ir == HLT:
                print("HALT called! Exiting...")
                break

            elif self.ir == LDI:
                # not ideal; should only be read into general purpose registers if needed
                # do the ram reading here ??
                self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)

            elif self.ir == PRN:
                print(self.reg[self.ram_read(self.pc+1)])

            elif self.ir == NOP:
                print("NOP Encountered. Exiting...")
                break

            else:
                print("Unknown opcode")
                break

            self.pc += ((self.ir & 0b11000000) >> 6) + 1


    def ram_read(self, address = None):
        if address is not None:
            self.mar = address

        self.mdr = self.ram[self.mar]
        return self.mdr

    def ram_write(self, address = None, value = None):
        if address is not None:
            self.mar = address
        if value is not None:
            self.mdr = value

        self.ram[self.mar] = self.mdr


if __name__ == "__main__":
    cpu = CPU()
    print(len(cpu.ram))

    # test
    # self.MAR = self.reg[3]
    # self.MDR = self.reg[4]

    cpu.ram_write()
    print(cpu.ram[3])

