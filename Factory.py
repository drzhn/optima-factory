import matplotlib.pyplot as plt
import matplotlib.patches as patches
import random
import math
from Utils import Utils
from Rectangle import Rectangle
from Rectangle import Point
from Settings import get_test_settings


class Factory:
    rectangles = []

    def add_rectangle(self, index):
        ratio = self.settings["ratio"]
        area = self.settings["areas"][index]
        width, height = math.sqrt(area / ratio), math.sqrt(area / ratio) * ratio
        if len(self.rectangles) == 0:
            # all_rectangles = Rectangle.create_rectangles_from_point(Point(0, 0), width, height)
            r = Rectangle(width, height)
            r.set_rect(Point(0, 0), False, False, False)
            r.index = index
            self.rectangles.append(r)
            # self.rectangles += all_rectangles
            return
        points = []  # сюда будем складывать все точки, куда можно поставить следующий прямоугольник
        raycast_points = []
        # points.append(self.rectangles[0].b)
        for rect in self.rectangles:
            points += rect.points()
            for edge in rect.edges():
                found, nearest_point, distance, horizontal, i = \
                    Rectangle.get_nearest_rayast_point(edge,self.rectangles)
                if found:
                    raycast_points.append((nearest_point, distance, horizontal))

        all_rectangles = []
        for p in points:
            all_rectangles += Rectangle.create_rectangles_from_point(p, width, height, index=index)
        for p in raycast_points:
            if p[1] > 0:
                if p[2]:
                    all_rectangles += Rectangle.create_rectangles_from_point(p, width, height, p[1], 0, index=index)
                else:
                    all_rectangles += Rectangle.create_rectangles_from_point(p, width, height, 0, p[1], index=index)
        acceptable_rectangles = []
        for r in all_rectangles:
            accept = True
            for rectangle in self.rectangles:
                if Rectangle.check_cross(r, rectangle):
                    accept = False
            if accept:
                acceptable_rectangles.append(r)
        # print(len(acceptable_rectangles))
        # self.rectangles += acceptable_rectangles
        self.rectangles.append(acceptable_rectangles[random.randint(0, len(acceptable_rectangles) - 1)])

    def show_rectangles(self):
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111, aspect='equal')
        ax1.grid(True, which='both')

        for rect in self.rectangles:
            # print(rect.center())
            ax1.add_patch(
                patches.Rectangle(
                    rect.d.tuple(),  # (x,y)
                    rect.width,  # width
                    rect.height,  # height
                    color=(random.random(), random.random(), random.random())
                )
            )
        plt.show()

    def load_settings(self):
        self.settings = get_test_settings()


f = Factory()
f.load_settings()

concomponent = Utils.connection_components(f.settings["traffic"])
for component in concomponent:
    for index in component:
        f.add_rectangle(index)
# f.add_rectangle(0)
# f.add_rectangle(1)
f.show_rectangles()

# r1 = Rectangle(3, 4)
# r1.set_rect(Point(0, 0), False, True, True)
# r2 = Rectangle(3, 2)
# r2.set_rect(Point(1, 1), False, True, True)
# f = Factory()
# f.AddRectangle(r1)
# f.AddRectangle(r2)
# f.ShowRectangles()
