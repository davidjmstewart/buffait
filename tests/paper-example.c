#include <stdlib.h>
#define BUFF_SIZE 100

int main(int argc, char *argv[])
{
    char buf[BUFF_SIZE], *buf2;
    int n = BUFF_SIZE, i;

    if (argc != 3)
    {
        printf("Usage: prog_name length_of_data data\n");
        exit(-1);
    }

    for (i = 1; i <= n; i++)
    {
        buf[i] = 'A';
    }

    buf[n] = '\0';
    n = atoi(argv[1]);
    buf2 = (char *)malloc(n);
    
    for (i = 0; i <= n; i++)
    {
        buf2[i] = argv[2][i];
    }
    return 0;
}