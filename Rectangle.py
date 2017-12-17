###
# классы для удобной работы с прямоугльниками и точками
###

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def tuple(self):
        return (self.x, self.y)

    # @staticmethod
    # def distance(p1,p2):

    # @staticmethod
    # def check_segment_cross_segment(a,b,x,y):
    # проверяем, лежит ли точка p на отрезке ab (который может быть либо горизонтальный, либо вертикальный)
    @staticmethod
    def check_point_on_segment(a, b, p):
        if ((a.x <= p.x <= b.x) or (b.x <= p.x <= b.x) and a.y == p.y == b.y) or (
                    (a.y <= p.y <= b.y) or (b.y <= p.y <= b.y) and a.x == p.x == b.x):
            return True
        else:
            return False


# прямоугольник abcd будем считать фигуру в определенной последовательности:
# a -------- b
#  |        |
#  |        |
# c -------- d
class Rectangle:
    a = Point(0, 0)
    b = Point(0, 0)
    c = Point(0, 0)
    d = Point(0, 0)
    width = 0
    height = 0
    abstract = True  # абстрактный прямоугольник будет означать, что у него заданы ширина и высота, но не точки
    index = -1  # индекс прямоугольника

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.abstract = True
        self.max_x = 0
        self.max_y = 0
        self.min_x = 0
        self.min_y = 0

    def __str__(self):
        return str(self.a) + str(self.b) + str(self.c) + str(self.d)

    # всего возможны 8 комбинаций расположения прямоугольника
    # вокруг точки p
    def set_rect(self, p, swipe, up, right):
        if swipe:
            (self.width, self.height) = (self.height, self.width)
        if (up):
            if (right):
                self.a = Point(p.x, p.y + self.height)
                self.b = Point(p.x + self.width, p.y + self.height)
                self.c = Point(p.x + self.width, p.y)
                self.d = Point(p.x, p.y)
            else:
                self.a = Point(p.x, p.y + self.height)
                self.b = Point(p.x - self.width, p.y + self.height)
                self.c = Point(p.x - self.width, p.y)
                self.d = Point(p.x, p.y)
        else:
            if right:
                self.a = Point(p.x, p.y - self.height)
                self.b = Point(p.x + self.width, p.y - self.height)
                self.c = Point(p.x + self.width, p.y)
                self.d = Point(p.x, p.y)
            else:
                self.a = Point(p.x, p.y - self.height)
                self.b = Point(p.x - self.width, p.y - self.height)
                self.c = Point(p.x - self.width, p.y)
                self.d = Point(p.x, p.y)
        self.max_x = max(self.a.x, self.b.x, self.c.x, self.d.x)
        self.max_y = max(self.a.y, self.b.y, self.c.y, self.d.y)
        self.min_x = min(self.a.x, self.b.x, self.c.x, self.d.x)
        self.min_y = min(self.a.y, self.b.y, self.c.y, self.d.y)
        self.reformat_rectangle()
        self.abstract = False

    # проверяет, в правильном ли порядке расположены точки
    def reformat_rectangle(self):
        self.a = Point(self.min_x, self.max_y)
        self.b = Point(self.max_x, self.max_y)
        self.c = Point(self.max_x, self.min_y)
        self.d = Point(self.min_x, self.min_y)

    def points(self):
        return [self.a, self.b, self.c, self.d]

    def edges(self):
        return [(self.a, self.b), (self.b, self.c), (self.c, self.d), (self.d, self.a)]

    def center(self):
        return Point((self.max_x - self.min_x) / 2, (self.max_y - self.min_y) / 2)

    # один прямоугольник будет пересекать другой когда:
    # - хотя бы одна точка лежит внутри него
    # - если все точки лежат на гранях прямоугольника
    @staticmethod
    def check_cross(r1, r2):
        for p in r1.points():
            if Rectangle.check_point_in_rect(r2, p):
                return True
        for p in r2.points():
            if Rectangle.check_point_in_rect(r1, p):
                return True
        edge_crosses = 0
        for edge in r1.edges():
            if Rectangle.check_edge_in_rect(r2, edge):
                edge_crosses += 1
        for edge in r2.edges():
            if Rectangle.check_edge_in_rect(r1, edge):
                edge_crosses += 1
        if edge_crosses > 3:  # MAGIC
            return True
        return False

    @staticmethod
    def check_point_in_rect(rect, p):
        if rect.min_x < p.x < rect.max_x and rect.min_y < p.y < rect.max_y:
            return True
        else:
            return False

    # проверяем, касается\пересекает ли отрезок прямоугольник
    @staticmethod
    def check_edge_in_rect(rect, edge):
        count = 0
        for e in rect.edges():
            if Rectangle.check_edge_cross_edge(e, edge):
                count += 1
        if count >= 2:
            return True
        else:
            return False

    # пересекают ли два отрезка друг друга
    @staticmethod
    def check_edge_cross_edge(e1, e2):
        # если они параллельны, то точно не пересекает
        if (e1[0].x == e1[1].x and e2[0].x == e2[1].x) or \
                (e1[0].y == e1[1].y and e2[0].y == e2[1].y):
            return False
        if e1[0].y == e1[1].y and e2[0].x == e2[1].x and \
                                min(e2[0].y, e2[1].y) <= e1[0].y <= max(e2[0].y, e2[1].y) and \
                                min(e1[0].x, e1[1].x) <= e2[0].x <= max(e1[0].x, e1[1].x):
            return True
        if e1[0].x == e1[1].x and e2[0].y == e2[1].y and \
                                min(e2[0].x, e2[1].x) <= e1[0].x <= max(e2[0].x, e2[1].x) and \
                                min(e1[0].y, e1[1].y) <= e2[0].y <= max(e1[0].y, e1[1].y):
            return True
        return False

    @staticmethod
    def create_rectangles_from_point(p, width, height, limit_w=0, limit_h=0, index=-1):
        ret = []
        for i in range(8):
            args = [True if digit == '1' else False for digit in bin(i)[2:]]
            args = [False] * (3 - len(args)) + args
            if (limit_w == 0 or limit_w < width) and \
                    (limit_h == 0 or limit_h < height):
                r = Rectangle(width, height)
                r.set_rect(p, args[0], args[1], args[2])
                r.index = index
                ret.append(r)
        return ret

    @staticmethod
    def get_nearest_rayast_point(edge, rectangles):
        min_distance = float("inf")
        nearest_point = Point(0, 0)
        found = False
        index = -1
        for rect in rectangles:
            for e in rect.edges():
                res = Rectangle.check_ray_cross_edge(edge, e)
                if res[0] == True and res[2] < min_distance:
                    min_distance = res[2]
                    nearest_point = res[1]
                    found = True
                    index = rect.index
        # в конце вернем является ли луч вертикальным или горизонтальным
        return found, nearest_point, min_distance, edge[0].y == edge[1].y, index

    # проверяем, пересекает ли луч пущенный из одного отрезка в разные стороны другой отрезок
    @staticmethod
    def check_ray_cross_edge(seg, edge):
        # если они параллельны, то точно не пересекает
        if (seg[0].x == seg[1].x and edge[0].x == edge[1].x) or \
                (seg[0].y == seg[1].y and edge[0].y == edge[1].y):
            return False, Point(0, 0), 0
        if seg[0].y == seg[1].y and min(edge[0].y, edge[1].y) <= seg[0].y <= max(edge[0].y, edge[1].y):
            return True, Point(edge[0].x, seg[0].y), min(abs(edge[0].x - seg[0].x), abs(edge[0].x - seg[1].x))
        if seg[0].x == seg[1].x and min(edge[0].x, edge[1].x) <= seg[0].x <= max(edge[0].x, edge[1].x):
            return True, Point(seg[0].x, edge[0].y), min(abs(edge[0].y - seg[0].y), abs(edge[0].y - seg[1].y))
        return False, Point(0, 0), 0

    # r1 = Rectangle(3, 4)
    # r1.set_rect(Point(0, 0), False, True, True)
    # for p in r1.points():
    #     print(p)
    # print()
    # r2 = Rectangle(3, 2)
    # r2.set_rect(Point(1, 1), False, True, True)
    # for p in r2.points():
    #     print(p)
    # print()
    # r3 = Rectangle(3, 2)
    # r3.set_rect(Point(3, 1), False, True, True)
    # for p in r3.points():
    #     print(p)
    # print()
    # r4 = Rectangle(3, 2)
    # r4.set_rect(Point(4, 5), False, True, True)
    # print(Rectangle.check_cross(r1, r3))
    # print(Rectangle.check_edge_in_rect(r3, (Point(0,0),Point(3,0))))

    # for r in Rectangle.create_rectangles_from_point(Point(0,0),3,2):
    #     print(r)
    # print(Rectangle.bool_args_from_int(8))

    # for edge in r1.edges():
    # print(Point(3, 5), Point(3, 7))
    # print(r1.edges()[0][0], r1.edges()[0][1])
    # print(Rectangle.check_ray_cross_edge((Point(3, 3), Point(5, 3)), edge)[1])
    # print(Rectangle.check_ray_cross_edge((Point(3, 3), Point(5, 3)), edge)[2])
