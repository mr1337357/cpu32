#include <stdio.h>

#include "elf.h"

int main(int argc,char **argv)
{
    
    elf_file *ef;
    ef = elf_open(argv[1]);
    
    return 0;
}