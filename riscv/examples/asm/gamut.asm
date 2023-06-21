.globl _start
func:
  addi sp, sp, -16
  sw ra, 12(sp)
  sw s0, 8(sp)
  addi s0, sp, 16
  nop
  lw s0, 8(sp)
  lw ra, 12(sp)
  addi sp, sp, 16
  jalr zero, 0(ra)

mem:
  addi sp, sp, -16
  sw ra, 12(sp)
  sw s0, 8(sp)
  addi s0, sp, 16
  li a1, 5
  sb a1, 4(sp)
  sh a1, 0(sp)
  lw ra, 12(sp)
  ret

_start:
  li a0, 0x8675309
  jal func
  beq a0, ra, func
  bne a0, a0, func
  blt a0, a0, func
  bge a0, a0, func
  bltu a0, a0, func
  bgeu a0, a0, func
  jal mem
  add a0, a1, a2
  sub a0, a1, a2
  xor a0, a1, a2
  or a0, a1, a2
  and a0, a1, a2
  sll a0, a1, a2
  srl a0, a1, a2
  sra a0, a1, a2
  slt a0, a1, a2
  sltu a0, a1, a2
  addi a0, a1, 5
  xori a0, a1, 5
  ori a0, a1, 5
  andi a0, a1, 5
  slli a0, a1, 5
  srli a0, a1, 5
  srai a0, a1, 5
  slti a0, a1, 5
  sltiu a0, a1, 5
  ret
