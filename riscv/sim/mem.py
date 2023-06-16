class mem:
    class memregion:
        def __init__(self):
            self.start = 0
            self.end = 0
            self.size = 0
            self.mem = []
            
        def __str__(self):
            return 'Region {}-{}: {}'.format(hex(self.start),hex(self.end),self.mem)
            
        def __repr__(self):
            return str(self)
            
    def __init__(self):
        self.regions = []
    
    def create_region(self,start,size):
        region = mem.memregion()
        region.start = start
        region.size = size
        region.end = start+size-1
        region.mem = [0] * size
        self.regions.append(region)
        
    def write(self,address,value):
        value &= 0xFF
        for region in self.regions:
            if address >= region.start:
                if address <= region.end:
                    region.mem[address-region.start] = value
                    return
        raise Exception('not a valid address {}'.format(hex(address)))
        
    
    def read(self,address):
        for region in self.regions:
            if address >= region.start:
                if address <= region.end:
                    return region.mem[address-region.start]                
        raise Exception('not a valid address {}'.format(hex(address)))
        
    def dump(self):
        dumpfile = open('memdump','w')
        for region in self.regions:
            addr = region.start
            while addr < region.end:
                dumpfile.write('{}: '.format(hex(addr)))
                for i in range(16):
                    if addr > region.end:
                        break
                    dumpfile.write('{} '.format(hex(self.read(addr)+256)[3:]))
                    addr += 1
                dumpfile.write('\n')
