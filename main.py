#! /usr/bin/python3
from sim import simulator
from drawer import drawer
import math
import numpy as np
from config import config
from kf import hoge


def plot(data):
    global cnt
    cnt += 1
    simulator.update()
    kf.update(simulator)
    if cnt % 10 == 0:
        kf.update2(simulator)
    #ball_img = drawer.draw_arraw(simulator.x,simulator.y, simulator.x+500*math.sin(simulator.theta), simulator.y+500*math.cos(simulator.theta))
    ball_img = drawer.draw_point(simulator.x, simulator.y)
    ball_img = drawer.draw_point(kf.x,kf.y, c='b')
    ball_img = drawer.draw_circle(kf.x,kf.y,np.sqrt(kf.Pxy[0]),np.sqrt(kf.Pxy[1]),c='g')
    if abs(simulator.x) > 4000 or abs(simulator.y) > 4000 :
        drawer.stop_animation()
    return ball_img

cnt = 0

simulator = simulator.Sim(0,0,0,0,0,0) #x,y,theta,dx,dy,dtheta
simulator.setacc(0,0,0) #ddx,ddy,ddtheta
simulator.setpos(-3000,-3000,5,5,0,0.0001) #x,y,theta,dx,dy,dtheta

kf = hoge.Map()

kf.set_pos([-3000,-3000,5,5])

drawer = drawer.Drawing(plot)

ball_img = config.init(drawer)

drawer.show()
