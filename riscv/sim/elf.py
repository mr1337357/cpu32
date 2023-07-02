class elf_file:
    class elfheader:
        pass
    def __init__(self,filename):
        self.filename = filename
        self.header = None
        self.mem = {}

    def int_from_file(self,file,length):
        num = 0
        for i in range(length):
            num += file.read(1)[0] * (256 ** i)
        return num

    def load_header(self,infile):
        self.header = elf_file.elfheader()
        self.header.EI_MAG = infile.read(4)
        if self.header.EI_MAG != b'\x7fELF':
            raise Exception('bad magic')
        self.header.EI_CLASS = self.int_from_file(infile,1)
        self.header.EI_DATA = self.int_from_file(infile,1)
        self.header.EI_VERSION = self.int_from_file(infile,1)
        self.header.EI_OSABI = self.int_from_file(infile,1)
        self.header.EI_ABIVERSION = self.int_from_file(infile,1)
        self.header.EI_PAD = infile.read(7)
        self.header.e_type = self.int_from_file(infile,2)
        self.header.e_machine = self.int_from_file(infile,2)
        self.header.e_version = self.int_from_file(infile,4)
        if self.header.EI_CLASS == 1:
            self.header.e_entry = self.int_from_file(infile,4)
            self.header.e_phoff = self.int_from_file(infile,4)
            self.header.e_shoff = self.int_from_file(infile,4)
        if self.header.EI_CLASS == 2:
            self.header.e_entry = self.int_from_file(infile,8)
            self.header.e_phoff = self.int_from_file(infile,8)
            self.header.e_shoff = self.int_from_file(infile,8)
        self.header.e_flags = self.int_from_file(infile,4)
        self.header.e_ehsize = self.int_from_file(infile,2)
        self.header.e_phentsize = self.int_from_file(infile,2)
        self.header.e_phnum = self.int_from_file(infile,2)
        self.header.e_shentsize = self.int_from_file(infile,2)
        self.header.e_shnum = self.int_from_file(infile,2)
        self.header.e_shstrndx = self.int_from_file(infile,2)

    def load_pheader(self,infile):
        infile.seek(self.header.e_phoff)
        self.pheaders = []
        for i in range(self.header.e_phnum):
            h = elf_file.elfheader()
            h.p_type = self.int_from_file(infile,4)
            if self.header.EI_CLASS == 1:
                h.p_offset = self.int_from_file(infile,4)
                h.p_vaddr = self.int_from_file(infile,4)
                h.p_paddr = self.int_from_file(infile,4)
                h.p_filesz = self.int_from_file(infile,4)
                h.p_memsz = self.int_from_file(infile,4)
                h.p_flags = self.int_from_file(infile,4)
                h.p_align = self.int_from_file(infile,4)
            if self.header.EI_CLASS == 2:
                h.p_flags = self.int_from_file(infile,4)
                h.p_offset = self.int_from_file(infile,8)
                h.p_vaddr = self.int_from_file(infile,8)
                h.p_paddr = self.int_from_file(infile,8)
                h.p_filesz = self.int_from_file(infile,8)
                h.p_memsz = self.int_from_file(infile,8)
                h.p_align = self.int_from_file(infile,8)
            self.pheaders.append(h)
                    
    def load_section_headers(self,infile):
        infile.seek(self.header.e_shoff)
        self.sheaders = []
        for i in range(self.header.e_shnum):
            h = elf_file.elfheader()
            h.sh_name = self.int_from_file(infile,4)
            h.sh_type = self.int_from_file(infile,4)
            if self.header.EI_CLASS == 1:
                h.sh_flags = self.int_from_file(infile,4)
                h.sh_addr = self.int_from_file(infile,4)
                h.sh_offset = self.int_from_file(infile,4)
                h.sh_size = self.int_from_file(infile,4)
                h.sh_link = self.int_from_file(infile,4)
                h.sh_info = self.int_from_file(infile,4)
                h.sh_addralign = self.int_from_file(infile,4)
                h.sh_entsize = self.int_from_file(infile,4)
            if self.header.EI_CLASS == 2:
                h.sh_flags = self.int_from_file(infile,8)
                h.sh_addr = self.int_from_file(infile,8)
                h.sh_offset = self.int_from_file(infile,8)
                h.sh_size = self.int_from_file(infile,8)
                h.sh_link = self.int_from_file(infile,4)
                h.sh_info = self.int_from_file(infile,4)
                h.sh_addralign = self.int_from_file(infile,8)
                h.sh_entsize = self.int_from_file(infile,8)
            self.sheaders.append(h)
            
    def load_names(self,infile):
        infile.seek(self.sheaders[self.header.e_shstrndx].sh_offset)
        self.names = infile.read(self.sheaders[self.header.e_shstrndx].sh_size)
        for h in self.sheaders:
            h.name_text = ''
            i = h.sh_name
            while self.names[i] != 0:
                h.name_text += chr(self.names[i])
                i += 1
    
    def load(self):
        infile = open(self.filename,'rb')
        self.load_header(infile)
        self.load_pheader(infile)
        self.load_section_headers(infile)
        self.load_names(infile)
        
    def read_segment(self,index):
        infile = open(self.filename,'rb')
        infile.seek(self.sheaders[index].sh_offset)
        return infile.read(self.sheaders[index].sh_size)
        
if __name__ == '__main__':
    import sys
    infile = sys.argv[1]
    e = elf_file(infile)
    e.load()
    print('elf header:')
    for elem in e.header.__dict__:
        try:
            print('   {} = {}'.format(elem,hex(e.header.__dict__[elem])))
        except:
            print('   {} = {}'.format(elem,e.header.__dict__[elem]))

    for h in e.pheaders:
        print('Program Header:')
        for elem in h.__dict__:
            try:
                print('   {} = {}'.format(elem,hex(h.__dict__[elem])))
            except:
                print('   {} = {}'.format(elem,h.__dict__[elem]))
    i=0
    for h in e.sheaders:
        print('Section Header {}:'.format(i))
        i = i + 1
        for elem in h.__dict__:
            try:
                print('   {} = {}'.format(elem,hex(h.__dict__[elem])))
            except:
                print('   {} = {}'.format(elem,h.__dict__[elem]))
