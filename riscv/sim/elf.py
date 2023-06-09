class elf_file:
    class elfheader:
        pass
    def __init__(self,filename):
        self.filename = filename
        self.header = None
        self.mem = {}

    def load_header(self,infile):
        self.header = elf_file.elfheader()
        self.header.EI_MAG = infile.read(4)
        if self.header.EI_MAG != '\x7FELF':
            raise Exception('bad magic')
        self.header.EI_CLASS = infile.read(1)
        self.header.EI_DATA = infile.read(1)
        self.header.EI_VERSION = infile.read(4)
        infile.read(6)
        self.header.e_type = infile.read(2)
        self.header.e_machine = infile.read(2)
        self.header.e_version = infile.read(4)
        self.header.e_entry = infile.read(4)
        self.header.e_phoff = infile.read(4)
        self.header.e_shoff = infile.read(4)
        infile.read(4)
        self.header.e_ehsize = infile.read(2)
        self.header.e_phentsize = infile.read(2)
        self.header.e_shentsize = infile.read(2)
        self.header.e_shnum = infile.read(2)
        self.header.e_shstrndx = infile.read(2)
        print(self.header.EI_MAG)

    def load(self):
        infile = open(self.filename,'r')
        self.load_header(infile)
        
        
if __name__ == '__main__':
    import sys
    infile = sys.argv[1]
    e = elf_file(infile)
    e.load()