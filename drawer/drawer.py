import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as pat
from matplotlib.widgets import Button
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
        self.playButton  = self.__createButton(0, 0, 0.15, 0.1, "play/pause", self.stop_animation) # (左下 x 座標, 左下 y 座標, 幅, 高さ, ラベル, バインドする函数)
        self.ani = animation.FuncAnimation(self.fig, func, interval=100, frames=10)

    def draw_point(self, center_x, center_y, c = "r", pointsize=3):#人の大きさは半径15cm
        return self.ax.plot(center_x, center_y, ".", color=c,markersize=pointsize)


    def draw_circle(self, center_x, center_y, size_x, size_y, c = "b"):
        e1 = pat.Ellipse(xy = (center_x, center_y), width = size_x, height = size_y, angle = 0,fc = None, fill = False,ec = c)
        return self.ax.add_patch(e1)

    def draw_arraw(self,start_x,start_y,end_x,end_y):
        return self.ax.annotate('', xy=(end_x,end_y), xytext=(start_x,start_y),
                arrowprops=dict(shrink=0, width=0.5, headwidth=2, 
                                headlength=2, connectionstyle='arc3',
                                facecolor='gray', edgecolor='gray')
           )

    def draw_line(self,p1,p2,c="g"):
        return self.ax.plot([p1[0],p2[0]], [p1[1],p2[1]], color = c)

    def stop_animation(self,event):
        self.ani.event_source.stop()

    def __createButton(self, bottomLeftX, bottomLeftY, width, height, label, func):
        box    = self.fig.add_axes([bottomLeftX, bottomLeftY, width, height]) # ボタン用の枠を描いて、
        button = Button(box, label)                                           # それをボタンとして実体化して、
        button.on_clicked(func)                                               # クリックされたときに実行する函数をバインドする。
        return button

    def show(self):
        plt.show()
