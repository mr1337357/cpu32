
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#pragma pack(1)
#define EI_NIDENT 16
typedef uint32_t ElfN_Addr;
typedef uint32_t ElfN_Off; 
// https://www.man7.org/linux/man-pages/man5/elf.5.html
struct ElfHeader {
    unsigned char e_ident[EI_NIDENT];
    uint16_t      e_type;
    uint16_t      e_machine;
    uint32_t      e_version;
    ElfN_Addr     e_entry;
    ElfN_Off      e_phoff;
    ElfN_Off      e_shoff;
    uint32_t      e_flags;
    uint16_t      e_ehsize;
    uint16_t      e_phentsize;
    uint16_t      e_phnum;
    uint16_t      e_shentsize;
    uint16_t      e_shnum;
    uint16_t      e_shstrndx;
};

void show_elf_header (struct ElfHeader* eh) {
    printf("e_ident = %s\n", eh -> e_ident);
    printf("e_machine = %x\n", eh -> e_machine);
    printf("e_version = %x\n", eh -> e_version);
    printf("e_entry = %x\n", eh -> e_entry);
    printf("e_phoff = %x\n", eh -> e_phoff);
    printf("e_shoff = %x\n", eh -> e_shoff);
    printf("e_flags = %x\n", eh -> e_flags);
    printf("e_phentsize = %x\n", eh -> e_phentsize);
    return;
}

// mostly copy and paste
struct Elf32_SectionHeader {
    uint32_t   sh_name;
    uint32_t   sh_type;
    uint32_t   sh_flags;
    // Elf32_Addr sh_addr;
    uint32_t  sh_addr;
    // Elf32_Off  sh_offset;
    uint32_t   sh_offset;
    uint32_t   sh_size;
    uint32_t   sh_link;
    uint32_t   sh_info;
    uint32_t   sh_addralign;
    uint32_t   sh_entsize;
};

void show_section_header (struct Elf32_SectionHeader *sh) {
    if (sh == NULL) {
        printf("show_section_header: null ptr\n");
        return;
    }
    printf("sh_addr = %x\n", sh -> sh_addr);
    printf("sh_offset = %x\n", sh -> sh_offset);
    printf("sh_size = %x\n", sh -> sh_size);
}

// generic, load any binary file
char *loadfile(const char *fname, unsigned int *s) {
    FILE *f           = fopen(fname, "rb");
    unsigned int size = 0; // number of elements to buffer;
    unsigned int rcnt = 0; // number of char's read by fread(...)
    if (f == NULL) {
        perror("file handler is null ptr");
        return NULL;
    }
    // this method of determining file size works up to 2 GB.
    fseek(f, 0, SEEK_END);
    size = ftell(f);
    rewind(f);
    char *buf = (char*)malloc(sizeof(char) * size);
    if (buf == NULL) {
        perror("buf is null after malloc");
        free(buf);
        return NULL;
    }
    rcnt = fread(buf, sizeof(char), size, f);
    if (rcnt < size) {
        perror("read count < size");
        free(buf);
        return NULL;
    }
    fclose(f);
    *s = rcnt;
    return buf;
}

struct ELF32_SectionHeader*
get_section_header(struct ElfHeader *eh, unsigned int i, unsigned int memsize) {
    struct Elf32_SectionHeader *sh;
    if (i > eh -> e_shnum) {
        perror("i exceeds eh -> e_shnum");
        return NULL;
    }
    char *mem = eh;
    unsigned int ith_offset = i * (eh -> e_shentsize);
    sh = mem + (eh -> e_shoff) + ith_offset;
    if (sh > mem+memsize) {
        printf("%x, %x\n", sh, memsize);
        perror("warning: potential segmentation fault ahead");
    }
    return sh;
}

#ifdef __ELF_STANDALONE__

int main(int argc, char ** argv) {
    if (argc < 2) {
        printf("usage: program filename\n");
        return;
    }
    char *f = argv[1];
    unsigned int bufsize = 0;
    char *buffer         = loadfile(f, &bufsize);
    struct ElfHeader *eh;
    eh = buffer;
    show_elf_header(eh);
    for (unsigned int i = 0; i < eh -> e_shnum; ++i) {
        printf("-- section header %.2i --\n", i);
        // struct Elf32_SectionHeader *sh;
        // unsigned int ith_offset = i * (eh -> e_shentsize);
        // printf("%x, %x\n", buffer+ith_offset, eh+ith_offset);
        struct Elf32_SectionHeader *sample;
        sample = get_section_header(eh, i, bufsize);
        // sh = buffer + (eh -> e_shoff) + ith_offset;
        show_section_header(sample);
        printf("-----------------------\n");
    }
    free(buffer);
    return 0;
}

#endif //__ELF_STANDALONE__