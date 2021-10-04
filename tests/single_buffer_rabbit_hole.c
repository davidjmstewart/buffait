#include <stdlib.h>
#define BUFF_SIZE 100

int main(int argc, char *argv[])
{
    int j = atoi(argv[1]);
    int *intArray = malloc(4 * sizeof(int));
    intArray[1] = j;
    char *buf = malloc(intArray[1] * sizeof(char));
    buf[4] = 10; // unknown if this is an overflow because the size of buf depends on user input
    return 0;
}