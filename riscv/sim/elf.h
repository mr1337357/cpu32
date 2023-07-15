#include <stdbool.h>
#include <elf.h>

typedef struct elf_file elf_file;

elf_file *elf_open(char *filename);
int elf_get_number_of_sections(elf_file *ef);
int elf_get_section_flags(elf_file *ef, unsigned int n);
uint64_t elf_get_section_address(elf_file *ef, unsigned int n);
int elf_get_section_size(elf_file *ef, unsigned int n);
int elf_copy_section_to_array(elf_file *ef, unsigned int n, uint8_t *array);
int elf_close(elf_file *ef);