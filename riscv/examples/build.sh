PREFIX=riscv64-linux-gnu-
export CC=${PREFIX}gcc
export LD=${PREFIX}ld
export OD=${PREFIX}objdump


export CFLAGS="-g -march=rv64id -mabi=lp64d"
export LDFLAGS="-march=rv64id -mabi=lp64d"

rm app/*.o
rm native/*.o

cd app/

for prog in hello_world hello_puts
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
for prog in add math calls
do
  make $prog.o
  make $prog
  $OD -S $prog > $prog.dis
done
cd ..

export AS=${PREFIX}as
cd asm/
for prog in add os gamut
do
  ${AS} ${prog}.asm -o ${prog}.o
  ${LD} ${prog}.o -o ${prog}
done
