unsigned int registers[32];

unsigned int pc;

#define OP(inst)  ((inst >>  0) & 0x00007F)
#define RD(inst)  ((inst >>  7) & 0x00001F)
#define FN3(inst) ((inst >> 12) & 0x000007)
#define RS1(inst) ((inst >> 15) & 0x00001F)
#define RS2(inst) ((inst >> 20) & 0x00001F)
#define FN7(inst) ((inst >> 25) & 0x00007F)
#define IIM(inst) ((inst >> 20) & 0x000FFF)
#define SI1(inst) ((inst >>  7) & 0x00001F)
#define SI2(inst) ((inst >> 25) & 0x00001F)
#define UIM(inst) ((inst >> 12) & 0x0FFFFF)

