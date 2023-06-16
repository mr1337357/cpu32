import opcode
from rvtypes import uint32

class cpu:
    def __init__(self,mem):
        self.mem = mem
        self.ir = uint32(0)
        self.pc = uint32(0)
        self.registers = [uint32(0)] * 32

    def handle_r(self):
        rd = opcode.get_rd(self.ir)
        rs1 = opcode.get_rs1(self.ir)
        rs2 = opcode.get_rs2(self.ir)
        fun3 = opcode.get_funct3(self.ir)
        fun7 = opcode.get_funct7(self.ir)
        if fun3 == 0x00:
            if fun7 == 0x00:
                self.registers[rd] = self.registers[rs1] + self.registers[rs2]
            elif fun7 == 0x20:
                self.registers[rd] = self.registers[rs1] - self.registers[rs2]
            else:
                raise Exception('unimplemented type r {} {}'.format(fun3, fun7))
        else:
            raise Exception('unimplemented type r {} {}'.format(fun3, fun7))

    def handle_i(self):
        rd = opcode.get_rd(self.ir)
        rs1 = opcode.get_rs1(self.ir)
        rs2 = opcode.get_rs2(self.ir)
        imm = opcode.get_imm12(self.ir)
        fun = opcode.get_funct3(self.ir)
        if fun == 0:
            self.registers[rd] = self.registers[rs1] + imm
        elif fun == 2:
            self.registers[rd] = self.registers[rs1] < imm
        else:
            raise Exception('unimplemented')

    def handle_s(self):
        rs1 = opcode.get_rs1(self.ir)
        rs2 = opcode.get_rs2(self.ir)
        imm = opcode.get_simm12(self.ir)
        fun = opcode.get_funct3(self.ir)
        wv = int(self.registers[rs2])
        addr = int(self.registers[rs1] + imm)
        print(imm,repr(self.registers[rs1]))
        self.mem.write(addr,wv)
        if fun > 0:
            self.mem.write(addr+1,wv>>8)
        if fun > 1:
            self.mem.write(addr+2,wv>>16)
            self.mem.write(addr+3,wv>>24)

    def handle_j(self):
        rd = opcode.get_rd(self.ir)
        imm20 = opcode.get_jimm20(self.ir)
        op = opcode.get_op(self.ir)
        if op == 0x6F:
            self.registers[rd] = uint32(self.pc)
            self.pc += imm20
            self.pc -= 4 #hack (need to probably redo all instructions with current pc as input)
        else:
            raise Exception('unimplemented')
        
    def handle_u(self):
        rd = opcode.get_rd(self.ir)
        imm20 = opcode.get_jimm20(self.ir)
        op = opcode.get_op(self.ir)
        imm20 << 12
        if op == 0x37:
            self.registers[rd] = imm20
        else:
            raise Exception('unimplemented')
        
    def handle_l(self):
        rd = opcode.get_rd(self.ir)
        rs1 = opcode.get_rs1(self.ir)
        imm = opcode.get_imm12(self.ir)
        fun = opcode.get_funct3(self.ir)
        addr = int(self.registers[rs1] + imm)
        op = opcode.get_op(self.ir)
        if op == 0x67: #jalr
            self.pc = int(addr)
            self.registers[rd] = self.pc
        elif fun == 0x00 or fun == 0x04: #lb lbu
            rv = self.mem.read(addr)
            self.registers[rd] = uint32(rv)
        elif fun == 0x02:
            rv = self.mem.read(addr) + (self.mem.read(addr+1) << 8) + (self.mem.read(addr+1) << 16) + (self.mem.read(addr+1) << 24)
            self.registers[rd] = uint32(rv)
        else:
            raise Exception('unimplemented')

    def execute(self):
        self.registers[0] = 0
        op = opcode.match_opcode(self.ir)
        self.opcode = op
        print(op)
        if op[1] == 'r':
            self.handle_r()
        elif op[1] == 'i':
            self.handle_i()
        elif op[1] == 's':
            self.handle_s()
        elif op[1] == 'j':
            self.handle_j()
        elif op[1] == 'u':
            self.handle_u()
        elif op[1] == 'l':
            self.handle_l()
            
        
        else:
            return 1
        return 0

    def fetch(self):
        self.ir = self.mem.read(self.pc)
        self.ir += self.mem.read(self.pc+1) * 256
        self.pc += 2
        if self.ir & 0x03 == 0x03:
            self.ir += self.mem.read(self.pc) * 65536
            self.ir += self.mem.read(self.pc+1) * 16777216
            self.pc += 2
        
    def step(self):
        self.fetch()
        res = self.execute()
        print(hex(self.pc)+' '+repr(self.registers))
        return res
