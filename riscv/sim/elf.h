#include <stdbool.h>
#include <elf.h>

typedef struct
{
    FILE *f;
    bool is_64;
    union
    {
        Elf32_Ehdr e32_hdr;
        Elf64_Ehdr e64_hdr;
        uint8_t buf[0];
    };
    union
    {
        Elf32_Phdr *e32_phdr;
        Elf64_Phdr *e64_phdr;
    };
    union
    {
        Elf32_Shdr *e32_shdr;
        Elf64_Shdr *e64_shdr;
    };
} elf_file;

elf_file *elf_open(char *filename);
int elf_get_number_of_sections(elf_file *ef);
int elf_get_section_flags(elf_file *ef, unsigned int n);
int elf_get_section_size(elf_file *ef, unsigned int n);
int elf_copy_section_to_array(elf_file *ef, unsigned int n, uint8_t *array);
int elf_close(elf_file *ef);