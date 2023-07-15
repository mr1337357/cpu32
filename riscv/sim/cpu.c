#include <stdint.h>
#include "cpu.h"

int64_t pc;

uint64_t ir;

uint64_t isa;

int64_t registers[32];

instruction rv32i[] =
{
    { 0x0000007f, 0x00000037, }, //lui
    { 0x0000007f, 0x00000017, }, //auipc
    { 0x0000007f, 0x0000006f, }, //jal
    { 0x0000707f, 0x00000067, }, //jalr
    { 0x0000707f, 0x00000063, }, //beq
    { 0x0000707f, 0x00001063, }, //bne 
    { 0x0000707f, 0x00004063, }, //blt
    { 0x0000707f, 0x00005063, }, //bge
    { 0x0000707f, 0x00006063, }, //bltu 
    { 0x0000707f, 0x00007063, }, //bgeu 
    { 0x0000707f, 0x00000003, }, //lb 
    { 0x0000707f, 0x00001003, }, //lh   
    { 0x0000707f, 0x00002003, }, //lw  
    { 0x0000707f, 0x00004003, }, //lbu
    { 0x0000707f, 0x00005003, }, //lhu  
    { 0x0000707f, 0x00000023, }, //sb  
    { 0x0000707f, 0x00001023, }, //sh 
    { 0x0000707f, 0x00002023, }, //sw 
    { 0x0000707f, 0x00000013, }, //addi 
    { 0x0000707f, 0x00002013, }, //slti 
    { 0x0000707f, 0x00003013, }, //sltiu
    { 0x0000707f, 0x00004013, }, //xori 
    { 0x0000707f, 0x00006013, }, //ori  
    { 0x0000707f, 0x00007013, }, //andi 
    { 0xf800707f, 0x00001013, }, //slli 
    { 0xf800707f, 0x00005013, }, //srli 
    { 0xf800707f, 0x40005013, }, //srai 
    { 0xfe00707f, 0x00000033, }, //add  
    { 0xfe00707f, 0x40000033, }, //sub 
    { 0xfe00707f, 0x00001033, }, //sll 
    { 0xfe00707f, 0x00002033, }, //slt  
    { 0xfe00707f, 0x00003033, }, //sltu 
    { 0xfe00707f, 0x00004033, }, //xor 
    { 0xfe00707f, 0x00005033, }, //srl 
    { 0xfe00707f, 0x40005033, }, //sra 
    { 0xfe00707f, 0x00006033, }, //or   
    { 0xfe00707f, 0x00007033, }, //and 
    { 0x0000707f, 0x0000000F, }, //fence
    { 0xFFFFFFFF, 0x00000073, }, //ecall
    { 0xFFFFFFFF, 0x00100073, }, //ebreak
};

int decode()
{
}

int execute()
{
}

int fetch()
{
    int status;
    status = mem_read_32(pc,&ir,MEM_EX);
}