
#include <stdlib.h>
#include <stdio.h>
#include <stdint.h>

#include <stdbool.h>

// https://www.man7.org/linux/man-pages/man5/elf.5.html
#include <elf.h>

// #pragma pack(1)

bool is_elf(const unsigned char* const buf, unsigned int bufsize, bool *is_64bit) {
    if (bufsize < EI_NIDENT) { 
        return false;
    }
    bool valid = true;
    if (buf[0] != 0x7f) {// EI_MAG0
        valid = false;
    } else if (buf[1] != 'E') { // EI_MAG1
        valid = false;
    } else if (buf[2] != 'L') { // EI_MAG2
        valid= false;
    } else if (buf[3] != 'F') { // EI_MAG3
        valid = false;
    } else if (buf[EI_CLASS] == ELFCLASSNONE) {
        valid = false;
    } else if (buf[EI_CLASS] == ELFCLASS64) {
        *is_64bit = true;
    } else if (buf[EI_VERSION] == EV_NONE) {
        valid = false;
    }
    return valid;
}

void show_elf_header (Elf32_Ehdr* eh) {
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

int elf_get_number_of_sections(unsigned char* elf_file, unsigned int len) {
    bool is_64bit;
    if (!is_elf(elf_file, len, &is_64bit)) {
        return -1;
    }
    // to do: use 64 bit elf header if is_64bit
    Elf32_Ehdr *eh;
    eh = (Elf32_Ehdr*)elf_file;
    int no_of_sections = eh -> e_shnum;
    return no_of_sections;
}

int elf_get_sh_flags(unsigned char *elf_file, unsigned int len, unsigned int n) {
    bool is_64bit;
    if (!is_elf(elf_file, len, &is_64bit)) {
        return -1;
    }
    // to do: use 64 bit elf header if is_64bit
    Elf32_Ehdr *eh;
    Elf32_Shdr *section_header;
    eh = (Elf32_Ehdr*)elf_file;
    if (n > (eh -> e_shnum)) {
        return -1;
    }
    unsigned int offset = n * (eh -> e_shentsize) + eh -> e_shoff;
    section_header = init(elf_file, len, offset);
    if (section_header == NULL) {
        return -1;
    }
    int sh_flags = section_header ->  sh_flags;
    return sh_flags;
}

int elf_copy_section_to_array(int section_no, uint8_t *array) {
    // assume  array has not been allocated and will be freed by  callee
    return 0;
}


// demo/testing purposes
#ifdef STANDALONE
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
    int count = elf_get_number_of_sections(elf_file, len);
    if (count < 0) {
        return;
    }
    for (unsigned int i = 0; i < count; i++) {
        int flags = elf_get_sh_flags(elf_file, len, i);
        printf("flag: %x\n", flags);
    }
}

int main(int argc, char ** argv) {
    if (argc < 2) {
        printf("usage: program filename\n");
        return 0;
    }
    unsigned int bufsize = 0;
    char *f      = argv[1];
    char *buffer = loadfile(f, &bufsize);
    bool is_64;
    if (!is_elf(buffer, bufsize, &is_64)) {
        return 0;
    }
    Elf32_Ehdr *eh;
    eh = (Elf32_Ehdr*)buffer;
    show_elf_header(eh);
    test_00(eh, buffer, bufsize);
    test_01(buffer, bufsize);
    free(buffer);
    return 0;
}
# endif
