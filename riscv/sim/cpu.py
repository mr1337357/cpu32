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
            if fun7 == 0x20:
                self.registers[rd] = self.registers[rs1] - self.registers[rs2]

    def handle_i(self):
        rd = opcode.get_rd(self.ir)
        rs1 = opcode.get_rs1(self.ir)
        rs2 = opcode.get_rs2(self.ir)
        imm = opcode.get_imm12(self.ir)
        fun = opcode.get_funct3(self.ir)
        if fun == 0:
            self.registers[rd] = self.registers[rs1] + imm
        if fun == 2:
            self.registers[rd] = self.registers[rs1] < imm

    def handle_l(self):
        pass

    def execute(self):
        op = opcode.match_opcode(self.ir)
        self.opcode = op
        print(op)
        if op[1] == 'r':
            self.handle_r()
        if op[1] == 'i':
            self.handle_i()
        return None

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
        print(self.registers)
        return res
