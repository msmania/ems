import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation as animation
from scipy.spatial import distance

class Field:
    def __init__(self, dim=2):
        self.dim = dim
        self.m = []
        self.friction = []
        self.forces = []
        self.acc = np.empty((0, dim), dtype='d')
        self.vel = np.empty((0, dim), dtype='d')
        self.pos = np.empty((0, dim), dtype='d')
        self.fig, self.ax = plt.subplots()

    def addSpring(self, n1, n2, k, l):
        self.forces[n1].append(self.getSpringForceGenerator(n1, n2, k, l))
        self.forces[n2].append(self.getSpringForceGenerator(n2, n1, k, l))

    def getSpringForceGenerator(self, n1, n2, k, l):
        return lambda : k * (1 - l / distance.euclidean(self.pos[n1,:],
                                                        self.pos[n2,:])) * \
                            np.array(self.pos[n2,:] - self.pos[n1,:])

    def move(self, dt):
        self.acc = np.array([sum([f() for f in forces])
                             for forces in self.forces]) / self.m
        self.vel += dt * np.array(self.acc) - (self.friction * self.vel) / self.m
        self.pos += dt * np.array(self.vel)

    def frameGen(self):
        dt = .1
        for i in xrange(0, 1000):
            self.move(dt)
            yield self

    def initFrame(self):
        data = next(self.frameGen())
        x = data.pos[:,0]
        y = data.pos[:,1]
        self.scat = self.ax.scatter(x, y)
        l = 5
        self.ax.axis([-l, l, -l, l])
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

    def add(self, pos, friction=1, m=1):
        self.m.append(m)
        self.friction.append(friction)
        self.forces.append([])
        self.acc = np.vstack([self.acc, np.zeros(self.dim)])
        self.vel = np.vstack([self.vel, np.zeros(self.dim)])
        self.pos = np.vstack([self.pos, pos])
        
    def start(self):
        self.anime = animation.FuncAnimation(self.fig,
                                             self.updateFrame,
                                             init_func=self.initFrame,
                                             interval=50)

    def save(self, filename):
        self.anime.save(filename)

def Main():
    field = Field(dim=2)
    field.add([0, 4], .04)
    field.add([0, -4], .04)
    field.addSpring(0, 1, k=2, l=5)
    field.start()
    #field.save('ems.mp4')
    print 'Done!'
    plt.show()

if __name__ == '__main__':
    Main()
