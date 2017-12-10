import matplotlib.pyplot as plt
import matplotlib.patches as patches


# прямоугольник abcd будем считать фигуру в определенной последовательности:
# a -------- b
#  |        |
#  |        |
# c -------- d

class Factory:
    rectangles = []

    def AddRectangle(self, r):
        self.rectangles.append(r)

    def ShowRectangles(self):
        fig1 = plt.figure()
        ax1 = fig1.add_subplot(111, aspect='equal')
        for rect in self.rectangles:
            ax1.add_patch(
                patches.Rectangle(
                    (rect.centerX - rect.width / 2, rect.centerY - rect.height / 2),  # (x,y)
                    rect.width,  # width
                    rect.height,  # height
                )
            )
        plt.show()


