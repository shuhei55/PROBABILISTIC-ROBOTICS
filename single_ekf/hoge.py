#! /usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random



class Map:
    DT = 10 #ms
    def __init__(self):
        self.x = 0
        self.y = 0
        self.theta = 0
        self.Pxy = np.array([[10,0,0],
                            [0,10,0],
                            [0,0,10]])

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.theta = pos[2]

    def update(self, sim):
        self.x += sim.get_enc()[0]
        self.y += sim.get_enc()[1]
        self.theta += sim.get_gyro() * sim.DT
        self.Pxy += np.array([[2500,0,0],
                             [0,2500,0],
                             [0,0,2500]])

    def update2(self, sim):
        tmp = np.array([sim.get_x_length() - self.x, sim.get_y_length() - self.y])
        tmp[0] = tmp[0] * (self.Pxy[0] / (self.Pxy[0] + 400.0))
        tmp[1] = tmp[1] * (self.Pxy[1] / (self.Pxy[1] + 400.0))
        self.x += tmp[0]
        self.y += tmp[1]
        self.Pxy[0] *= 1 - (self.Pxy[0]/(self.Pxy[0] + 400.0))
        self.Pxy[1] *= 1 - (self.Pxy[1]/(self.Pxy[1] + 400.0))

