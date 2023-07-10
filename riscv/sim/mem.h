typedef enum
{
    MEM_OK,
    MEM_INVALID,
    MEM_NOREAD,
    MEM_NOWRITE,
    MEM_NOEXEC,
} MEM_STATUS;

#define MEM_RD 4
#define MEM_WR 2
#define MEM_EX 1
