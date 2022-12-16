from colors import *
from base import Base
from threading import Thread
import random

calc = None

try:
    from code.clib import mCalc
    calc = mCalc
except:
    pass

class Mandelbrot(Base):

    def __init__(self, size, title=""):
        Base.__init__(self, size, self.__run, title)
        self.setExp(2)
        self.setRadius(2)
        self.setZ0(0 + 0j)
        self.width = size[0]
        self.height = size[1]
        self.setRange(3.5, 3.5)
        self.setCentre(0 + 0j)

    def setRadius(self, R):
        self.R = R

    def setZ0(self, Z0):
        self.Z0 = Z0

    def setCentre(self, z0):
        self.z0 = z0

    def setRange(self, xmax, ymax):
        self.xmax = xmax
        self.ymax = ymax

    def __getXY(self, i, j):
        return complex((i / self.width - 0.5) * self.xmax + self.z0.real, (j / self.height - 0.5) * self.ymax + self.z0.imag)

    def scala(self, i, j, rate):
        self.setCentre(self.__getXY(i, j))
        self.xmax /= rate
        self.ymax /= rate

    def setExp(self, expc):
        self.expc = expc

    def color(self, n, r=2):
        color_list = [yellows, purples, blues, reds, rainbow]
        first_color = purples
        second_color = blues
        third_color = blues
        if n < len(first_color):
            return first_color[n]
        else:
            if r < self.R:
                return second_color[int((len(second_color) - 1) * r / self.R)]
            else:
                return third_color[int((len(third_color) - 1) * self.R / r)]


    def setColor(self, call):
        self.color = call

    def __calc(self, start, w, h):
        for i in range(w):
            for j in range(h):
                if calc:
                    ct, r = mCalc((start[0] + i, start[1] + j, self.Z0.real, self.Z0.imag, self.z0.real,
                                   self.z0.imag, self.width, self.height, self.xmax, self.ymax, self.N, self.expc, self.R))
                    self.screen.set_at(
                        [start[0] + i, start[1] + j], self.color(ct, r))
                else:
                    ct = 0
                    z = self.Z0
                    c = self.__getXY(start[0] + i, start[1] + j)
                    for k in range(self.N):
                        ct = k
                        if abs(z) > self.R:
                            break
                        z = z**self.expc + c
                    self.screen.set_at(
                        [start[0] + i, start[1] + j], self.color(ct, abs(z)))

    def __run(self):
        print("x range ：[-%.2e,%.2e]\ny range ：[-%.2e,%.2e]" % (
            self.xmax, self.xmax, self.ymax, self.ymax))
        tn = 5
        ci = self.width // tn
        cj = self.height // tn
        ts = []
        for i in range(tn):
            for j in range(tn):
                t = Thread(target=self.__calc, args=(
                    [i * ci, j * cj], self.width // tn, self.height // tn))
                t.start()
                ts.append(t)
        for t in ts:
            t.join()
        del ts

    def doMandelbrot(self, N):
        self.N = N
