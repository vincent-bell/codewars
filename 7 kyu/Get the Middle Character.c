#include <string.h>

char *get_middle(char outp[3], const char *inp)
{
    unsigned inp_len = strlen(inp);
    if ( inp_len % 2 == 0 ) {
        char c1 = inp[inp_len / 2 - 1];
        char c2 = inp[inp_len / 2];
        outp[0] = c1;
        outp[1] = c2;
        outp[2] = '\0';
    }
    else {
        outp[0] = inp[inp_len / 2],
        outp[1] = '\0';
    }

    return outp;
}
