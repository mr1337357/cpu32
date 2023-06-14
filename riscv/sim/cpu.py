class cpu:
    def __init__(self,mem):
        self.mem = mem
        self.pc = 0
        self.registers = [0] * 32
        
    opcodes = {
        'xxxxxxxxxxxxxxxxxxxxxxxxx0110111': ['lui'],
        'xxxxxxxxxxxxxxxxxxxxxxxxx0010111': ['auipc'],
        'xxxxxxxxxxxxxxxxxxxxxxxxx1101111': ['jal'],
        'xxxxxxxxxxxxxxxxx000xxxxx1100111': ['jalr'],
        'xxxxxxxxxxxxxxxxx000xxxxx1100011': ['beq'],
        'xxxxxxxxxxxxxxxxx001xxxxx1100011': ['bne'],
        'xxxxxxxxxxxxxxxxx100xxxxx1100011': ['blt'],
        'xxxxxxxxxxxxxxxxx101xxxxx1100011': ['bge'],
        'xxxxxxxxxxxxxxxxx110xxxxx1100011': ['bltu'],
        'xxxxxxxxxxxxxxxxx111xxxxx1100011': ['bgeu'],
        'xxxxxxxxxxxxxxxxx000xxxxx0000011': ['lb'],
        'xxxxxxxxxxxxxxxxx001xxxxx0000011': ['lh'],
        'xxxxxxxxxxxxxxxxx010xxxxx0000011': ['lw'],
        'xxxxxxxxxxxxxxxxx100xxxxx0000011': ['lbu'],
        'xxxxxxxxxxxxxxxxx101xxxxx0000011': ['lhu'],
        'xxxxxxxxxxxxxxxxx000xxxxx0100011': ['sb'],
        'xxxxxxxxxxxxxxxxx001xxxxx0100011': ['sh'],
        'xxxxxxxxxxxxxxxxx010xxxxx0100011': ['sw'],
        'xxxxxxxxxxxxxxxxx000xxxxx0010011': ['addi'],
        'xxxxxxxxxxxxxxxxx010xxxxx0010011': ['slti'],
        'xxxxxxxxxxxxxxxxx011xxxxx0010011': ['sltiu'],
        'xxxxxxxxxxxxxxxxx100xxxxx0010011': ['xori'],
        'xxxxxxxxxxxxxxxxx110xxxxx0010011': ['ori'],
        'xxxxxxxxxxxxxxxxx111xxxxx0010011': ['andi'],
        '00000xxxxxxxxxxxx001xxxxx0010011': ['slli'],
        '00000xxxxxxxxxxxx101xxxxx0010011': ['srli'],
        '01000xxxxxxxxxxxx101xxxxx0010011': ['srai'],
        '0000000xxxxxxxxxx000xxxxx0110011': ['add'],
        '0100000xxxxxxxxxx000xxxxx0110011': ['sub'],
        '0000000xxxxxxxxxx001xxxxx0110011': ['sll'],
        '0000000xxxxxxxxxx010xxxxx0110011': ['slt'],
        '0000000xxxxxxxxxx011xxxxx0110011': ['sltu'],
        '0000000xxxxxxxxxx100xxxxx0110011': ['xor'],
        '0000000xxxxxxxxxx101xxxxx0110011': ['srl'],
        '0100000xxxxxxxxxx101xxxxx0110011': ['sra'],
        '0000000xxxxxxxxxx110xxxxx0110011': ['or'],
        '0000000xxxxxxxxxx111xxxxx0110011': ['and'],
    }
    
    def binstr(self,number):
        binary = bin(number)[2:]
        while len(binary) <32:
            binary = '0' + binary
        return binary
    
    def get_instr(self,ir):
        binary = self.binstr(ir)
        for opcode,info in self.opcodes.items():
            match = True
            for o,i in zip(opcode,binary):
                if o == 'x':
                    continue
                if o != i:
                    match = False
                    break
            if match == True:
                return info
        return None
    
    def decode(self,ir):
        instr = self.get_instr(ir)
        
    def step(self):
        ir = self.mem.read(self.pc)
        ir += self.mem.read(self.pc+1) * 256
        self.pc += 2
        if ir & 0x03 == 0x03:
            ir += self.mem.read(self.pc) * 65536
            ir += self.mem.read(self.pc+1) * 16777216
            self.pc += 2
        self.decode(ir)
