#reference implementation: https://riscvasm.lucasteske.dev/

import elf
import mem
import opcode
import sys

def hexstr(num,size):
    if num < 0:
        num += 2**32
    h = hex(num)[2:]
    os = '0' * (size - len(h)) + h
    return os

def binstr(number):
    binary = bin(number)[2:]
    while len(binary) <32:
        binary = '0' + binary
    return binary

def decode_r(instr):
    rd = opcode.get_rd(instr)
    rs1 = opcode.get_rs1(instr)
    rs2 = opcode.get_rs2(instr)
    return '{}, {}, {}'.format(opcode.name_register(rd),opcode.name_register(rs1),opcode.name_register(rs2))

def decode_i(instr):
    rd = opcode.get_rd(instr)
    rs1 = opcode.get_rs1(instr)
    rs2 = opcode.get_rs2(instr)
    imm = opcode.get_imm12(instr)
    return '{}, {}, {}'.format(opcode.name_register(rd),opcode.name_register(rs1),imm)

def decode_s(instr):
    rd = opcode.get_rd(instr)
    rs1 = opcode.get_rs1(instr)
    rs2 = opcode.get_rs2(instr)
    imm = opcode.get_simm12(instr)
    return '{}, {}({})'.format(opcode.name_register(rs1),imm,opcode.name_register(rs2))
    
def decode_u(instr):
    rd = opcode.get_rd(instr)
    rs1 = opcode.get_rs1(instr)
    rs2 = opcode.get_rs2(instr)
    imm = opcode.get_imm20(instr)
    return '{}, {}'.format(opcode.name_register(rd),imm)
    
def decode_j(instr):
    rd = opcode.get_rd(instr)
    rs1 = opcode.get_rs1(instr)
    rs2 = opcode.get_rs2(instr)
    imm = opcode.get_jimm20(instr)
    return '{}, {}'.format(opcode.name_register(rd),hexstr(imm,8))

def decode_l(instr):
    rd = opcode.get_rd(instr)
    rs1 = opcode.get_rs1(instr)
    rs2 = opcode.get_rs2(instr)
    imm = opcode.get_imm12(instr)
    return '{}, {}({})'.format(opcode.name_register(rd),imm,opcode.name_register(rs1))

def instr_to_string(instr):
    os = ''
    op = opcode.match_opcode(instr,'ic')
    if op:
        os += op[0]+ ' '
        if op[1] == 'i':
            os += decode_i(instr)
        if op[1] == 'l':
            os += decode_l(instr)
        if op[1] == 'j':
            os += decode_j(instr)
        if op[1] == 'r':
            os += decode_r(instr)
        if op[1] == 'u':
            os += decode_u(instr)
        if op[1] == 's':
            os += decode_s(instr)
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
