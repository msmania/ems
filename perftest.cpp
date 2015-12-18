#include <stdlib.h>
#include <stdio.h>
#include <vector>
#include <valarray>
#include <Eigen/Dense>
#include "common.h"

template<class T>
void dumpVector(const T &v) {
#ifdef LOG
    putchar('[');
    for (auto c : v) {
        printf(" %.3f", c);
    }
    puts(" ]\n");
#endif
}

#ifdef _AVX
namespace avx {
#else
namespace noavx {
#endif

void TestVector(int size, int repeat) {
    std::vector<double> v1(size * 2);
    std::vector<double> v2(size * 2);
    int i, j;
    for (i = 0 ; i < size * 2 ; ++i) {
        v1[i] = distribution(generator);
        v2[i] = distribution(generator);
    }
    dumpVector<std::vector<double> >(v1);
    dumpVector<std::vector<double> >(v2);
    g_Timer.Start("std::vector  ");
    for (i = 0; i < repeat ; ++i) {
        double d = distribution(generator) * 4 - 2;
        for (j = 0; j < size * 2; ++j) {
            v1[j] += d * v2[j];
        }
    }
    g_Timer.Stop();
    dumpVector<std::vector<double> >(v1);
}

void TestValArray(int size, int repeat) {
    std::valarray<double> v1(size * 2);
    std::valarray<double> v2(size * 2);
    int i;
    for (i = 0 ; i < size * 2 ; ++i) {
        v1[i] = distribution(generator);
        v2[i] = distribution(generator);
    }
    dumpVector<std::valarray<double> >(v1);
    dumpVector<std::valarray<double> >(v2);
    g_Timer.Start("std::valarray");
    for (i = 0; i < repeat ; ++i) {
        double d = distribution(generator) * 4 - 2;
        v1 += d * v2;
    }
    g_Timer.Stop();
    dumpVector<std::valarray<double> >(v1);
}

void TestEigen(int size, int repeat) {
    Eigen::MatrixXd v1(size, 2);
    Eigen::MatrixXd v2(size, 2);
    v1.setRandom();
    v2.setRandom();
    g_Timer.Start("Eigen::Matrix");
    for (int i = 0; i < repeat ; ++i) {
        double d = distribution(generator) * 4 - 2;
        v1 += d * v2;
    }
    g_Timer.Stop();
}

} // namespace