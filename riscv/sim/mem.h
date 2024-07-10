#ifndef __MEM_H__
#include "cpu.h"

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
int mem_read_bytes(uint64_t address, void *data, uint8_t len, uint8_t access, csr_struct *csr);
int mem_write_bytes(uint64_t address, void *data, uint8_t len, uint8_t access, csr_struct *csr);
void mem_dump();

#define __MEM_H__
#endif //__MEM_H__