import sys

# instruction definition
LDI = 0b10000010  # LDI: PRINT IMMEDIATE NUMBER
CMP = 0b10100111  # CMP: This is an instruction handled by the ALU
JMP = 0b01010100  # JEQ : JUMP TO THE ADDRESS STORED IN THE GIVEN REGISTER
JEQ = 0b01010101  # JEQ : JUMP TO GIVEN REGISTER
JNE = 0b01010110  # JEQ : JUMP TO GIVEN REGISTER
# flags
l_flag = 0b100
g_flag = 0b010
e_flag = 0b001


class CPU:
    def __init__(self):
        self.ram = [0] * 100  # memory
        self.reg = [0]*8  # list of registers
        self.pc = 0  # program counter
        self.sp = 7  # stack pointer
        # branch set up
        self.flags = 0b00000001
        self.branch = {}
        self.branch[LDI] = self.LDI
        self.branch[CMP] = self.CMP
        self.branch[JEQ] = self.JEQ
        self.branch[JMP] = self.JMP
        self.branch[JNE] = self.JNE

    def JMP(self):
        '''
        Jump to the address stored in the given register.

        Set the PC to the address stored in the given register.
        '''
        address = self.reg[self.pc+1]

        self.pc = address

        self.pc += 2

    def JNE(self):
        '''
        If E flag is clear (false, 0), jump to the address stored in the given register.        
        '''
        address = self.reg[self.pc + 1]

        if self.flags == 0:
            self.pc = address

        self.pc += 2

    def JEQ(self):
        '''
        If equal flag is set true, jump to the address stored in the given register
        '''
        if self.flags == e_flag:
            self.pc = self.reg[self.pc+1]
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
                self.flags = e_flag
                # else set to 0
            if reg_a < reg_b:
                # set lessthan flag to 1
                self.flags = l_flag
                # else set to 0
            if reg_a > reg_b:
                # set set greater than G flag to 1
                self.flags = g_flag
                # else set to 0
            else:
                self.flags = 0
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
        while True:
            command = self.ram[self.pc]
            self.branch[command]()


if len(sys.argv) != 2:
    print('ERROR: Must have file name')
    sys.exit(1)


c = CPU()
c.load(sys.argv[1])
c.run()
