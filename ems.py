import sys
import itertools
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from scipy.spatial import distance

class Field:
    def __init__(self, dim=2, size=5):
        self.dim = dim
        self.m = []
        self.friction = []
        self.forces = []
        self.colors = []
        self.acc = np.empty((0, dim), dtype='d')
        self.vel = np.empty((0, dim), dtype='d')
        self.pos = np.empty((0, dim), dtype='d')
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=80)
        self.ehistory = [100] * 5
        self.ax.axis([-size, size, -size, size])

    def addSpring(self, n1, n2, k, l):
        self.forces[n1].append(self.getSpringForceGenerator(n1, n2, k, l))
        self.forces[n2].append(self.getSpringForceGenerator(n2, n1, k, l))

    def getSpringForceGenerator(self, n1, n2, k, l):
        return lambda : k * (1 - l / distance.euclidean(self.pos[n1,:],
                                                        self.pos[n2,:])) * \
                            np.array(self.pos[n2,:] - self.pos[n1,:])

    def move(self, dt):
        self.acc = np.array([sum([f() for f in forces])
                             for forces in self.forces]) / np.c_[self.m]
        self.vel += dt * np.array(self.acc)
        self.vel -= np.c_[np.array(self.friction) / self.m] * self.vel
        self.pos += dt * np.array(self.vel)
        #self.dump(0)

    def updateEnergy(self):
        earray = np.array([sum(np.array(v) * v) for v in self.vel]) * self.m
        self.ehistory.append(sum(earray))
        self.ehistory.pop(0)
        e = np.mean(self.ehistory)
        #print e
        return e

    def frameGen(self):
        dt = .1
        while self.updateEnergy() >= .001:
            self.move(dt)
            yield self

    def initFrame(self):
        data = next(self.frameGen())
        x = data.pos[:,0]
        y = data.pos[:,1]
        self.scat = self.ax.scatter(x, y,
                                    s=50, c=self.colors, marker='o', edgecolors='k')
        return self.scat,

    def updateFrame(self, i):
        data = next(self.frameGen())
        self.scat.set_offsets(data.pos)
        return self.scat,

    def dump(self, i):
        print '%4d (%+.3f, %+.3f) v(%+.3f, %+.3f) a(%.3f, %.3f)' % \
            (i,
             self.pos[i,0], self.pos[i,1],
             self.vel[i,0], self.vel[i,1],
             self.acc[i,0], self.acc[i,1])

    def add(self, pos, friction=1, m=1, color='b'):
        self.m.append(m)
        self.friction.append(friction)
        self.forces.append([lambda : np.array(np.zeros(self.dim))])
        self.colors.append(color)
        self.acc = np.vstack([self.acc, np.zeros(self.dim)])
        self.vel = np.vstack([self.vel, np.zeros(self.dim)])
        self.pos = np.vstack([self.pos, pos])

    def bulkInit(self, pos, friction=1, m=1, color='b'):
        n = pos.shape[0]
        self.dim = pos.shape[1]
        self.m = np.tile(m, n)
        self.friction = np.tile(friction, n)
        self.forces = [[lambda : np.array(np.zeros(self.dim))] for i in xrange(0, n)]
        self.colors = np.tile(color, n)
        self.acc = np.zeros(pos.shape)
        self.vel = np.zeros(pos.shape)
        self.pos = pos

    def start(self):
        self.anime = animation.FuncAnimation(self.fig,
                                             self.updateFrame,
                                             init_func=self.initFrame,
                                             interval=50,
                                             save_count=10000)

    def save(self, filename):
        self.anime.save(filename,
                        writer='ffmpeg',
                        extra_args=['-vcodec', 'libx264'])

def Main():
    fieldSize = 5
    field = Field(dim=2, size=fieldSize)

    nodes = 8
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

    field.start()

    if len(sys.argv)>1:
        try:
            field.save(sys.argv[1])
        except StopIteration:
            pass
        print 'Done!'
    else:
        plt.show()

if __name__ == '__main__':
    Main()
