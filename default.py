#! /usr/bin/python3

from sim import simulator
from drawer import drawer
import numpy as np
from config import config

def plot(data):
    sim.update()
    ball_img = drawer.draw_point(sim.x,sim.y)
    return ball_img

sim = simulator.Sim(0,0,1,1,0,0) #コンストラクタ

drawer = drawer.Drawing(plot)

ball_img = config.init(drawer)

drawer.show()
