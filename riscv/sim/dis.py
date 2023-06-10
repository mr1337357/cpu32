#reference implementation: https://riscvasm.lucasteske.dev/

import elf
import mem

import sys



opcodes = {
    0x17: (0,'auipc','u'),
    0x37: (0,'lui','i'),
    0x6f: (0,'jal','j'),
    0x67: (1,
        {
            0x00: (0,'jalr','r'),
        }),
    0x63: (1,
        {
            0x00: (0,'beq','r'),
            0x01: (0,'bne','r'),
            0x04: (0,'blt','r'),
            0x05: (0,'bge','r'),
            0x06: (0,'bltu','r'),
            0x07: (0,'bgeu','r'),
        }),
    0x03: (1,
        {
            0x00: (0,'lb','r'),
            0x01: (0,'lh','r'),
            0x02: (0,'lw','r'),
            0x03: (0,'ld','x'),
            0x04: (0,'lbu','r'),
            0x05: (0,'lhu','r'),
        }),
    0x23: (1,
        {
            0x00: (0,'sb','r'),
            0x01: (0,'sh','r'),
            0x02: (0,'sw','r'),
        }),
    0x13: (1,
        {
            0x00: (0,'addi','i'),
            0x02: (0,'slti','i'),
            0x03: (0,'sltiu','i'),
            0x04: (0,'xori','i'),
            0x06: (0,'ori','i'),
            0x07: (0,'andi','i'),
            0x01: (2,
            {
                0x00: (0,'slli','i'),
            }),
            0x05: (2,
            {
                0x00: (0,'srli','i'),
                0x08: (0,'srai','i'),
            }),
        }),
    0x33: (1,
        {
            0x00: (2,
            {
                0x00: (0,'add','r'),
                0x20: (0,'sub','r'),
            }),
            0x01: (0,'sll','r'),
            0x02: (0,'slt','r'),
            0x03: (0,'sltu','r'),
            0x04: (0,'xor','r'),
            0x05: (2,
            {
                0x00: (0,'srl','r'),
                0x20: (0,'sra','r'),
            }),
            0x06: (0,'or','r'),
            0x07: (0,'and','r'),
        }),
}


def hexstr(num,size):
    
    h = hex(num)[2:]
    os = '0' * (size - len(h)) + h
    return os

def get_opcode(instr):
    op = instr & 0x0000007F
    table = opcodes
    opcode = None
    if op in table:
        opcode = table[op]
        if opcode[0] == 1:
            f3 = (instr >>12) & 0x00000007
            if f3 in opcode[1]:
                opcode = opcode[1][f3]
                if opcode[0] == 2:
                    f7 = (instr >> 25) & 0x0000007F
                    if f7 in opcode[1]:
                        opcode = opcode[1][f7]

    if opcode and opcode[0] != 0:
        opcode = None
    return opcode

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
        os += op[1]+ ' '
        if op[2] == 'i':
            os += decode_i(instr)
        if op[2] == 'j':
            os += decode_j(instr)
        if op[2] == 'r':
            os += decode_r(instr)
        if op[2] == 'u':
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