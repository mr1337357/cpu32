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
bne     'xxxxxxxxxxxxxxxxx001xxxxx1100011': ['bne'],
blt     'xxxxxxxxxxxxxxxxx100xxxxx1100011': ['blt'],
bge     'xxxxxxxxxxxxxxxxx101xxxxx1100011': 
bltu    'xxxxxxxxxxxxxxxxx110xxxxx1100011': 
bgeu    'xxxxxxxxxxxxxxxxx111xxxxx1100011': 
lb      'xxxxxxxxxxxxxxxxx000xxxxx0000011': 
lh      'xxxxxxxxxxxxxxxxx001xxxxx0000011': 
lw      'xxxxxxxxxxxxxxxxx010xxxxx0000011': 
lbu     'xxxxxxxxxxxxxxxxx100xxxxx0000011': 
lhu     'xxxxxxxxxxxxxxxxx101xxxxx0000011': 
sb      'xxxxxxxxxxxxxxxxx000xxxxx0100011': 
sh      'xxxxxxxxxxxxxxxxx001xxxxx0100011': 
sw      'xxxxxxxxxxxxxxxxx010xxxxx0100011': 
addi    'xxxxxxxxxxxxxxxxx000xxxxx0010011': 
slti    'xxxxxxxxxxxxxxxxx010xxxxx0010011': 
sltiu   'xxxxxxxxxxxxxxxxx011xxxxx0010011': 
xori    'xxxxxxxxxxxxxxxxx100xxxxx0010011': 
ori     'xxxxxxxxxxxxxxxxx110xxxxx0010011': 
andi    'xxxxxxxxxxxxxxxxx111xxxxx0010011': 
slli    '00000xxxxxxxxxxxx001xxxxx0010011': 
srli    '00000xxxxxxxxxxxx101xxxxx0010011': 
srai    '01000xxxxxxxxxxxx101xxxxx0010011': 
add     '0000000xxxxxxxxxx000xxxxx0110011': 
sub     '0100000xxxxxxxxxx000xxxxx0110011': 
sll     '0000000xxxxxxxxxx001xxxxx0110011': 
slt     '0000000xxxxxxxxxx010xxxxx0110011': 
sltu    '0000000xxxxxxxxxx011xxxxx0110011': 
xor     '0000000xxxxxxxxxx100xxxxx0110011': 
srl     '0000000xxxxxxxxxx101xxxxx0110011': 
sra     '0100000xxxxxxxxxx101xxxxx0110011': 
or      '0000000xxxxxxxxxx110xxxxx0110011': 
and     '0000000xxxxxxxxxx111xxxxx0110011': 
        
    def decode(self,ir):
        pass
        
    def step(self):
        ir = self.mem.read(self.pc)
        ir += self.mem.read(self.pc+1) * 256
        self.pc += 2
        if ir & 0x03 == 0x03:
            ir += self.mem.read(self.pc) * 65536
            ir += self.mem.read(self.pc+1) * 16777216
            self.pc += 2
        print(hex(ir))
