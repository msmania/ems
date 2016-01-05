#include <stdlib.h>
#include <valarray>
#include <vector>
#include "emsfield.h"

int main(int argc, char *argv[]) {
    Field field(/*dim*/2, /*n*/2);
    // Field.BulkInit(/*m*/1.0, /*friction*/.5, /*field*/5);
    darray initpos = {0.0, 0.0, 0.0, 2.0};
    field.BulkInit(/*m*/1.0, /*friction*/.5, initpos);
    field.AddSpring(0, 1, 1.0, 1.0);
    for (int i=0 ; i<10 ; ++i) {
        field.Dump();
        field.Move(.1);
    }
    exit(0);
}
