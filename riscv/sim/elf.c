
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include <stdbool.h>

// for memcpy
#include <string.h>

// https://www.man7.org/linux/man-pages/man5/elf.5.html
#include <elf.h>

#include "elf.h"

#if defined(DEBUG)
#define DEBUG_PRINT(x,...) fprintf(stderr,"%s(%d): " x,__FILE__,__LINE__,__VA_ARGS__)
#endif

// #pragma pack(1)

bool is_elf(const unsigned char* const buf, unsigned int bufsize, bool *is_64bit) {
    if (bufsize < EI_NIDENT) { 
        return false;
    }
    bool valid = true;
    if (buf[EI_MAG0] != ELFMAG0) {// EI_MAG0
        valid = false;
    } 
    if (buf[EI_MAG1] != ELFMAG1) { // EI_MAG1
        valid = false;
    } 
    if (buf[EI_MAG2] != ELFMAG2) { // EI_MAG2
        valid= false;
    } 
    if (buf[EI_MAG3] != ELFMAG3) { // EI_MAG3
        valid = false;
    } 
    if (buf[EI_CLASS] == ELFCLASSNONE) {
        valid = false;
    } 
    if (buf[EI_CLASS] == ELFCLASS64) {
        *is_64bit = true;
    } else {
        *is_64bit = false;
    }
    if (buf[EI_VERSION] == EV_NONE) {
        valid = false;
    }
    return valid;
}

void show_elf_header(elf_file *ef)
{
    if(ef->is_64)
    {
        printf("e_ident = %s\n",   ef->e64_hdr.e_ident);
        printf("e_machine = %x\n", ef->e64_hdr.e_machine);
        printf("e_version = %x\n", ef->e64_hdr.e_version);
        printf("e_entry = %x\n",   ef->e64_hdr.e_entry);
        printf("e_phoff = %x\n",   ef->e64_hdr.e_phoff);
        printf("e_shoff = %x\n",   ef->e64_hdr.e_shoff);
        printf("e_flags = %x\n",   ef->e64_hdr.e_flags);
        printf("e_phentsize = %x\n", ef->e64_hdr.e_phentsize);
    }
    else
    {
        printf("e_ident = %s\n",   ef->e32_hdr.e_ident);
        printf("e_machine = %x\n", ef->e32_hdr.e_machine);
        printf("e_version = %x\n", ef->e32_hdr.e_version);
        printf("e_entry = %x\n",   ef->e32_hdr.e_entry);
        printf("e_phoff = %x\n",   ef->e32_hdr.e_phoff);
        printf("e_shoff = %x\n",   ef->e32_hdr.e_shoff);
        printf("e_flags = %x\n",   ef->e32_hdr.e_flags);
        printf("e_phentsize = %x\n", ef->e32_hdr.e_phentsize);
    }
    return;
}

void print_shdr(const Elf32_Shdr * const sh) {
    void print_type (uint32_t a) {
        switch (a) {
            case SHT_NULL:
                printf(" (SHT_NULL)\n");
                break;
            case SHT_PROGBITS:
                printf(" (SHT_PROGBITS)\n");
                break;
            case SHT_SYMTAB:
                printf(" (SHT_SYMTAB)\n");
                break;
            case SHT_STRTAB:
                printf(" (SHT_STRTAB)\n");
                break;
            case SHT_HASH:
                printf(" (SHT_HASH)\n");
                break;
            case SHT_DYNAMIC:
                printf(" (SHT_DYNAMIC)\n");
                break;
            case SHT_NOTE:
                printf(" (SHT_NOTE)\n");
                break;
            case SHT_NOBITS:
                printf(" (SHT_NOBITS)\n");
                break;
            case SHT_SHLIB:
                printf(" (SHT_SHLIB)\n");
                break;
            case SHT_DYNSYM:
                printf(" (SHT_DYNSYM)\n");
                break;
            case SHT_LOUSER:
                printf(" (SHT_NOTE)\n");
                break;
            case SHT_HIUSER:
                printf(" (SHT_NOTE)\n");
                break;
            default:
                if (SHT_LOPROC < a && a < SHT_HIPROC) {
                    printf(" (reserved)\n");
                }
                break;
        }
    }
    if (sh == NULL) {
        printf("print_shdr: null ptr\n");
        return;
    }
    const char *names[] = {
        "sh_name", "sh_type", "sh_flags", "sh_addr", "sh_offset",
        "sh_size", "sh_link", "sh_info", "sh_addralign", "sh_entsize"
    };
    for (unsigned int i = 0; i < 10; ++i) {
        // all attributes in  the 32-bit version are the same type
        uint32_t *x = (uint32_t*)((char*)sh + (sizeof(uint32_t) * i));
        printf("%s = %x", names[i], *x);
        switch (i) {
            default:
                printf("\n");
                break;
            case 1: // sh_type
                print_type(*x);
                break;
        }
    }
}

