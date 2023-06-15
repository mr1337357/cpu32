import opcode

class cpu:
    def __init__(self,mem):
        self.mem = mem
        self.ir = 0
        self.pc = 0
        self.registers = [0] * 32

    def handle_r(self):
        rd = opcode.get_rd(self.ir)
        print(rd)

    def execute(self):
        op = opcode.match_opcode(self.ir)
        print(op)
        if op[1] == 'r':
            self.handle_r()
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
        return res
