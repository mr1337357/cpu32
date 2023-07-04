#include <stdint.h>

uint32_t registers[32];

uint32_t execute(uint32_t instruction)
{
	return instruction << 1;
}
