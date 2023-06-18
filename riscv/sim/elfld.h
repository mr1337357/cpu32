typedef struct _elfdata_private elfdata_private;
typedef struct 
{
    int fd;
    elfdata_private *private;
} elf_file;