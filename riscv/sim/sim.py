import elf
import mem
import cpu
from rvtypes import uint32
import sys

bp = []
STACK_TOP=0x8000000
STACK_SIZE=0x1000

if __name__ == '__main__':
    code = elf.elf_file(sys.argv[1])
    code.load()
    m = mem.mem()
    for i in range(len(code.sheaders)):
        section = code.sheaders[i]
        if section.sh_type == 1:
            if (section.sh_flags & 6)==6 or (section.sh_flags & 6)==2:
                m.create_region(section.sh_addr,section.sh_size)
                buff = code.read_segment(i)
                for j in range(len(buff)):
                    m.write(section.sh_addr+j,buff[j])
    m.create_region(STACK_TOP,STACK_SIZE)
    c = cpu.cpu(m)
    c.registers[2] = uint32(STACK_TOP+STACK_SIZE)
    c.pc = code.header.e_entry
    try:
        while True:
            res = c.step()
            if res > 0:
                break
            if c.pc in bp:
                break
    except Exception as e:
        import traceback
        traceback.print_exception(e)
        print(e)
    #m.dump()
