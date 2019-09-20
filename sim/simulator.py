import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random

class Sim:
    DT = 10 #ms
    def __init__(self,x,y,dx,dy,theta,omega):
        self.x = x #mm
        self.y = y #mm
        self.dx = dx #mm/s
        self.dy = dy #mm/s
        self.theta = theta #rad
        self.omega = omega # rad/s
        self.ddx = 0 #mm/s^2
        self.ddy = 0 #mm/s^2
        self.ep = 0 #rad/s^2
        self.b_x = 0
        self.b_y = 0

    def setpos(self,x,y,dx,dy,theta,omega):
        self.x = x #mm
        self.y = y #mm
        self.dx = dx #mm/s
        self.dy = dy #mm/s
        self.theta = theta #rad
        self.omega = omega # rad/s
        self.b_x = 0
        self.b_y = 0

    def poszero(self):
        self.setpos(0,0,0,0,0,0)

    def setacc(self,ddx,ddy,ep):
        self.ddx = ddx
        self.ddy = ddy
        self.ep = ep

    def setacczero(self):
        self.setacc(0,0,0)

    def update(self):
        self.b_x = self.x
        self.b_y = self.y
        self.x += (self.dx * self.DT + 0.5 * self.ddx * self.DT**2)
        self.y += (self.dy * self.DT + 0.5 * self.ddy * self.DT**2)
        self.dx += (self.ddx + (random.random() - 0.5) * 0.1) * self.DT
        self.dy += (self.ddy + (random.random() - 0.5) * 0.1) * self.DT
        self.theta += (self.omega * self.DT + 0.5 * self.ep * self.DT**2)
        self.omega += (self.ep + (random.random() - 0.5) * 0.00001) * self.DT

    def get_enc(self):
        return np.dot(np.array([[np.cos(self.theta), -np.sin(self.theta)],[np.sin(self.theta), np.cos(self.theta)]]), np.array([(self.x - self.b_x) * (1 + 0.3 * (random.random() - 0.6)), (self.y - self.b_y) * (1 + 0.3 * (random.random() - 0.4))]).T)

    def get_x_length(self):
        return self.x + 20 * (random.random() - 0.5)

    def get_y_length(self):
        return self.y + 20 * (random.random() - 0.5)

    def get_theta(self):
        return self.theta + 0.00000000 * (random.random() - 0.5)

    def get_gyro(self):
        return self.omega + (random.random() - 0.5) * 0.000001


#x=0の柵があると過程したとき
#angleはマシンの正面からみた角度右が正
    def get_single_wall_length(self, angle):
        field_angle = self.theta + angle
        length = -self.x / np.float64(np.sin(field_angle))
        if length < 0 or length == np.inf:
            return np.inf
        else :
            return length + (random.random() - 0.5) * 5


#以下はx=4000, x=-4000, y= 4000, y=-4000に柵があると過程したときのもの
#angleはマシンの正面からみた角度右が正
    def get_multi_wall_length(self,angle):
        field_angle = self.theta + angle
        ls = []
        #x = 4000
        length = (4000 - self.x) / np.float64(np.sin(field_angle))
        if  length < 0 or length == np.inf:
            ls.append(np.inf)
        else :
            ls.append(length)
        #x = -4000
        length = (4000 + self.x) / np.float64(np.sin(-field_angle))
        if  length < 0 or length == np.inf:
            ls.append(np.inf)
        else :
            ls.append(length)
        #y = 4000
        length = (4000 - self.y) / np.float64(np.cos(field_angle))
        if  length < 0 or length == np.inf:
            ls.append(np.inf)
        else :
            ls.append(length)
        #y = -4000
        length = (4000 + self.x) / np.float64(np.cos(-field_angle))
        if  length < 0 or length == np.inf:
            ls.append(np.inf)
        else :
            ls.append(length)

        if min(ls) == np.inf:
            return np.inf
        else:
            return min(ls) + (random.random() - 0.5) * 5

