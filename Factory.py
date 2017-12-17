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
        ratio = self.settings["ratios"][index]
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
        acceptable_rectangles = self.get_acceptable_rectangles(width, height, index)
        r = self.get_optima_rectangle(acceptable_rectangles)
        # self.rectangles.append(acceptable_rectangles[random.randint(0, len(acceptable_rectangles) - 1)])
        # self.rectangles += acceptable_rectangles
        self.rectangles.append(r)

    def get_optima_rectangle(self, acceptable_rectangles):
        min_d = float("inf")
        optima = Rectangle(0, 0)
        for r in acceptable_rectangles:
            index = r.index
            D = 0
            for rect in self.rectangles:
                index_rect = rect.index
                # print(index_rect)
                D += self.settings["coefficients"][self.settings["location"][index][index_rect]] + \
                     Point.distance(r.center(), rect.center()) * self.settings["traffic"][index][index_rect]
                # D += Point.distance(r.center(), rect.center())
            if (D < min_d):
                min_d = D
                optima = r
        return optima

    def get_acceptable_rectangles(self, width, height, index):
        points = []  # сюда будем складывать все точки, куда можно поставить следующий прямоугольник
        raycast_points = []
        points.append(self.rectangles[0].b)
        for rect in self.rectangles:
            points += rect.points()
            for edge in rect.edges():
                found, nearest_point, distance, horizontal, i = \
                    Rectangle.get_nearest_rayast_point(edge, self.rectangles)
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
        return acceptable_rectangles

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
        for i in range(len(self.settings["areas"])):
            for j in range(len(self.settings["areas"])):
                if j > i:
                    self.settings["location"][j][i] = self.settings["location"][i][j]
                if self.settings["traffic"][j][i] > 0:
                    self.settings["traffic"][i][j] = self.settings["traffic"][j][i]
                if self.settings["traffic"][i][j] > 0:
                    self.settings["traffic"][j][i] = self.settings["traffic"][i][j]

    def print_result(self):
        length = len(self.rectangles)
        for i in range(length):
            for r in self.rectangles:
                if r.index == i:
                    print(r)

    def save_result(self):
        f = open("result.txt","w")
        length = len(self.rectangles)
        for i in range(length):
            for r in self.rectangles:
                if r.index == i:
                    f.write(str(r)+'\n')


f = Factory()
f.load_settings()

concomponent = Utils.connection_components(f.settings["traffic"])
for component in concomponent:
    for i in range(len(component)-1):
        for j in range(i+1,len(component)):
            if f.settings["areas"][component[j]] > f.settings["areas"][component[i]]:
                component[i], component[j] = component[j], component[i]
    for i in range(len(component)):
        f.add_rectangle(component[i])
f.print_result()
f.show_rectangles()
f.save_result()
