typedef enum
{
    MEM_OK,
    MEM_INVALID,
    MEM_NOREAD,
    MEM_NOWRITE,
    MEM_NOEXEC,
} MEM_STATUS;

#define MEM_RD 4
#define MEM_WR 2
#define MEM_EX 1

int mem_init();
int mem_make_segment(uint64_t start,uint64_t size,uint64_t permissions);
uint8_t *mem_get_segment_ptr(uint64_t address);
int mem_phys_read_8(uint64_t address,uint8_t *data,uint8_t access);
int mem_phys_write_8(uint64_t address,uint8_t *data, uint8_t access);