#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

#include "mem.h"

struct mem_segment
{
    uint64_t start;
    uint64_t end;
    uint64_t length;
    uint8_t permissions;
    uint8_t *memory;
};

//LOCALS
static int num_segments = 0;
static struct mem_segment *memory = 0;

//CSRs
#define SATP_MODE (satp>>60)
#define SATP_ASID ((satp>>44)&0xFFFF)
#define SATP_PPN  ((satp>>0)&0xFFFFFFFFFFF)

int mem_init()
{
    num_segments = 0;
    memory = 0;
}

int mem_make_segment(uint64_t start,uint64_t size,uint8_t permissions)
{
    struct mem_segment *newsegment;
    //TODO: check for overlaps and reject
    memory = realloc(memory,++num_segments * sizeof(struct mem_segment));
    newsegment = &memory[num_segments-1];
    newsegment->start = start;
    newsegment->end = start+size - 1;
    newsegment->length = size;
    newsegment->memory = malloc(size);
    newsegment->permissions = permissions;
    return 0;
}

uint8_t *mem_get_segment_ptr(uint64_t address)
{
    int i;
    for(i=0;i<num_segments;i++)
    {
        if(memory[i].start == address)
        {
            return memory[i].memory;
        }
    }
    return 0;
}

void *mem_get_phys_ptr(uint64_t address)
{
    uint64_t offset;
    int i;
    for(i=0;i<num_segments;i++)
    {
        if(memory[i].start <= address && memory[i].end >= address)
        {
            break;
        }
    }
    if(i==num_segments)
    {
        return 0;
    }
    offset = address - memory[i].start;
    return &memory[i].memory[offset];
}

int mem_read_bytes(uint64_t address, void *data, uint8_t len, uint8_t access)
{
    uint8_t *dptr = data;
    uint8_t *ptr = 0;
    int i;
    if(SATP_MODE == 0x08) //39 bit virtual memory
    {
        
    }
    else
    {
        ptr = mem_get_phys_ptr(address);
    }
    if(ptr != NULL)
    {
        for(i=0;i<len;i++)
        {
            dptr[i] = ptr[i];
        }
        return MEM_OK;
    }
    return MEM_INVALID;
}

int mem_write_bytes(uint64_t address, void *data, uint8_t len, uint8_t access)
{
    uint8_t *dptr = data;
    uint8_t *ptr = 0;
    int i;
    if(SATP_MODE == 0x08) //39 bit virtual memory
    {
        
    }
    else
    {
        ptr = mem_get_phys_ptr(address);
    }
    if(ptr != NULL)
    {
        for(i=0;i<len;i++)
        {
            ptr[i] = dptr[i];
        }
        return MEM_OK;
    }
    return MEM_INVALID;
}

void mem_dump()
{
    int i;
    int j;
    for(i=0;i<num_segments;i++)
    {
        printf("%s %s\n",(memory[i].permissions&MEM_WR)?"WR":"  ",(memory[i].permissions&MEM_EX)?"EX":"  ");
        for(j=0;j<memory[i].length;j++)
        {
            if((j&15) == 0)
            {
                printf("\n%016X: ",memory[i].start+j);
            }
            printf("%02hhX ",memory[i].memory[j]);
        }
        printf("\n");
    }
}