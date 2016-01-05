CC=g++
RM=rm -f

TARGET=ems
SRCS=$(wildcard *.cpp)
OBJS=$(SRCS:.cpp=.o)

override CFLAGS+=-Wall -fPIC -std=c++11 -O3 -g -Wno-deprecated-declarations
LFLAGS=

# http://www.isus.jp/article/compileroptimization/compiler_part1/
# http://www.isus.jp/article/compileroptimization/avx_part1/
# https://gcc.gnu.org/projects/tree-ssa/vectorization.html
VFLAGS=-ftree-vectorize -ftree-vectorizer-verbose=1 -mavx

INCLUDES=-I/usr/local/python/current/include/python2.7 -I/usr/local/boost/current/include
LIBDIRS=-L/usr/local/python/current/lib -L/usr/local/boost/current/lib
LIBS=-lpython2.7 -lboost_python

all: clean $(TARGET) ems.so

clean:
	$(RM) $(OBJS) $(TARGET)

$(TARGET): $(OBJS)
	$(CC) $(LFLAGS) $(LIBDIRS) $^ -o $@ $(LIBS)

ems.so: emsfield.o shared.o
	$(CC) -shared $(LFLAGS) $(LIBDIRS) $^ -o $@ $(LIBS)

$(OBJS): $(SRCS)
	$(CC) $(INCLUDES) $(CFLAGS) $(VFLAGS) -c $^
