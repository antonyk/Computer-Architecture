"""
CPU functionality.

"""

import sys
# import ops
from ops import *
# from reg import *
# import reg
# from datetime import datetime
import datetime

# TIMER_INTERRUPT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        # Internal Registers
        self.pc     = 0b00000000
        self.ir     = opcodes['NOP']
        self.mar    = 0b00000000
        self.mdr    = 0b00000000
        self.fl     = 0b00000000  # 00000LGE - only last 3 bits matter
        # self.op1    = 0b00000000
        # self.op2    = 0b00000000

        # Interrupt Vector Table
        self.ivt = [0] * 8
        for i in range(len(self.ivt)):
            self.ivt[i] = 0xf8 + i

        # General Purpose Registers
        self.reg = [0] * 8  # this is the CPU's register
        self.reg[7] = 0xf4

        # Memory
        self.ram = [0] * 265 # size of the computer's memory

        # Instructions
        # max instruction space is 4 bits for each: alu and non-alu
        # *** LS8 doesn't support this structure ***
        # self.std = [0] * 16
        # self.alu = [0] * 16
        self.ops = [0] * 256

        self.iset = Instructions(self)
        # self.inst = [0] * 64 # max number of instructions, based on 6-bit binary
        for key in opcodes:
            self.ops[opcodes[key]] = getattr(self.iset, "handle_" + key, 0)

        # for key in opcodes:
        #     opcode = opcodes[key]
        #     instruction_type = opcode & 0b00100000
        #     idx = opcode & 0b00001111
        #     if instruction_type == 0:   # STD
        #         self.std[idx] = getattr(self.iset, key.lower(), 0)
        #         print("STD:",key, self.std[idx])
        #     else:                       # ALU
        #         self.alu[idx] = getattr(self.iset, key.lower(), 0)
        #         # print("ALU:", key, self.alu[idx])

        # print("STD:", self.std)
        # # print("ALU:", self.alu)
        # print("HLD:", self.std[1])

        self.allow_interrupts = True


    def load(self, program = None, second="Hello"):
        """Load a program into memory."""

        # print(second)

        if program == None:
            # Use hardcoded program:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

        address = 0
        for instruction in program:
            self.ram[address] = instruction
            address += 1

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

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

    def push_state_to_stack(self):
        # push PC to stack
        self.SP -= 1
        self.ram_write(self.SP, self.pc)

        # push FL to stack
        self.SP -= 1
        self.ram_write(self.SP, self.fl)

        # push R0-R6 to stack in this order
        for i in range(7):
            self.SP -= 1
            self.ram_write(self.SP, self.reg[i])

    def pop_state_from_stack(self):
        # pop R6-R0 from stack in this order
        for i in range(7):
            self.reg[6-i] = self.ram_read(self.SP)
            self.SP += 1

        # pop FL from stack
        self.fl = self.ram_read(self.SP)
        self.SP += 1

        # pop PC from stack
        self.pc = self.ram_read(self.SP)
        self.SP += 1

    def run(self):
        # running = True  # maybe use break to halt??
        start_time = datetime.datetime.now()
        while True:
            # set Timer Interrupt's value (is it ON/OFF?)
            if (datetime.datetime.now() - start_time).total_seconds() > 1:
                self.IS = self.IS | 0b00000001  # ensure the ZERO bit is True

            if self.allow_interrupts:
                maskedInterrupts = self.IS & self.IM
                # get requested interrupts
                if maskedInterrupts:
                    for i in range(8):
                        if ((maskedInterrupts >>  i) & 0b00000001):
                            # disable further interrupts
                            self.allow_interrupts = False
                            # clear current interrupt (IS) bit
                            self.IS = self.IS & (~(0b00000001 << i))
                            # special case for timer reset
                            if i == 0:
                                start_time = datetime.datetime.now()
                            # push current state onto the stack
                            self.push_state_to_stack()
                            # set the PC with the address in the interrupt vector
                            self.pc = self.ram_read(self.ivt[i])


            # self.trace("Loop Start")
            self.ir = self.ram_read(self.pc)
            # self.reg[2] = self.ram_read(self.pc+1)
            # self.reg[3] = self.ram_read(self.pc+2)
            
            # increment pc after reach of its reads, thus moving the machine's head
            # print(f"PRE: {self.ir} (self.ir), {LDI} (LDI)")

            # self.trace("If Start")

            # build the arguments array based on the top 2 bits
            args = []
            for i in range((self.ir >> 6)):
                args.append(self.ram_read(self.pc+1+i))

            # call the standard instruction passing it the args array
            # possibly shorten mask to 0b1111 as leading zeros are irrelevant
            if self.ops[self.ir]:
                self.ops[self.ir](*args)

            # come here if instruction not found / not defined
            else:
                # print(self.ir)
                # print(self.std)
                print("Unknown opcode:", self.ir)
                print("pc:", self.pc)
                break

            # increment the program counter (PC):
            # 1. IF 5th bit is 1 (determines if instruction itself sets the PC)
            # 2. based on the size of the args array
            if (self.ir & 0b00010000) == 0:  # 5th bit is 1 if instruction sets the PC
                self.pc = (self.pc + ((self.ir  >> 6) + 1)) & 0b11111111


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


    @property
    def SP(self):
        return self.reg[7]
    @SP.setter
    def SP(self, value):
        self.reg[7] = (value) & 0xff

    @property
    def IS(self):
        return self.reg[6]
    @IS.setter
    def IS(self, value):
        self.reg[6] = (value) & 0xff

    @property
    def IM(self):
        return self.reg[5]
    @IM.setter
    def IM(self, value):
        self.reg[5] = (value) & 0xff



if __name__ == "__main__":
    cpu = CPU()
    print(len(cpu.ram))


    cpu.ram_write()
    print(cpu.ram[3])
