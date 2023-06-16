import elf
import mem
import cpu
from rvtypes import uint32
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
    m.create_region(0x8000000,0x100000)
    c = cpu.cpu(m)
    c.registers[2] = uint32(0x8000000+0x100000)
    c.pc = code.header.e_entry
    for i in range(100):
        res = c.step()
        if res > 0:
            break