void print_phdr(const Elf32_Phdr* const ph) {
    if (ph == NULL) {
        return;
    }
    const char *names[] = {
        "p_type", "p_offset", "p_vaddr", "p_paddr",
        "p_filesz", "p_memsz", "p_flags", "p_align"
    };
    for (unsigned int i = 0; i < 8; i++) { // 8 = # of attributes
        uint32_t *x =(uint32_t*)((char*)ph + (sizeof(uint32_t) * i));
        printf("%s = %x\n", names[i], *x);
    }
}

void* init(char * const buf, const unsigned int bufsize, unsigned int offset) {
    if (buf+offset > buf+bufsize) {
        printf("invalid (%x, %x)\n", buf+offset, buf+bufsize);
        return NULL;
    }
    return (buf+offset);
}

void *elf_get_section_header(unsigned char *elf_file, unsigned int len, 
                            unsigned int n) {
    bool is_64bit;
    if (!is_elf(elf_file, len, &is_64bit)) {
        return NULL;
    }
    // to do: use 64 bit elf header if is_64bit
    int shnum;
    int shentsize;
    int shoff;
    if (is_64bit) {
        Elf64_Ehdr *eh;
        eh = (Elf64_Ehdr*)elf_file;
        shnum = eh -> e_shnum;
        shoff = eh -> e_shoff;
        shentsize = eh -> e_shentsize;
    } else {
        Elf32_Ehdr *eh;
        eh = (Elf32_Ehdr*)elf_file;
        shnum = eh -> e_shnum;
        shoff = eh -> e_shoff;
        shentsize = eh -> e_shentsize;
    }
    if (n > shnum) {
        return NULL;
    }
    unsigned int offset = n * shentsize + shoff;
    void *sh = init(elf_file, len, offset);
    // return value may also be null
    return sh;
}

elf_file *elf_open(char *filename)
{
    elf_file *ef;
    FILE *f = fopen(filename, "rb");
    int i;
    
    if (f == NULL) {
        perror("file handler is null ptr");
        return NULL;
    }
    ef = malloc(sizeof(elf_file));
    ef->f = f;
    fread(ef->buf,sizeof(uint8_t),EI_NIDENT,f);
    if(!is_elf(ef->buf,EI_NIDENT,&ef->is_64))
    {
        fprintf(stderr,"not a elf\n");
        free(ef);
        fclose(f);
        return NULL;
    }
    if(ef->is_64)
    {
        fread(&ef->buf[EI_NIDENT],sizeof(uint8_t),sizeof(ef->e64_hdr)-EI_NIDENT,f);
        ef->e64_phdr = malloc(sizeof(Elf64_Phdr) * ef->e64_hdr.e_phnum);
        fseek(f,ef->e64_hdr.e_phoff,SEEK_SET);
        fread(ef->e64_phdr,sizeof(Elf64_Phdr), ef->e64_hdr.e_phnum,f);
        ef->e64_shdr = malloc(sizeof(Elf64_Shdr) * ef->e64_hdr.e_shnum);
        fseek(f,ef->e64_hdr.e_shoff,SEEK_SET);
        fread(ef->e64_shdr,sizeof(Elf64_Shdr), ef->e64_hdr.e_shnum,f);
    }
    else
    {
        fread(&ef->buf[EI_NIDENT],sizeof(uint8_t),sizeof(ef->e32_hdr)-EI_NIDENT,f);
        ef->e32_phdr = malloc(sizeof(Elf32_Phdr) * ef->e32_hdr.e_phnum);
        fseek(f,ef->e32_hdr.e_phoff,SEEK_SET);
        fread(ef->e32_phdr,sizeof(Elf32_Phdr), ef->e32_hdr.e_phnum,f);
        fseek(f,ef->e32_hdr.e_shoff,SEEK_SET);
        fread(ef->e32_shdr,sizeof(Elf32_Shdr), ef->e32_hdr.e_shnum,f);
    }
    
    return ef;
}

