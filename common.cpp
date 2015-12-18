#include <string>
#include <random>
#include "common.h"

std::default_random_engine generator;
std::uniform_real_distribution<double> distribution(0.0, 1.0);

void Timer::Start(const char *name) {
    _name = name;
    _start = clock();
}

void Timer::Stop() {
    _result = double(clock() - _start) / CLOCKS_PER_SEC;
    if (_print) {
        printf("%s time = %.3f (s)\n", _name, _result);
    }
}