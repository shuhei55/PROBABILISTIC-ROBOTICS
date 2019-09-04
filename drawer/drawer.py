import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as pat
import math

class Drawing():
    def __init__(self, func):
        self.color = []
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-5000,5000)
        self.ax.set_ylim(-5000,5000)
        self.ax.set_aspect('equal')
        self.ax.set_xlabel('X [m]') 
        self.ax.set_ylabel('Y [m]') 
        self.ax.grid(True)
        self.ani = animation.FuncAnimation(self.fig, func, interval=100, frames=1000)

    def draw_point(self, center_x, center_y, c = "r", pointsize=3):#人の大きさは半径15cm
        return self.ax.plot(center_x, center_y, ".", color=c,markersize=pointsize)


    def draw_circle(self, center_x, center_y, size_x, size_y, c = "b"):
        e1 = pat.Ellipse(xy = (center_x, center_y), width = size_x, height = size_y, angle = 0,fc = None, fill = False,ec = c)
        return self.ax.add_patch(e1)

    def draw_arraw(self,start_x,start_y,end_x,end_y):
        return self.ax.annotate('', xy=(end_x,end_y), xytext=(start_x,start_y),
            arrowprops=dict(arrowstyle='-|>', 
                            connectionstyle='arc3', 
                            facecolor='C0', 
                            edgecolor='C0')
           )

    def show(self):
        plt.show()
