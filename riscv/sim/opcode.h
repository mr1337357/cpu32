typedef struct
{
} opcode_info;

//R I S B U J
#define OP(inst)  ((inst >>  0) & 0x00007F)
//R I U J
#define RD(inst)  ((inst >>  7) & 0x00001F)
// R I S B
#define RS1(inst) ((inst >> 15) & 0x00001F)
// R S B
#define RS2(inst) ((inst >> 20) & 0x00001F)
// R I S B
#define FN3(inst) ((inst >> 12) & 0x000007)
// R
#define FN7(inst) ((inst >> 25) & 0x00007F)
// I
#define IIM(inst) ((inst >> 20) & 0x000FFF)
// S
#define SI(inst) (((inst >>  7) & 0x00001F)|((inst >> 20) & 0x00000000))
// B
#define SI2(inst) ((inst >> 25) & 0x00001F)
#define UIM(inst) ((inst >> 12) & 0x0FFFFF)