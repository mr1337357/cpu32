class cpu:
    def __init__(self,mem):
        self.mem = mem
        self.pc = 0
        self.registers = [0] * 32
        
    def step(self):
        ir = self.mem.read(self.pc)
        ir += self.mem.read(self.pc+1) * 256
        self.pc += 2
        if ir & 0x03 == 0x03:
            ir += self.mem.read(self.pc) * 65536
            ir += self.mem.read(self.pc+1) * 16777216
            self.pc += 2
        print(hex(ir))