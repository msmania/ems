#include <stdio.h>
#include <stdlib.h>
#include <vector>
#include <random>
#include "common.h"

#define COUNT_OF(x) ((sizeof(x)/sizeof(0[x])) / ((size_t)(!(sizeof(x) % sizeof(0[x])))))

Timer g_Timer(false);

int main(int argc, char *argv[]) {
    if (argc > 3) {
        int size = atoi(argv[1]);
        int repeat = atoi(argv[2]);
        int n = atoi(argv[3]);

        typedef void (*TESTER)(int, int);
        TESTER Testers[] = {
            avx::TestVector,
            avx::TestValArray,
            avx::TestEigen,
            noavx::TestVector,
            noavx::TestValArray,
            noavx::TestEigen
        };

        double *results = new double[n * COUNT_OF(Testers)];
        if (results) {
            int i, j, cnt = 0;
            for (i = 0; i < n + 1; ++i) {
                printf("# Starting #%d\n", i);
                fflush(stdout);
                for (auto Tester : Testers) {
                    Tester(size, repeat);
                    if (i == 0) continue; // discard the first result
                    double d = (double)g_Timer;
                    results[cnt++] = d;
                }
            }
            for (i = 0; i < (int)COUNT_OF(Testers); ++i) {
                for (j = 0; j < n; ++j) {
                    int idx = i + j * COUNT_OF(Testers);
                    printf(" % 3.4f", results[idx]);
                }
                putchar('\n');
            }
            delete [] results;            
        }
    }
    else {
        printf("usage: runc <size> <repeat> <N>\n");
    }
    exit(0);
}
