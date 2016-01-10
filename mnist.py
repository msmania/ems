import sys
import os
import time
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

def writeDistances(images):
    dir = os.path.expanduser('~/Documents/MNIST_data/')
    with open(dir + 'distance', 'wb') as f:
        # use nested loop instead of itertools.combinatin to make sure the order
        for j in xrange(1, len(images)):
            for i in xrange(0, j):
                d = distance.euclidean(images[i].astype('d'),
                                       images[j].astype('d'))
                f.write(struct.pack('d', d))

def readDistances(nodes):
    dir = os.path.expanduser('~/Documents/MNIST_data/')
    with open(dir + 'distance-10k', 'rb') as f:
        x = f.read(8 * nodes * (nodes - 1) / 2)
    return x

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
    initTime = time.time()
    distances = readDistances(nodes)
    for pair in itertools.combinations(np.arange(0, nodes), 2):
        # pair[0] < pair[1]
        idx = pair[1] * (pair[1] - 1) / 2 + pair[0]

        d = struct.unpack('d', distances[(8*idx):(8*idx + 8)])[0]
        # d = distance.euclidean(images[pair[0]].astype('d'),
        #                        images[pair[1]].astype('d'))

        d /= 350

        # N=200 --> k=.5
        # N=1000 --> k=.02 ~ .1
        # N=5000 --> k=.005 ~ .01
        # N=10000 --> k=.002 ~ .005
        field.addSpring(pair[0], pair[1], k=.5, l=d)
    del(distances)
    print 'initialize = %.3f sec' % (time.time() - initTime)
    field.start(limit=.1)
    if len(sys.argv)>1:
        field.save(sys.argv[1])
        print 'Done!'
    else:
        field.show()

if __name__ == '__main__':
    Main()
    # images,labels = readMNIST(0)
    # writeDistances(images)