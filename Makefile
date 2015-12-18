CC=g++
RM=rm -f

TARGET=perftest
SRCS=common.cpp main.cpp
OBJS=$(SRCS:.cpp=.o)

override CFLAGS+=-Wall -fPIC -std=c++11 -O3 -g -Wno-deprecated-declarations
LFLAGS=

# http://www.isus.jp/article/compileroptimization/compiler_part1/
# http://www.isus.jp/article/compileroptimization/avx_part1/
# https://gcc.gnu.org/projects/tree-ssa/vectorization.html
VFLAGS=-ftree-vectorize -ftree-vectorizer-verbose=6 -mavx -D_AVX

INCLUDES=-I/usr/include/python2.7 -I/usr/include/eigen3
#LIBDIRS=-L/usr/local/openssl/current/lib
LIBS=-lpython2.7 -lboost_python

all: clean $(TARGET).so runc

clean:
	$(RM) *.o *.so

$(TARGET).so: perftest.o perftest_avx.o common.o shared.o
	$(CC) -shared $(LFLAGS) $(LIBDIRS) $^ -o $@ $(LIBS)

runc: perftest.o perftest_avx.o $(OBJS)
	$(CC) $(LFLAGS) $(LIBDIRS) $^ -o $@ $(LIBS)

perftest.o: perftest.cpp
	$(CC) $(INCLUDES) $(CFLAGS) -c $^

perftest_avx.o: perftest.cpp
	$(CC) $(INCLUDES) $(CFLAGS) $(VFLAGS) -c $^ -o $@

$(OBJS): $(SRCS) shared.cpp
	$(CC) $(INCLUDES) $(CFLAGS) -c $^
