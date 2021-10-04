#include <stdlib.h>
#define BUFF_SIZE 100

int main(int argc, char *argv[])
{
    char buf[BUFF_SIZE];
    int i = 0;
    buf[99 + i] = 0; // valid
    i = 1; // we do not support i++ which requires a more stateful approach to parsing 
    buf[99 + i] = 0; // INVALID we have overrun the buffer

    return 0;
}