int elf_get_number_of_sections(elf_file *ef) {
    int no_of_sections;
    if (ef->is_64) {
        no_of_sections = ef->e64_hdr.e_shnum;
    } else {
        no_of_sections = ef->e32_hdr.e_shnum;
    }
    return no_of_sections;
}

int elf_get_section_flags(elf_file *ef, unsigned int n) {

    int sh_flags;
    if (ef->is_64) {
        sh_flags = ef->e64_shdr[n].sh_flags;
    } else {
        sh_flags = ef->e32_shdr[n].sh_flags;
    }
    return sh_flags;
}

uint64_t elf_get_section_address(elf_file *ef, unsigned int n)
{
    int sh_size;
    if (ef->is_64) {
        sh_size = ef->e64_shdr[n].sh_addr;
    } else {
        sh_size = ef->e32_shdr[n].sh_addr;
    }
    return sh_size;
}

int elf_get_section_size(elf_file *ef, unsigned int n)
{
    int sh_size;
    if (ef->is_64) {
        sh_size = ef->e64_shdr[n].sh_size;
    } else {
        sh_size = ef->e32_shdr[n].sh_size;
    }
    return sh_size;
}

int elf_copy_section_to_array(elf_file *ef, unsigned int n, uint8_t *array) {
    unsigned int offset;
    unsigned int size;
    if (ef->is_64) {
        offset = ef->e64_shdr[n].sh_offset;
        size = ef->e64_shdr[n].sh_size;
    } else {
        offset = ef->e32_shdr[n].sh_offset;
        size = ef->e32_shdr[n].sh_size;
    }
    if (size <= 0) {
        return size; // hits for SHT_NULL or SHT_NOBITS
    }
    fseek(ef->f,offset,SEEK_SET);
    fread(array,sizeof(uint8_t),size,ef->f);
    return size;
}

int elf_close(elf_file *ef)
{
    fclose(ef->f);
    if(ef->is_64)
    {
        free(ef->e64_phdr);
        free(ef->e64_shdr);
    }
    else
    {
        free(ef->e32_phdr);
        free(ef->e32_shdr);
    }
    free(ef);
}

// demo/testing purposes
#ifdef STANDALONE

// print all program and section headers
void test_00(Elf32_Ehdr * eh, char *buffer, unsigned int bufsize) {
    for (unsigned int i = 0; i < eh -> e_phnum; ++i) {
        printf("-- program header %.2i --\n", i);
        unsigned int offset = i * (eh -> e_phentsize) + eh -> e_phoff;
        Elf32_Phdr *p = init(buffer, bufsize, offset);
        print_phdr(p);
        printf("-----------------------\n");
    }
    for (unsigned int i = 0; i < eh -> e_shnum; ++i) {
        printf("-- section header %.2i --\n", i);
        Elf32_Shdr *sample;
        unsigned int offset = i * (eh -> e_shentsize) + eh -> e_shoff;
        sample = init(buffer, bufsize,  offset);
        print_shdr(sample);
        printf("-----------------------\n");
    }
}

void test_01(unsigned char* elf_file, unsigned int len) {
    // test file has 7 sections
    int count = elf_get_number_of_sections(elf_file);
    if (count <= 0) {
        printf("!\n");
        return;
    }
    for (unsigned int i = 0; i < count; i++) {
        int flags = elf_get_section_flags(elf_file, i);
        printf("flag: %x\n", flags);
    }
}

int main(int argc, char ** argv) {
    int n;
    uint64_t addr;
    elf_file *ef;
    if (argc < 2) {
        printf("usage: program filename\n");
        return 0;
    }
    ef = elf_open(argv[1]);
    show_elf_header(ef);
    //test_00(eh, buffer, bufsize);
    //test_01(buffer, bufsize);
    uint8_t *buff = NULL;
    for(n = 0;n < elf_get_number_of_sections(ef); n++)
    {
        buff = realloc(buff,elf_get_section_size(ef,n));
        addr = elf_get_section_address(ef,n);
        int c = elf_copy_section_to_array(ef,n,buff);
        printf("Section at address %016X:\n",addr);
        for (unsigned int i=0; i < c; i++) {
            printf("%x, ", buff[i]);
        }
        printf("\n");
    }

    return 0;
}
# endif
