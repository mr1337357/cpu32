import elf
import mem
import cpu

import sys

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
    c = cpu.cpu(m)
    c.pc = code.header.e_entry
    for i in range(100):
        c.step()