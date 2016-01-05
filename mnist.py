import sys
import os
import itertools
import struct
import numpy as np
import ems
from scipy.spatial import distance

def readMNIST(findex):
    imagefiles = ['t10k-images-idx3-ubyte', 'train-images-idx3-ubyte']
    labelfiles = ['t10k-labels-idx1-ubyte', 'train-labels-idx1-ubyte']
    dir = os.path.expanduser('~/Documents/MNIST_data/')
    with open(dir + imagefiles[findex], 'rb') as f:
        magic = f.read(4)
        n = struct.unpack('>L', f.read(4))[0]
        x = struct.unpack('>L', f.read(4))[0]
        y = struct.unpack('>L', f.read(4))[0]
        images = f.read(n * x * y)
    with open(dir + labelfiles[findex], 'rb') as f:
        magic = f.read(4)
        n = struct.unpack('>L', f.read(4))[0]
        labels = f.read(n)
    return (np.split(np.fromstring(images, dtype=np.uint8), n),
            np.fromstring(labels, dtype=np.uint8))

def Main():
    colorMap = ['#000000',
                '#0000ff',
                '#ff0000',
                '#ff00ff',
                '#00ff00',
                '#00ffff',
                '#ffff00',
                '#ffffff',
                '#808080',
                '#000080']
    nodes = int(os.environ['N']) if 'N' in os.environ else 10
    fieldSize = 10
    images,labels = readMNIST(0)
    field = ems.Field(dim=2, size=fieldSize, nodes=nodes)
    field.bulkInit(friction=.04)
    field.colors = [colorMap[l] for l in labels]
    for pair in itertools.combinations(np.arange(0, nodes), 2):
        d = distance.euclidean(images[pair[0]].astype('d'),
                               images[pair[1]].astype('d'))
        d /= 350
        field.addSpring(pair[0], pair[1], k=.5, l=d)
    field.start(limit=.1)

    if len(sys.argv)>1:
        field.save(sys.argv[1])
        print 'Done!'
    else:
        field.show()

if __name__ == '__main__':
    Main()