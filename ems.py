import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial import distance

class Node:
    def __init__(self, initpos, friction):
        self.m = 1
        self.friction = friction
        self.acc = np.array([0, 0], dtype='d')
        self.vel = np.array([0, 0], dtype='d')
        self.pos = np.array(initpos, dtype='d')
        self.forceGenerators = []
        self.history = np.empty((7, 0), dtype='d')

    def getFixedForceGenerator(node, f):
        return lambda : np.array([0, f])
    
    def getSpringForceGenerator(nodeFrom, nodeTo, k, l):
        return lambda : k * (1 - l / distance.euclidean(nodeFrom.pos, nodeTo.pos)) * \
            (nodeTo.pos - nodeFrom.pos)

    def addForceGenerator(self, forceGenerator):
        self.forceGenerators.append(forceGenerator)

    def addSpring(n1, n2, k, l):
        n1.addForceGenerator(Node.getSpringForceGenerator(n1, n2, k, l))
        n2.addForceGenerator(Node.getSpringForceGenerator(n2, n1, k, l))

    def energy(self):
        return .5 * self.m * np.sum(self.vel * self.vel)

    def move(self, dt):
        force = np.array([0, 0], dtype='d')
        for forceGenerator in self.forceGenerators:
            force += forceGenerator()
        self.acc = force / self.m # for history logging
        self.pos += dt * self.vel
        self.vel += dt * (force - self.friction * self.vel) / self.m

    def log(self, t):
        self.history = np.c_[self.history, \
                             np.r_[t, self.pos, self.vel, self.acc]]

class Plotting:
    def __init__(self):
        self.styles = ['k', '#ff00ff', 'b']

    def addplot(self, node):
        # plt.plot(node.history[0], node.history[1], 'k', linewidth=2) # x
        plt.plot(node.history[0], node.history[2], 'k', linewidth=2) # y
        # plt.plot(node.history[0], node.history[3], 'k', linewidth=2) # vx
        # plt.plot(node.history[0], node.history[4], 'k', linewidth=2) # vy
        # plt.plot(node.history[0], node.history[5], 'k', linewidth=2) # ax
        # plt.plot(node.history[0], node.history[6], 'k', linewidth=2) # ay

class Field:
    def __init__(self):
        self.nodes = []

    def add(self, node):
        self.nodes.append(node)
        
    def run(self):
        t = .0
        dt = .01
        for i in xrange(0, 1000):
            e = .0
            for node in self.nodes:
                node.log(t)
                e += node.energy()
                node.move(dt)
            print "t = %3.3f e = %.6f" % (t,  e)
            t += dt

        plot = Plotting()
        for node in self.nodes:
            plot.addplot(node)

        plt.show()

def Main():
    n1 = Node([0, 0], 1)
    n2 = Node([0, 2], 1)
    Node.addSpring(n1, n2, k=2, l=1)
    
    field = Field()
    field.add(n1)
    field.add(n2)
    field.run()

if __name__ == '__main__':
    Main()
