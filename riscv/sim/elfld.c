#include <stdio.h>
#include <elf.h>
#include <fcntl.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>

#include "elfld.h"

struct _elfdata_private
{
    union 
    {
        uint8_t *bytes;
        Elf32_Ehdr e32h;
        Elf64_Ehdr e64h;
    } header;
    union
    {
        uint8_t *bytes;
        Elf32_Shdr *e32sh;
        Elf64_Shdr *e64sh;
    } sheaders; //section headers
    union
    {
        uint8_t *bytes;
        Elf32_Phdr *e32ph;
        Elf64_Phdr *e64ph;
    } pheaders; //program headers
};

elf_file *elf_open(char *filename)
{
    int in_fd;
    elf_file *efile;
    
    
    in_fd = open(filename,O_RDONLY);
    efile = malloc(sizeof(elf_file));
    efile->private = malloc(sizeof(elf_file));
    efile->private->header.bytes = malloc(sizeof(Elf64_Ehdr)); //allocate enough for 64 bit since header is bigger
    read(in_fd,efile->private->header.bytes,sizeof(Elf32_Ehdr)); //read a 32 bit header first
    if(strncmp((char *)efile->private->header.e32h.e_ident,ELFMAG,SELFMAG)!= 0)
    {
        free(efile->private->header.bytes);
        free(efile->private);
        free(efile);
        return 0;
    }
    if(efile->private->header.e32h.e_type == ELFCLASS64)
    {
        read(in_fd,efile->private->header.bytes + sizeof(Elf32_Ehdr),sizeof(Elf64_Ehdr)-sizeof(Elf32_Ehdr)); //it's 64 bit so read the rest of the header
    }
    //todo
    return efile;
}