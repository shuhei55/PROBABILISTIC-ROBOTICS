#! /usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random



class Map:
    DT = 10 #ms
    def __init__(self):
        self.x = np.array([[0,0,0]])
        self.Pxy = np.array([[10,10,0.0001]])

    def set_pos(self, pos):
        self.x = np.array(pos)
        self.Pxy = np.array([[10,10,0.0001]])

    def update(self, sim):
        self.x += np.array([[0,0,sim.get_gyro() * self.DT]])
        self.x += (np.array([[np.cos(-self.x[0][2]),-np.sin(-self.x[0][2])],[np.sin(-self.x[0][2]), np.cos(-self.x[0][2])],[0,0]]) @ sim.get_enc()).T
        self.Pxy += np.array([[1600,1600,0.0001]])

    def update2(self, sim):
        tmp = np.array([[sim.get_x_length(), sim.get_y_length(), sim.get_theta()]]) - self.x
        tmp *= (self.Pxy / (self.Pxy + np.array([[600,600,0.000001]])))
        self.x += tmp
        self.Pxy *= (1 - (self.Pxy/(self.Pxy + np.array([[600.0,600,0.000001]]))))
