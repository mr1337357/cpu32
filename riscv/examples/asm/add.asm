.org 0x8000
.globl _start
_start:
    addi sp,sp,-48
    sw   s0,44(sp)
    addi s0,sp,48
    sw   a0,-36(s0)
    sw   a1,-40(s0)
    li   a5,1
    sw   a5,-20(s0)
    li   a5,2
    sw   a5,-24(s0)
    lw   a4,-20(s0)
    lw   a5,-24(s0)
    add  a5,a4,a5
    sw   a5,-28(s0)
    li   a5,0
    mv   a0,a5
    lw   s0,44(sp)
    addi sp,sp,48
    ret
