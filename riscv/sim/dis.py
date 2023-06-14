#reference implementation: https://riscvasm.lucasteske.dev/

import elf
import mem

import sys

opcodes = {
    'xxxxxxxxxxxxxxxxxxxxxxxxx0110111': ['lui  ','x'],
    'xxxxxxxxxxxxxxxxxxxxxxxxx0010111': ['auipc','x'],
    'xxxxxxxxxxxxxxxxxxxxxxxxx1101111': ['jal  ','x'],
    'xxxxxxxxxxxxxxxxx000xxxxx1100111': ['jalr ','x'],
    'xxxxxxxxxxxxxxxxx000xxxxx1100011': ['beq  ','x'],
    'xxxxxxxxxxxxxxxxx001xxxxx1100011': ['bne  ','x'],
    'xxxxxxxxxxxxxxxxx100xxxxx1100011': ['blt  ','x'],
    'xxxxxxxxxxxxxxxxx101xxxxx1100011': ['bge  ','x'],
    'xxxxxxxxxxxxxxxxx110xxxxx1100011': ['bltu ','x'],
    'xxxxxxxxxxxxxxxxx111xxxxx1100011': ['bgeu ','x'],
    'xxxxxxxxxxxxxxxxx000xxxxx0000011': ['lb   ','x'],
    'xxxxxxxxxxxxxxxxx001xxxxx0000011': ['lh   ','x'],
    'xxxxxxxxxxxxxxxxx010xxxxx0000011': ['lw   ','x'],
    'xxxxxxxxxxxxxxxxx100xxxxx0000011': ['lbu  ','x'],
    'xxxxxxxxxxxxxxxxx101xxxxx0000011': ['lhu  ','x'],
    'xxxxxxxxxxxxxxxxx000xxxxx0100011': ['sb   ','x'],
    'xxxxxxxxxxxxxxxxx001xxxxx0100011': ['sh   ','x'],
    'xxxxxxxxxxxxxxxxx010xxxxx0100011': ['sw   ','x'],
    'xxxxxxxxxxxxxxxxx000xxxxx0010011': ['addi ','i'],
    'xxxxxxxxxxxxxxxxx010xxxxx0010011': ['slti ','x'],
    'xxxxxxxxxxxxxxxxx011xxxxx0010011': ['sltiu','x'],
    'xxxxxxxxxxxxxxxxx100xxxxx0010011': ['xori ','x'],
    'xxxxxxxxxxxxxxxxx110xxxxx0010011': ['ori  ','x'],
    'xxxxxxxxxxxxxxxxx111xxxxx0010011': ['andi ','x'],
    '00000xxxxxxxxxxxx001xxxxx0010011': ['slli ','x'],
    '00000xxxxxxxxxxxx101xxxxx0010011': ['srli ','x'],
    '01000xxxxxxxxxxxx101xxxxx0010011': ['srai ','x'],
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

def hexstr(num,size):
    
    h = hex(num)[2:]
    os = '0' * (size - len(h)) + h
    return os

def binstr(number):
    binary = bin(number)[2:]
    while len(binary) <32:
        binary = '0' + binary
    return binary

def get_opcode(instr):
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

def decode_i(instr):
    rd = (instr >> 7)  & 0x0000001F
    rs = (instr >> 15) & 0x0000001F
    imm = instr >> 20
    return 'x{}, x{}, {}'.format(str(rd),str(rs),hexstr(imm,8))
    
def decode_j(instr):
    rd = (instr >> 7)    & 0x0000001F
    imm = ((instr >> 20) & 0x000003FE) | ((instr >> 9) & 0x00000800) | ((instr >> 0) & 0x000FF000)
    return 'x{}, {}'.format(str(rd),hexstr(imm,8))

def decode_r(instr):
    rd =  (instr >> 7)  & 0x0000001F
    rs1 = (instr >> 15) & 0x0000001F
    rs2 = (instr >> 20) & 0x0000001F
    return 'x{}, x{}, x{}'.format(rd,rs1,rs2)
    
def decode_u(instr):
    rd = (instr >> 7)   & 0x0000001F
    imm = (instr >> 12) & 0x000FFFFF
    return 'x{}, {}'.format(rd,hex(imm))

def instr_to_string(instr):
    os = ''
    op = get_opcode(instr)
    if op:
        os += op[0]+ ' '
        if op[1] == 'i':
            os += decode_i(instr)
        if op[1] == 'j':
            os += decode_j(instr)
        if op[1] == 'r':
            os += decode_r(instr)
        if op[1] == 'u':
            os += decode_u(instr)
        return os
    return 'Unknown'

def fetch(pc,mem):
    ir = mem.read(pc) + mem.read(pc+1) * 256
    size = 2
    if ir & 3 == 3:
        ir += mem.read(pc+2) * 65536 + mem.read(pc+3) * 16777216
        size += 2
    return size,ir
        

if __name__ == '__main__':
    code = elf.elf_file(sys.argv[1])
    code.load()
    m = mem.mem()
    for i in range(len(code.sheaders)):
        section = code.sheaders[i]
        if section.sh_type == 1:
            if (section.sh_flags & 6)==6:
                m.create_region(section.sh_addr,section.sh_size)
                buff = code.read_segment(i)
                for j in range(len(buff)):
                    m.write(section.sh_addr+j,buff[j])
                print('{}'.format(section.name_text))
                pc = section.sh_addr
                while pc - section.sh_addr < section.sh_size:
                    size,ir = fetch(pc,m)
                    if size == 2:
                        sys.stdout.write('{}:     {} {}\n'.format(hexstr(pc,8),hexstr(ir,size*2),instr_to_string(ir)))
                    if size == 4:
                        sys.stdout.write('{}: {} {}\n'.format(hexstr(pc,8),hexstr(ir,size*2),instr_to_string(ir)))
                    pc += size
