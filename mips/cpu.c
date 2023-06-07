#include <stdio.h>

unsigned int registers[16];

unsigned int ir[5];

unsigned int pc = 0x0000;

#define OP(x) ((x>>26)&0x3F)
#define FUNC(x) ((x>>0)&0x3F)

int isWrite(unsigned int instruction)
{
	switch(OP(instruction))
	{
		case 0x00: //maths
		case 0x08: //addi
		case 0x09: //addiu
		case 0x0A: //slti
		case 0x0B: //sltiu
		case 0x0C: //andi
		case 0x0D: //ori
		case 0x0F: //lui
		case 0x10: //mfc0
		case 0x20: //lb
		case 0x23: //lw
		case 0x24: //lbu
		case 0x25: //lhu
			return 1;
	}
	return 0;
}

int isMem(unsigned int instruction)
{
	switch(OP(instruction))
	{
		case 0x20: //lb
		case 0x23: //lw
		case 0x24: //lbu
		case 0x25: //lhu
		case 0x28: //sb
		case 0x29: //sh
		case 0x2B: //sw
			return 1;
	}
	return 0;
}

int isMath(unsigned int instruction)
{
	switch(OP(instruction))
	{
		case 0x00: //maths
		case 0x08: //addi
		case 0x09: //addiu
		case 0x0A: //slti
		case 0x0B: //sltiu
		case 0x0C: //andi
		case 0x0D: //ori
		case 0x0F: //lui (maybe??)
			return 1;
	}
	return 0;
}

int isRead(unsigned int instruction)
{
	switch(OP(instruction))
	{
		case 0x00: //maths
		case 0x08: //addi
		case 0x09: //addiu
		case 0x0A: //slti
		case 0x0B: //sltiu
		case 0x0C: //andi
		case 0x0D: //ori
		case 0x28: //sb
		case 0x29: //sh
		case 0x2B: //sw
			return 1;
	}
	return 0;
}

int isFetch(unsigned int instruction)
{
	return 1;
}

void step()
{
	int i;
	for(i=0;i<4;i++)
	{
		ir[i+1] = ir[i];
	}
	if(isWrite(ir[4])
	{
		//register write
	}
	if(isMem(ir[3])
	{
		//memory stuff
	}
	if(isMath(ir[2])
	{
		//do math
	}
	if(isRead(ir[1])
	{
		//register read
	}
	if(isFetch(ir[0])
	{
		//fetch
		ir[0] = memRead(pc);
		pc += 4;
	}
}