PREFIX=riscv64-linux-gnu-
export CC=${PREFIX}gcc
export LD=${PREFIX}ld
export OD=${PREFIX}objdump


export CFLAGS="-g -static"

cd app/

for prog in hello_world
do
  make $prog.o
  make $prog
  $OD -S $prog > $prog.dis
done
cd ..

PREFIX=riscv32-unknown-linux-gnu-
export CC=${PREFIX}gcc
export LD=${PREFIX}ld
export OD=${PREFIX}objdump

export CFLAGS="-nostdlib -march=rv32i -mabi=ilp32"
export LDFLAGS="-nostdlib -march=rv32i -mabi=ilp32"

cd native/
for prog in add math
do
  make $prog.o
  make $prog
  $OD -S $prog > $prog.dis
done
