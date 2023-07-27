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
int mem_make_segment(uint64_t start,uint64_t size,uint8_t permissions);
uint8_t *mem_get_segment_ptr(uint64_t address);
int mem_read_bytes(uint64_t address, void *data, uint8_t len, uint8_t access);
int mem_write_bytes(uint64_t address, void *data, uint8_t len, uint8_t access);
void mem_dump();