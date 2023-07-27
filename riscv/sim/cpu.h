typedef struct
{
    uint32_t mask;
    uint32_t opcode;
    void *extradata;
} instruction;

typedef struct
{
    uint64_t satp;
} csr_struct;

typedef struct cpu cpu;

#define RV32I (1<< 0)
#define RV64I (1<< 1)
#define ZIFEN (1<< 2)
#define ZICSR (1<< 3)
#define RV32M (1<< 4)
#define RV64M (1<< 5)
#define RV32A (1<< 6)
#define RV64A (1<< 7)
#define RV32C (1<< 8)
#define RV64C (1<< 9)

int cpu_step(cpu *c);