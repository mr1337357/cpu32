#reference implementation: https://riscvasm.lucasteske.dev/

import sys
import ihex

opcodes = {
    0x13: ('addi','i'),
    0x6F: ('jal','j'),
}

def get_opcode(instr):
    op = instr & 0x0000007F
    if op in opcodes:
        return opcodes[op]
    return None

def decode_i(instr):
    rd = (instr >> 7) & 0x0000001F
    rs = (instr >> 15) & 0x0000001F
    imm = instr >> 20
    return 'x{}, x{}, {}'.format(str(rd),str(rs),ihex.ihex.hexstr(None,imm,8))
    
def decode_j(instr):
    rd = (instr >> 7)   & 0x0000001F
    imm = ((instr >> 20) & 0x000003FE) | ((instr >> 9) & 0x00000800) | ((instr >> 0) & 0x000FF000)
    return 'x{}, {}'.format(str(rd),ihex.ihex.hexstr(None,imm,8))

def instr_to_string(instr):
    os = ''
    op = get_opcode(instr)
    if op:
        os += op[0]+ ' '
        if op[1] == 'i':
            os += decode_i(instr)
        if op[1] == 'j':
            os += decode_j(instr)
        return os
    return 'Unknown'

infile = ihex.ihex(sys.argv[1])
infile.load()

for pc in infile.mem:
    offset = 0
    while offset < len(infile.mem[pc]):
        try:
            instr = 0
            for i in range(4):
                instr *= 256
                byte = infile.fetch(pc+offset)
                offset += 1
                instr += byte
            sys.stdout.write(ihex.ihex.hexstr(None,pc + offset,8)+': '+ihex.ihex.hexstr(None,instr,8)+' ')
            sys.stdout.write(instr_to_string(instr)+'\n')
        except Exception as e:
            print(e)
        