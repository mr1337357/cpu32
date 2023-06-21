#include <stdio.h>
#include <elf.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include "elfld.h"

static int eline = 0;

struct _elfdata_private
{
    union 
    {
        uint8_t bytes[1];
        Elf32_Ehdr e32h;
        Elf64_Ehdr e64h;
    } header;
    union
    {
        uint8_t bytes[1];
        Elf32_Shdr *e32sh;
        Elf64_Shdr *e64sh;
    } sheaders; //section headers
    union
    {
        uint8_t bytes[1];
        Elf32_Phdr *e32ph;
        Elf64_Phdr *e64ph;
    } pheaders; //program headers
};

elf_file *elf_open(char *filename)
{
    int in_fd;
    elf_file *efile;
    int rv;
    
    in_fd = open(filename,O_RDONLY);
    if(in_fd < 0)
    {
        eline = __LINE__;
        return NULL;
    }
    efile = malloc(sizeof(elf_file));
    if(efile == NULL)
    {
        eline = __LINE__;
        return NULL;
    }
    efile->private = malloc(sizeof(elf_file));
    if(efile->private == NULL)
    {
        eline = __LINE__;
        return NULL;
    }
    rv = read(in_fd,efile->private->header.bytes,sizeof(Elf32_Ehdr)); //read a 32 bit header first
    if(rv < 1)
    {
        eline = __LINE__;
        return NULL;
    }
    if(strncmp((char *)efile->private->header.e32h.e_ident,ELFMAG,SELFMAG)!= 0)
    {
        eline = __LINE__;
        return NULL;
    }
    if(efile->private->header.e32h.e_type == ELFCLASS64)
    {
        read(in_fd,efile->private->header.bytes + sizeof(Elf32_Ehdr),sizeof(Elf64_Ehdr)-sizeof(Elf32_Ehdr)); //it's 64 bit so read the rest of the header
    }
    printf("%d\n",efile->private->header.e32h.e_type);
    //todo: grab section and program headers
    return efile;
}

int main(int argc,char **argv)
{
    elf_file *ef = NULL;
    ef = elf_open(argv[1]);
    if(ef == NULL)
    {
        printf("%d\n",eline);
    }
    else
    {
        printf("idk\n");
    }
    return 0;
}