#! /usr/bin/python3
from sim import simulator
from drawer import drawer
import math
import numpy as np
from config import config
from multi_model_ekf import hoge


def plot(data):
    global cnt
    cnt += 1
    simulator.update()
    ekf.update(simulator)
    if cnt % 10 == 0:
        ekf.update2(simulator)
    ball_img = drawer.draw_arraw(simulator.x,simulator.y, simulator.x+200*math.sin(simulator.theta), simulator.y+200*math.cos(simulator.theta))
    ball_img = drawer.draw_point(simulator.x, simulator.y)
    ball_img = drawer.draw_point(ekf.x[0][0],ekf.x[0][1], c='b')
    ball_img = drawer.draw_circle(ekf.x[0][0],ekf.x[0][1],np.sqrt(ekf.Pxy[0][0]),np.sqrt(ekf.Pxy[1][1]),c='g')
    ball_img = drawer.draw_arraw(ekf.x[0][0],ekf.x[0][1], ekf.x[0][0]+200*np.sin(ekf.x[0][2]), ekf.x[0][1]+200*np.cos(ekf.x[0][2]),"black")
    #print(simulator.get_multi_wall_length(1.57))
    if abs(simulator.x) > 4000 or abs(simulator.y) > 4000 :
        drawer.stop_animation()
    return ball_img

cnt = 0

simulator = simulator.Sim(0,0,0,0,0,0) #x,y,theta,dx,dy,dtheta
simulator.setacc(0,0,0) #ddx,ddy,ddtheta
simulator.setpos(-3000,-3000,5,5,0,0.0001) #x,y,theta,dx,dy,dtheta

ekf = hoge.Map()

ekf.set_pos([[-3000,-3000,0.0]])

drawer = drawer.Drawing(plot)

ball_img = config.init(drawer)

drawer.show()
