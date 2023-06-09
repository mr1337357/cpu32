export CC=riscv64-linux-gnu-gcc
export LD=riscv64-linux-gnu-ld
export OD=riscv64-linux-gnu-objdump

export CFLAGS="-g"
#export CFLAGS="-march=rv32i -mabi=ilp32"

for prog in hello_world
do
  make $prog
  $OD -S $prog > $prog.dis
done
