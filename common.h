class Timer {
private:
    const char *_name;
    clock_t _start;
    double _result;
    bool _print;

public:
    Timer(bool print) : _print(print) {}
    ~Timer() {}
    void Start(const char *name);
    void Stop();
    operator double() const {return _result;}
};

namespace avx {
    void TestVector(int size, int repeat);
    void TestValArray(int size, int repeat);
    void TestEigen(int size, int repeat);
}

namespace noavx {
    void TestVector(int size, int repeat);
    void TestValArray(int size, int repeat);
    void TestEigen(int size, int repeat);
}

extern Timer g_Timer;
extern std::default_random_engine generator;
extern std::uniform_real_distribution<double> distribution;