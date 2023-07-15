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

int num_segments = 0;
struct mem_segment *memory = 0;

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

int mem_phys_read_8(uint64_t address,uint8_t *data,uint8_t access)
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
        return MEM_INVALID;
    }
    if(!(access & memory[i].permissions))
    {
        return access == MEM_RD? MEM_NOREAD : MEM_NOEXEC;
    }
    offset = address - memory[i].start;
    *data = memory[i].memory[offset];
    return MEM_OK;
}

int mem_phys_write_8(uint64_t address,uint8_t *data, uint8_t access)
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
        return MEM_INVALID;
    }
    if(!(access & memory[i].permissions))
    {
        return access == MEM_NOWRITE;
    }
    offset = address - memory[i].start;
    memory[i].memory[offset] = *data;
    return MEM_OK;
}
int mem_virt_read_32(uint64_t address,uint32_t *data, uint8_t access)
{
    return MEM_OK;
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