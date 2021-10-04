#include <stdlib.h>
#define BUFF_SIZE 3

int main(int argc, char *argv[])
{
    char buf[BUFF_SIZE];
    for (int i = 0; i <= BUFF_SIZE; i++) {
        buf[i] = 3; // buffer overflow will happen on the last iteration, where we do buf[3] = 3;
    }
    return 0;
}