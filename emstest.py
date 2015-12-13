import numpy as np
import itertools
import sys
import ems

def basic():
    fieldSize = 5
    field = ems.Field(dim=2, size=fieldSize)
    field.add([4, -2], friction=.04, color='b')
    field.add([-3, 3], friction=.04, color='r')
    field.add([-3, -3], friction=.04, color='#ff00ff')
    field.addSpring(0, 1, k=2, l=4)
    field.addSpring(1, 2, k=2, l=4)
    field.addSpring(2, 0, k=2, l=4)
    return field, .001

def bulk():
    fieldSize = 5
    field = ems.Field(dim=2, size=fieldSize)
    nodes = 30
    field.bulkInit((np.random.rand(nodes, 2) * 2 - 1) * fieldSize,
                   friction=.04)
    field.colors = ['#000000',
                    '#ff0000',
                    '#0000ff',
                    '#ff00ff',
                    '#00ff00',
                    '#00ffff',
                    '#ffff00',
                    '#ffffff']
    for pair in itertools.combinations(np.arange(0, nodes), 2):
        field.addSpring(pair[0], pair[1], k=2, l=4)

    return field, .1

fieldMap = {'basic' : basic,
            'bulk' : bulk}

def Main():
    testname = sys.argv[1] if len(sys.argv)>1 else 'basic'
    if testname in fieldMap:
        field, limit = fieldMap[testname]()
        field.start(limit)
        if len(sys.argv)>2:
            field.save(sys.argv[2])
            print 'Done!'
        else:
            field.show()
    else:
        print 'invalid arg'

if __name__ == '__main__':
    Main()
