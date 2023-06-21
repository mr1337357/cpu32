#include <stdint.h>

uint32_t **segment_table;

uint32_t page_table = 0;


void mem_init()
{
}

void mem_add_segment(uint32_t start, uint32_t size)
{
    