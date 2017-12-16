import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
from Rectangle import Rectangle
from Rectangle import Point
from Settings import get_test_settings


class Factory:
    rectangles = []

    def AddRectangle(self, r):
        self.rectangles.append(r)

    def ShowRectangles(self):
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111, aspect='equal')
        ax1.grid(True, which='both')
        for rect in self.rectangles:
            print(rect.center())
            ax1.add_patch(
                patches.Rectangle(
                    rect.d.tuple(),  # (x,y)
                    rect.width,  # width
                    rect.height,  # height
                    color=(random.random(),random.random(), random.random())
                )
            )
        plt.show()
r1 = Rectangle(3, 4)
r1.set_rect(Point(0, 0), False, True, True)
r2 = Rectangle(3, 2)
r2.set_rect(Point(1, 1), False, True, True)
f = Factory()
f.AddRectangle(r1)
f.AddRectangle(r2)
f.ShowRectangles()