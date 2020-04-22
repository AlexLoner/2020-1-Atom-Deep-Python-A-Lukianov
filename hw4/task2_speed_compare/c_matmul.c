#include <stdio.h>
#include <stdlib.h>
int mtx()
{
    int m, n, p, q, c, d, k, sum = 0;
    int first[6][6] =    {{1, 1, 1, 1, 1, 1},
                            {2, 2, 2, 2, 2, 2},
                            {3, 3, 3, 3, 3, 3},
                            {4, 4, 4, 4, 4, 4},
                            {5, 5, 5, 5, 5, 5},
                            {6, 6, 6, 6, 6, 6}};
    int second[6][6] =   {{1, 1, 1, 1, 1, 1},
                            {2, 2, 2, 2, 2, 2},
                            {3, 3, 3, 3, 3, 3},
                            {4, 4, 4, 4, 4, 4},
                            {5, 5, 5, 5, 5, 5},
                            {6, 6, 6, 6, 6, 6}};

    int multiply[6][6];
    for (c = 0; c < 6; c++) {
        for (d = 0; d < 6; d++) {
            for (k = 0; k < 6; k++) {
                sum = sum + first[c][k]*second[k][d];
            }
            multiply[c][d] = sum;
            sum = 0;
        }
    }

    printf("Product of the matrices:\n");

    for (c = 0; c < 6; c++) {
        for (d = 0; d < 6; d++) {
            printf("%d\t", multiply[c][d]);
        }
        printf("\n");
    }

  return 0;
}