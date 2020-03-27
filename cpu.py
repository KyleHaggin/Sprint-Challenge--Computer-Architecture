"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [None] * 256

        self.register = [0]*8

        self.sp = 7

        self.pc = 0
        pass

    def load(self, filepath):
        """Load a program into memory."""

        address = 0

        # Try/Except file loader
        try:
            with open(filepath, 'r') as f:

                # Create program
                program = f.read().splitlines()
                program = [
                    '0b'+line[:8]
                    for line in program
                    if line and line[0] in ['0', '1']
                    ]

                # Load program to ram
                for instruction in program:
                    self.ram[address] = eval(instruction)
                    address += 1

        except FileNotFoundError:
            print('File not found')
            sys.exit(2)

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]

        elif op == 'MULT':
            self.register[reg_a] *= self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.self.pc),
            self.ram_read(self.self.pc + 1),
            self.ram_read(self.self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running is True:

            # Breakout condition
            if self.ram[self.pc] is 0b00000001:
                # Increment self.pc by 1
                self.pc += 1

                # Breakout condition
                running = False

            # Resister Print
            elif self.ram[self.pc] is 0b01000111:
                # Increment self.pc by 1
                self.pc += 1

                # Set register index
                reg = self.ram[self.pc]
                # Print the register
                print(self.register[reg])
                # Increment self.pc by 1
                self.pc += 1

            # Register Print
            elif self.ram[self.pc] is 0b10000010:
                # Increment self.pc by 1
                self.pc += 1

                # Set register index
                reg = self.ram[self.pc]
                # increment self.pc by 1
                self.pc += 1

                # Save value to register
                self.register[reg] = self.ram[self.pc]
                # Increment self.pc by 1
                self.pc += 1

            # Register multiply
            elif self.ram[self.pc] is 0b10100000:
                self.pc += 1

                # Save index of register 1
                reg_1 = self.ram[self.pc]
                # Increment self.pc by 1
                self.pc += 1

                # Save index of register 2
                reg_2 = self.ram[self.pc]
                # Increment self.pc by 1
                self.pc += 1

                # Run alu multiply
                self.alu('ADD', reg_1, reg_2)

            # Register multiply
            elif self.ram[self.pc] is 0b10100010:
                # Increment self.pc by 1
                self.pc += 1

                # Save index of register 1
                reg_1 = self.ram[self.pc]
                # Increment self.pc by 1
                self.pc += 1

                # Save index of register 2
                reg_2 = self.ram[self.pc]
                # Increment self.pc by 1
                self.pc += 1

                # Run alu multiply
                self.alu('MULT', reg_1, reg_2)

            # Stack Push
            elif self.ram[self.pc] is 0b01000101:
                # Increment self.pc by 1
                self.pc += 1

                # Save value of register at value in self.pc
                val = self.register[self.ram[self.pc]]
                # Decrement the SP
                self.register[self.sp] -= 1
                # Copy value in the register to the address pointed to by SP
                self.ram[self.register[self.sp]] = val
                # Increment self.pc by 1
                self.pc += 1

            # Stack Pop
            elif self.ram[self.pc] is 0b01000110:
                # Increment self.pc by 1
                self.pc += 1

                # Save the value of the memory to the register
                val = self.ram[self.register[self.sp]]
                # Copy the value from the address pointed
                # to by sp to the register
                self.register[self.ram[self.pc]] = val
                # Increment SP
                self.register[self.sp] += 1
                # Increment self.pc by 1
                self.pc += 1

            # Call
            elif self.ram[self.pc] is 0b01010000:
                # Increment self.pc by 2
                self.pc += 2

                # Address of instruction after call pushed onto Stack
                self.register[self.sp] -= 1
                self.ram[self.register[self.sp]] = self.pc

                # Decrement pc by 1
                self.pc -= 1
                self.pc = self.register[self.ram[self.pc]]

            # Ret
            elif self.ram[self.pc] is 0b00010001:
                self.pc = self.ram[self.register[self.sp]]
                self.register[self.sp] += 1

            else:
                print(
                    f'Unknown instruction: {self.ram[self.pc]}, '
                    f'{bin(self.ram[self.pc])}'
                    )
                sys.exit(1)
        pass
