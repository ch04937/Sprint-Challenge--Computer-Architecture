import sys

# instruction definition
HLT = 0b00000001  # HALT: STOP
LDI = 0b10000010  # LDI: PRINT IMMEDIATE NUMBER
CMP = 0b10100111  # CMP: This is an instruction handled by the ALU
JMP = 0b01010100  # JEQ : JUMP TO THE ADDRESS STORED IN THE GIVEN REGISTER
JEQ = 0b01010101  # JEQ : JUMP TO GIVEN REGISTER
JNE = 0b01010110  # JEQ : JUMP TO GIVEN REGISTER
PRN = 0b01000111  # PRN: PRINT NUMERIC VALUE STORED


class CPU:
    def __init__(self):
        self.ram = [0] * 100  # memory
        self.reg = [0]*8  # list of registers
        self.pc = 0  # program counter
        self.sp = 7  # stack pointer
        self.flags = {}
        # branch set up
        self.branch = {}
        self.branch[HLT] = self.HLT
        self.branch[LDI] = self.LDI
        self.branch[CMP] = self.CMP
        self.branch[JEQ] = self.JEQ
        self.branch[JMP] = self.JMP
        self.branch[JNE] = self.JNE
        self.branch[PRN] = self.PRN

    def PRN(self):
        # print numeric value stored in the given register
        address = self.ram[self.pc + 1]
        print(f'reg[0]: {self.reg[address]}')
        self.pc += 2

    def JMP(self):
        '''
        Jump to the address stored in the given register.

        Set the PC to the address stored in the given register.
        '''
        address = self.ram[self.pc+1]

        self.pc = self.reg[address]

    def JNE(self):
        '''
        If E flag is clear (false, 0), jump to the address stored in the given register.        
        '''
        address = self.ram[self.pc + 1]
        if self.flags['E'] == 0:
            self.pc = self.reg[address]

        else:
            self.pc += 2

    def JEQ(self):
        '''
        If equal flag is set true, jump to the address stored in the given register
        '''
        address = self.ram[self.pc + 1]

        if self.flags['E'] == 1:
            self.pc = self.reg[address]
        else:
            self.pc += 2

    def CMP(self):
        '''
        Compare the values in two registers
        '''
        self.alu('cmp', self.reg[0], self.reg[1])

        self.pc += 3

    def alu(self, operation, reg_a, reg_b):
        '''
        ALU operations
        '''
        if operation == 'cmp':
            if reg_a == reg_b:
                # set the Equal flag to 1
                self.flags['E'] = 1
            else:
                # else set to 0
                self.flags['E'] = 0
            if reg_a < reg_b:
                # set lessthan flag to 1
                self.flags['L'] = 1
            else:
                # else set to 0
                self.flags['L'] = 0
            if reg_a > reg_b:
                # set set greater than G flag to 1
                self.flags['G'] = 1
            else:
                self.flags['G'] = 0
                # else set to 0

        else:
            raise Exception('unsupported alu operation')

    def LDI(self):
        '''
        Set the value of a register to an integer
        '''
        # assign variables
        register = self.ram[self.pc+1]
        num = self.ram[self.pc+2]

        # set value of register
        self.reg[register] = num

        self.pc += 3

    def HLT(self):
        print('reg: ', c.reg)
        print('memory: ', c.ram)
        print('bye, bye')
        sys.exit(0)

    def load(self, filename):
        """Load a program into memory."""
        try:
            # Open the file
            with open(filename) as f:
                # Read all the lines
                address = 0
                for line in f:
                    # Parse out comments
                    comment_split = line.strip().split("#")
                    # Cast the numbers from strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == '':
                        continue
                    instruction = int(value, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('File not found')
            sys.exit(2)

    def run(self):
        '''
        Run the program
        '''
        print(self.ram)
        while True:

            command = self.ram[self.pc]

            if command in self.branch:
                self.branch[command]()
            else:
                print(f'command not in branch {command}')
                self.pc += 2


if len(sys.argv) != 2:
    print('ERROR: Must have file name')
    sys.exit(1)


c = CPU()
c.load(sys.argv[1])
c.run()
