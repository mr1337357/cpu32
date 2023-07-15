#include <stdio.h>

#include "elf.h"
#include "mem.h"

#if defined(DEBUG)
#define DEBUG_PRINT(x,...) fprintf(stderr,"%s(%d): " x,__FILE__,__LINE__,__VA_ARGS__)
#endif

int load_elf(elf_file *ef)
{
    int i;
    int nseg;
    int flags;
    uint64_t section_address;
    int section_size;
    uint8_t *mem_ptr;
    uint64_t permissions;
    mem_init();
    nseg = elf_get_number_of_sections(ef);
    for(i=0;i<nseg;i++)
    {
        permissions = 0;
        flags = elf_get_section_flags(ef,i);
        if(flags & SHF_ALLOC)
        {
            section_address = elf_get_section_address(ef,i);
            section_size = elf_get_section_size(ef,i);
            if(flags & SHF_WRITE)
            {
                permissions |= MEM_WR;
            }
            if(flags & SHF_EXECINSTR)
            {
                permissions |= MEM_EX;
            }
            mem_make_segment(section_address, section_size,permissions);
            mem_ptr = mem_get_segment_ptr(section_address);
            elf_copy_section_to_array(ef,i,mem_ptr);
        }
    }
    mem_dump();
    return 0;
}

int main(int argc,char **argv)
{
    
    elf_file *ef;
    ef = elf_open(argv[1]);
    if(ef == NULL)
    {
        return 1;
    }
    mem_init();
    load_elf(ef);
    return 0;
}