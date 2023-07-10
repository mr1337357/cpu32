#include <stdio.h>
#include <unistd.h>
#include <getopt.h>

#include "cpu.h"

static struct option long_options[] = 
{
    {"arch", required_argument, 0, 'a'},
    {"mode", required_argument, 0, 'm'},
};

uint64_t architecture = RV32I;

void parse_architecture(char *archstring)
{
    printf("%s\n",archstring);
}

int main(int argc,char **argv)
{
    int c;
    int option_index;
    while(1)
    {
        c = getopt_long(argc,argv, "a:m:", long_options, &option_index);
        if(c == -1)
        {
            break;
        }
        switch(c)
        {
            case 0:
                switch(option_index)
                {
                    case 0:
                        parse_architecture(optarg);
                        break;
                    case 1:
                        //todo
                        break;
                }
                break;
            case 'a':
                parse_architecture(optarg);
                break;
        }
    }
    return 0;
}