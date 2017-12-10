import matplotlib.pyplot as plt
import matplotlib.patches as patches
from factory import Factory
from factory import Rectangle


# f = Factory()
# f.AddRectangle(Rectangle(1,1,2,2))

def Cross(j,x, y, xp, yp):
    first = j
    second = 0
    if j == len(xp)-1:
        second = 0
    else:
        second = j+1
    print(first, second)
    yh = (x - xp[first]) * (yp[second] - yp[first]) / (xp[second] - xp[first]) + yp[first]
    minimal = min(xp[first], xp[second])
    maximal = max(xp[first], xp[second])
    return (xp[first] != xp[second]) and (y >= yh) and (x > minimal) and (x <= maximal)


def inPolygon(x, y, xp, yp):
    c = 0
    for i in range(len(xp)):
        c += Cross(i,x, y, xp, yp)
        if (((yp[i] <= y and y < yp[i - 1]) or (yp[i - 1] <= y and y < yp[i])) and (
                    x > (xp[i - 1] - xp[i]) * (y - yp[i]) / (yp[i - 1] - yp[i]) + xp[i])):
            c = 1 - c
    return c


print(inPolygon(0, 0, (-100, 100, 100, -100), (100, 100, -100, -100)))
