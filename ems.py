import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import time
from c import ems

class Field:
    def __init__(self, dim, size, nodes):
        self.colors = ['#000000',
                       '#ff0000',
                       '#0000ff',
                       '#ff00ff',
                       '#00ff00',
                       '#00ffff',
                       '#ffff00',
                       '#ffffff']
        self.fig, self.ax = plt.subplots(figsize=(6, 6), dpi=80)
        self.epos = 0
        self.ehistory = [100] * 5
        self.ax.axis([-size, size, -size, size])
        self.field = ems.Field(dim, nodes)
        self.size = size
        self.dim = dim
        self.nodes = nodes

    def setXY(self, idx, x, y):
        self.field.SetXY(idx, x, y)

    def addSpring(self, n1, n2, k, l):
        self.field.AddSpring(n1, n2, k, l)

    def updateEnergy(self):
        self.ehistory[self.epos] = self.field.Energy()
        self.epos = (self.epos + 1) % len(self.ehistory)
        e = np.mean(self.ehistory)
        return e

    def frameGen(self):
        dt = .1
        while self.updateEnergy() >= self.limit:
            for i in range(0, 10):
                self.field.Move(dt)
                yield self.field
        print 'time = %.3f sec' % (time.time() - self.startTime)

    def initFrame(self):
        self.startTime = time.time()
        data = next(self.frameGen())
        pos = np.array(data.Positions())
        n = self.nodes
        self.scat = self.ax.scatter(pos[0*n:1*n], pos[1*n:2*n],
                                    s=50, c=self.colors, marker='o', edgecolors='k')
        return self.scat,

    def updateFrame(self, i):
        data = next(self.frameGen())
        self.scat.set_offsets(np.reshape(data.Positions(), (-1, 2), order='F'))
        return self.scat,

    def bulkInit(self, friction=1, m=1):
        self.field.BulkInit(int(time.time()), m, friction, self.size)

    def start(self, limit=.1):
        self.limit = limit
        self.anime = animation.FuncAnimation(self.fig,
                                             self.updateFrame,
                                             init_func=self.initFrame,
                                             interval=50,
                                             save_count=10000)

    def save(self, filename):
        try:
            self.anime.save(filename,
                            writer='ffmpeg',
                            extra_args=['-vcodec', 'libx264'])
        except StopIteration:
            pass

    def show(self):
        plt.show()