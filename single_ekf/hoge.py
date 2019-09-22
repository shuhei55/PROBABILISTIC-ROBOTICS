#! /usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random



class Map:
    DT = 10 #ms
    def __init__(self):
        self.x = np.array([0,0,0])
        self.Pxy = np.array([[10,0,0],
                             [0,10,0],
                             [0,0,0.0001]])

    def set_pos(self, pos):
        self.x = np.array(pos)
        self.Pxy = np.array([[10,0,0],
                             [0,10,0],
                             [0,0,0.0001]])

    def update(self, sim):
        self.x += np.array([0,0,sim.get_gyro() * self.DT])
        self.x += np.dot(np.array([[np.cos(-self.x[2]),-np.sin(-self.x[2])],[np.sin(-self.x[2]),np.cos(-self.x[2])],[0,0]]),sim.get_enc().T)
        self.Pxy += np.array([[1600,0,0],
                             [0,1600,0],
                             [0,0,0.00000001]])


    def differential(self, angle):
        return np.array([-(1./np.sin(angle+self.x[2])), 0, -self.x[0]*(-np.cos(angle+self.x[2])/(np.sin(angle+self.x[2])**2))])

    def update2(self, sim):
        angle = 1.57
        y = sim.get_single_wall_length(angle)
        if y == np.inf:
            pass
        else :
            y_p = - self.x[0] / np.float64(np.sin(angle + self.x[2]))
