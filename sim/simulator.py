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
        return np.array([[np.cos(self.theta), -np.sin(self.theta)],[np.sin(self.theta), np.cos(self.theta)]]) @ np.array([[(self.x - self.b_x) * (1 + 0.3 * (random.random() - 0.6)), (self.y - self.b_y) * (1 + 0.3 * (random.random() - 0.4))]]).T

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
        length = (-4000 - self.x) / np.float64(np.sin(field_angle))
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
        length = (-4000 - self.y) / np.float64(np.cos(field_angle))
        if  length < 0 or length == np.inf:
            ls.append(np.inf)
        else :
            ls.append(length)

        if min(ls) == np.inf:
            return np.inf
        else:
            return min(ls) + (random.random() - 0.5) * 5

 # マシンの向きに対して垂直方向に12素子並んでいるラインセンサーを仮定する
 # マシンの中心から左右に素子間の距離を2mmでならんでいる
 # つまりマシン座標系で(1,0),(-1,0),(3,0),(-3,0)...とならんでいる
 # x=0(y軸)とy=0(x軸)に幅200mmの線が引かれていてそれを認識できるとする
 # またノイズとして一定の確率で正負がひっくり返ることがある
    def get_line_sensor(self):
        machine_sensor_point = np.array(
            [
                [11, 9, 7, 5, 3, 1, -1, -3, -5, -7, -9, -11],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            ]
        )
        field_sensor_point = np.array(
            [
                [np.cos(-self.theta), -np.sin(-self.theta)],
                [np.sin(-self.theta), np.cos(-self.theta)],
            ]
        ) @ machine_sensor_point + np.array([[self.x], [self.y]])
        data = np.random.rand(12)
        for i in range(0, len(data)):
            if (
                field_sensor_point[0][i] >= -100 and field_sensor_point[0][i] <= 100
            ) or (field_sensor_point[1][i] >= -100 and field_sensor_point[1][i] <= 100):
                data[i] -= 0.01
            else:
                data[i] -= 0.99
            if data[i] < 0:
                data[i] = 0
            else:
                data[i] = 1
        return data
