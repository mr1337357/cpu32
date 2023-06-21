#include <stdint.h>
#include "opcode.h"

uint32_t pc;
uint32_t ir;

uint32_t priv;

uint32_t regs[32];

int fetch()
{
    ir = mem_ld(pc,priv,MEM_EXEC);
}