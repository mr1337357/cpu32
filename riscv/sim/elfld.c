#include <stdio.h>
#include <elf.h>
#include <fcntl.h>
#include <stdlib.h>

#include "elfld.h"

struct _elfdata_private
{
};

elf_file *elf_open(char *filename)
{
    int in_fd;
    elf_file *efile;
    in_fd = open(filename,O_RDONLY);
    
}