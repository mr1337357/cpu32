import elf

import sys

pc = 0

named_addresses={}
exports = []
memory = {}

def directive(line):
    global pc
    global exports
    if line[0] == '.org':
        pc = int(line[1],0)
        memory[pc] = []
    if line[0] == '.export':
        if line[1] in named_addresses:
            exports.append(line[1])

def label(line):
    global named_addresses
    name = line[0][:-1]
    named_addresses[name]=pc

rtypes = {
    'add': '0000000xxxxxxxxxx000xxxxx0110011',
    'sub': '0100000xxxxxxxxxx000xxxxx0110011',
    'sll': '0000000xxxxxxxxxx001xxxxx0110011',
    'slt': '0000000xxxxxxxxxx010xxxxx0110011',
    'sltu': '0000000xxxxxxxxxx011xxxxx0110011',
    'xor': '0000000xxxxxxxxxx100xxxxx0110011',
    'srl': '0000000xxxxxxxxxx101xxxxx0110011',
    'sra': '0100000xxxxxxxxxx101xxxxx0110011',
    'or': '0000000xxxxxxxxxx110xxxxx0110011',
    'and': '0000000xxxxxxxxxx111xxxxx0110011',
    }

utypes = {
    'lui':   'xxxxxxxxxxxxxxxxxxxxddddd0110111',
    'auipc': 'xxxxxxxxxxxxxxxxxxxxddddd0010111',
    }

itypes = {
    'addi': 'xxxxxxxxxxxxxxxxx000xxxxx0010011',
    'slti': 'xxxxxxxxxxxxxxxxx010xxxxx0010011',
    'sltiu': 'xxxxxxxxxxxxxxxxx011xxxxx0010011',
    'xori': 'xxxxxxxxxxxxxxxxx100xxxxx0010011',
    'ori': 'xxxxxxxxxxxxxxxxx110xxxxx0010011',
    'andi': 'xxxxxxxxxxxxxxxxx111xxxxx0010011',
    'slli': '00000xxxxxxxxxxxx001xxxxx0010011',
    'srli': '00000xxxxxxxxxxxx101xxxxx0010011',
    'srai': '01000xxxxxxxxxxxx101xxxxx0010011',
    }

def name2reg(name):
    namelist = [
         'zero','ra','sp','gp','tp','t0','t1','t2',
         's0','s1','a0','a1','a2','a3','a4','a5',
         'a6','a7','s2','s3','s4','s5','s6','s7',
         's8','s9','s10','s11','t3','t4','t5','t6']
    if name[0] == 'x':
        return int(name[1:])
    return namelist.index(name)

def rtype(line):
    global pc
    global memory
    global rtypes

    instr = [x for x in rtypes[line[0]]]
    rd = name2reg(line[1])
    rs1 = name2reg(line[2])
    rs2 = name2reg(line[3])
    for i in range(-8,-13,-1):
        instr[i] = str(rd&1)
        rd >>= 1
    for i in range(-16,-21,-1):
        instr[i] = str(rs1&1)
        rs1 >>= 1
    for i in range(-21,-26,-1):
        instr[i] = str(rs2&1)
        rs2 >>= 1
    instrb = int(''.join(instr),2)
    print(hex(instrb))
    pc += 4
    
def utype(line):
    global pc
    global memory
    global utypes
    
    instr = [x for x in utypes[line[0]]]
    print(instr)
    
def itype(line):
    global pc
    global memory
    global itypes
    instr = [x for x in itypes[line[0]]]
    rd = name2reg(line[1])
    rs1 = name2reg(line[2])
    imm = int(line[3])
    if imm < 0:
        imm = 4096 + imm
    for i in range(-21,-33,-1):
        instr[i] = str(imm & 1)
        imm >>= 1
    for i in range(-8,-13,-1):
        instr[i] = str(rd&1)
        rd >>= 1
    for i in range(-16,-21,-1):
        instr[i] = str(rs1&1)
        rs1 >>= 1
    instrb = int(''.join(instr),2)
    print(hex(instrb))
    pc += 4
    

instrs = {
    'lui': utype,
    'auipc': utype,
    'jal': utype,
    'jalr': None,
    'beq': None,
    'bne': None,
    'blt': None,
    'bge': None,
    'bltu': None,
    'bgeu': None,
    'lb': None,
    'lh': None,
    'lw': None,
    'lbu': None,
    'lhu': None,
    'sb': None,
    'sh': None,
    'sw': None,
    'addi': itype,
    'slti': itype,
    'sltiu': itype,
    'xori': itype,
    'ori': itype,
    'andi': itype,
    'slli': itype,
    'srli': itype,
    'srai': itype,
    'add': rtype,
    'sub': rtype,
    'sll': rtype,
    'slt': rtype,
    'sltu': rtype,
    'xor': rtype,
    'srl': rtype,
    'sra': rtype,
    'or': rtype,
    'and': rtype,
}

def trimmed(line):
    trimmed = line[:line.find(';')]
    s = [w for w in filter(lambda x: len(x) > 0,trimmed.split(' '))]
    o = []
    for w in s:
        o += [w for w in filter(lambda x: len(x) > 0,w.split(','))]
    return o

if __name__ == '__main__':
    infile = open(sys.argv[1],'r')
    for line in infile.readlines():
        trim = trimmed(line)
        if trim[0][0] == '.':
            directive(trim)
        elif ':' in trim[0]:
            label(trim)
    infile.seek(0)
    for line in infile.readlines():
        trim = trimmed(line)
        if trim[0] in instrs:
            if instrs[trim[0]] != None:
                instrs[trim[0]](trim)
            else:
                print('not impl: {}'.format(trim[0]))
        else:
            print(trim)
