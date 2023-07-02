class ihex:
    def __init__(self,filename):
        self.filename = filename
        self.mem = {}
    
    def verify(self,line,cksum):
        start = line.find(':')
        if start < 0:
            return None
        
    def hexstr(self,num,size):
        
        h = hex(num)[2:]
        os = '0' * (size - len(h)) + h
        return os
        
    
    def parseline(self, line):
        start = line.find(':')
        if start < 0:
            return None
        datalen = int(line[start+1:start+3],16)
        address = int(line[start+3:start+7],16)
        recordtype = int(line[start+7:start+9],16)
        data = line[start+9:start+9+datalen*2]
        cksum = int(line[start+9+datalen*2:start+11+datalen*2],16)
        return address,recordtype,data,cksum
    
    def load(self):
        self.mem = {}
        with open(self.filename,'r') as infile:
            pc = 0
            for line in infile.readlines():
                address,recordtype,data,cksum = self.parseline(line)
                if recordtype == 0x04:
                    pc = int(data,16) * 65536
                if recordtype == 0x00:
                    if not pc in self.mem:
                        self.mem[pc]=[]
                    while len(self.mem[pc]) < address+len(data)//2:
                        self.mem[pc].append(0)
                    for i in range(len(data)//2):
                        self.mem[pc][address+i]=int(data[2*i:2*i+2],16)
                        
    def save(self):
        for pc in self.mem:
            pass
            
    def fetch(self,address):
        pc = address // 65536
        offset = address - (pc * 65536)
        return self.mem[pc][offset]
        
    def set(self,address,value):
        pc = address // 65536
        offset = address - (pc * 65536)
        self.mem[pc][offset] = value
                        
    def __str__(self):
        os = ''
        for pc in self.mem:
            for i in range(len(self.mem[pc])):
                if i % 16 == 0:
                    os += '\n' + self.hexstr(pc+i,8) + ': '
                os += self.hexstr(self.mem[pc][i],2) + ' '
            os += '\n'
        return os
    
    def __repr__(self):
        return 'repr'
                
if __name__ == '__main__':
    ih = ihex('test.ihex')
    ih.load()
    print(ih)
