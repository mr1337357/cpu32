opcodes = {
    'xxxxxxxxxxxxxxxxxxxxxxxxx0110111': ['lui  ','u'],
    'xxxxxxxxxxxxxxxxxxxxxxxxx0010111': ['auipc','u'],
    'xxxxxxxxxxxxxxxxxxxxxxxxx1101111': ['jal  ','j'],
    'xxxxxxxxxxxxxxxxx000xxxxx1100111': ['jalr ','l'],
    'xxxxxxxxxxxxxxxxx000xxxxx1100011': ['beq  ','j'],
    'xxxxxxxxxxxxxxxxx001xxxxx1100011': ['bne  ','j'],
    'xxxxxxxxxxxxxxxxx100xxxxx1100011': ['blt  ','j'],
    'xxxxxxxxxxxxxxxxx101xxxxx1100011': ['bge  ','j'],
    'xxxxxxxxxxxxxxxxx110xxxxx1100011': ['bltu ','j'],
    'xxxxxxxxxxxxxxxxx111xxxxx1100011': ['bgeu ','j'],
    'xxxxxxxxxxxxxxxxx000xxxxx0000011': ['lb   ','l'],
    'xxxxxxxxxxxxxxxxx001xxxxx0000011': ['lh   ','l'],
    'xxxxxxxxxxxxxxxxx010xxxxx0000011': ['lw   ','l'],
    'xxxxxxxxxxxxxxxxx100xxxxx0000011': ['lbu  ','l'],
    'xxxxxxxxxxxxxxxxx101xxxxx0000011': ['lhu  ','l'],
    'xxxxxxxxxxxxxxxxx000xxxxx0100011': ['sb   ','s'],
    'xxxxxxxxxxxxxxxxx001xxxxx0100011': ['sh   ','s'],
    'xxxxxxxxxxxxxxxxx010xxxxx0100011': ['sw   ','s'],
    'xxxxxxxxxxxxxxxxx000xxxxx0010011': ['addi ','i'],
    'xxxxxxxxxxxxxxxxx010xxxxx0010011': ['slti ','i'],
    'xxxxxxxxxxxxxxxxx011xxxxx0010011': ['sltiu','i'],
    'xxxxxxxxxxxxxxxxx100xxxxx0010011': ['xori ','i'],
    'xxxxxxxxxxxxxxxxx110xxxxx0010011': ['ori  ','i'],
    'xxxxxxxxxxxxxxxxx111xxxxx0010011': ['andi ','i'],
    '00000xxxxxxxxxxxx001xxxxx0010011': ['slli ','i'],
    '00000xxxxxxxxxxxx101xxxxx0010011': ['srli ','i'],
    '01000xxxxxxxxxxxx101xxxxx0010011': ['srai ','i'],
    '0000000xxxxxxxxxx000xxxxx0110011': ['add  ','r'],
    '0100000xxxxxxxxxx000xxxxx0110011': ['sub  ','r'],
    '0000000xxxxxxxxxx001xxxxx0110011': ['sll  ','r'],
    '0000000xxxxxxxxxx010xxxxx0110011': ['slt  ','r'],
    '0000000xxxxxxxxxx011xxxxx0110011': ['sltu ','r'],
    '0000000xxxxxxxxxx100xxxxx0110011': ['xor  ','r'],
    '0000000xxxxxxxxxx101xxxxx0110011': ['srl  ','r'],
    '0100000xxxxxxxxxx101xxxxx0110011': ['sra  ','r'],
    '0000000xxxxxxxxxx110xxxxx0110011': ['or   ','r'],
    '0000000xxxxxxxxxx111xxxxx0110011': ['and  ','r'],
}

namelist = [
     'zero','ra','sp','gp','tp','t0','t1','t2',
     's0','s1','a0','a1','a2','a3','a4','a5',
     'a6','a7','s2','s3','s4','s5','s6','s7',
     's8','s9','s10','s11','t3','t4','t5','t6']
     
def name_register(rnum):
    return namelist[rnum]

def binstr(number):
    binary = bin(number)[2:]
    while len(binary) <32:
        binary = '0' + binary
    return binary

def match_opcode(instr):
    binary = binstr(instr)
    for opcode,info in opcodes.items():
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

def get_op(instr):
    return instr & 0x0000007F    

def get_rd(instr):
    return (instr >>  7) & 0x0000001F
    
def get_rs1(instr):
    return (instr >> 15) & 0x0000001F
    
def get_rs2(instr):
    return (instr >> 20) & 0x0000001F
    
def get_imm20(instr):
    imm = (instr >>  12) & 0x000FFFFF
    if imm & 0x00080000:
        imm -= 0x00100000
    return imm

def get_imm12(instr):
    imm = (instr >> 20) & 0x00000FFF
    if imm & 0x00000800:
        imm -= 0x00001000
    return imm

def get_jimm20(instr):
    imm = ((instr >> 20) & 0x000007FE) | ((instr >> 9) & 0x00000800) | ((instr >> 0) & 0x000FF000)
    if imm & 0x00080000:
        imm -= 0x00100000
    return imm
    
def get_simm12(instr):
    imm = (instr >> 7)  & 0x0000001F | ((instr >> 25) & 0x0000007F)<<5
    if imm & 0x00000800:
        imm -= 0x00001000
    return imm
    
def get_limm12(instr):
    pass
    
def get_funct3(instr):
    f3 = (instr >> 12) & 0x00000007
    return f3
    
def get_funct7(instr):
    f7 = (instr >> 25) & 0x0000007F
    return f7
