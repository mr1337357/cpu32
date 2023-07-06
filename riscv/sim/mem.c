#include <stdio.h>
#include <stdint.h>

#include "mem.h"

struct mem_segment
{
    uint64_t start;
    uint64_t end;
    uint8_t permissions;
    uint8_t *memory;
};

int num_segments = 0;
struct mem_segment *memory = 0;

int mem_make_segment(uint64_t start,uint64_t size)
{
    struct mem_segment *newsegment;
    //TODO: check for overlaps and reject
    memory = realloc(memory,++num_segments * sizeof(mem_segment));
    newsegment = &memory[num_segments-1];
    newsegment->start = start;
    newsegment->end = start+size - 1;
    newsegment->memory = malloc(size);
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