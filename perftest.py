import numpy as np
import time
import sys
import rpy2.robjects as ro
import perftest

def TestNDArray(size, repeat):
    def test(repeat, v1, v2):
        start = time.time()
        for i in xrange(0, repeat):
            d = np.random.rand() * 4 - 2
            v1 += d * v2
        print 'time = %.3f (s)' % (time.time() - start)
    test(repeat,
         np.random.rand(size, 2),
         np.random.rand(size, 2))

def Main():
    if len(sys.argv) > 2:
        size = int(sys.argv[1])
        repeat = int(sys.argv[2])

        print '*** Python: numpy.ndarray ***'
        TestNDArray(size, repeat)

        print "*** R ***"
        r = ro.r('source(\'perftest.R\')')
        r = ro.r('TestAll(%d, %d)' % (size, repeat))

        print "*** C++: no-vectorize no-avx ***"
        perftest.testVector(size, repeat)
        perftest.testValArray(size, repeat)
        perftest.testEigen(size, repeat)

        print "*** C++: vectorize avx ***"
        perftest.testVectorV(size, repeat)
        perftest.testValArrayV(size, repeat)
        perftest.testEigenV(size, repeat)

if __name__ == '__main__':
    Main()