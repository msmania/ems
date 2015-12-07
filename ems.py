import numpy as np
from matplotlib import pyplot as plt

class Node:
    def __init__(self, initpos):
        self.friction = 0
        self.m = 1
        self.vel = np.array([0, 0], dtype='d')
        self.pos = np.array(initpos, dtype='d')
        self.force = lambda : np.array([0, 0])

    def dump2D(self):
        print "[%+.3f %+.3f] v[%+.3f %+.3f] a[%+.3f %+.3f]" % \
            (self.pos[0], self.pos[1],
             self.vel[0], self.vel[1],
             self.acc[0], self.acc[1])

    def setFriction(self, u):
        self.friction = u
        
    def getForceFixed(self, f):
        return lambda : np.array([0, f])

    def getForceSpring(self, k):
        return lambda : np.array([0, -k * self.pos[1]])
        
    def setForce(self, force):
        self.force = force
    
    def energy(self):
        return .5 * self.m * np.sum(self.vel * self.vel)

    def move(self, dt):
        self.acc = self.force()
        self.pos += dt * self.vel
        self.vel += dt * (self.force() - self.friction * self.vel) / self.m

    def statvector(self):
        return np.array([self.pos[1], self.vel[1], self.acc[1]])

class Plotting:
    def __init__(self):
        # data = [t, x, v, a]
        self.data = np.empty((4, 0), dtype='d')
        self.styles = ['k', '#ff00ff', 'b']

    def add(self, newvector):
        self.data = np.c_[self.data, newvector]

    def show(self):
        for row, style in zip(self.data[1:,:], self.styles):
            plt.plot(self.data[0,:], row, style, linewidth=2)
        plt.show()
        
class Field:
    def __init__(self):
        self.nodes = []
        self.plot = Plotting()
        
    def add(self, node):
        self.nodes.append(node)
        
    def run(self):
        t = .0
        dt = .01
        for i in xrange(0, 1000):
            e = .0
            for node in self.nodes:
                # node.dump2D()
                node.move(dt)
                e += node.energy()
                t += dt
                self.plot.add(np.r_[t, node.statvector()])
        self.plot.show()

def Main():
    n = Node([0, 1])

    n.setFriction(.1)
    n.setForce(n.getForceFixed(2))

    #n.setFriction(1)
    #n.setForce(n.getForceSpring(2))
    
    field = Field()
    field.add(n)
    field.run()

if __name__ == '__main__':
    Main()
