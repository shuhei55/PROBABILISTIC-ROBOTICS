#! /usr/bin/python3
import numpy as np
import numpy.linalg as LA
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import random



class Map:
    DT = 10 #ms
    def __init__(self):
        self.x = np.array([[0,0,0]])
        self.Pxy = np.array([[10,0,0],
                             [0,10,0],
                             [0,0,0.0001]])

    def set_pos(self, pos):
        self.x = np.array(pos)
        self.Pxy = np.array([[10,0,0],
                             [0,10,0],
                             [0,0,0.0001]])

    def update(self, sim):
        self.x += np.array([[0,0,sim.get_gyro() * self.DT]])
        self.x += (np.array([[np.cos(-self.x[0][2]),-np.sin(-self.x[0][2])],[np.sin(-self.x[0][2]),np.cos(-self.x[0][2])],[0,0]]) @ sim.get_enc()).T
        self.Pxy += np.array([[1600,0,0],
                             [0,1600,0],
                             [0,0,0.00000001]])


    def differential_1(self, angle):
        return np.array([[-(1./np.sin(angle+self.x[0][2])), 0, (4000-self.x[0][0])*(-np.cos(angle+self.x[0][2])/(np.sin(angle+self.x[0][2])**2))]])

    def differential_2(self, angle):
        return np.array([[-(1./np.sin(angle+self.x[0][2])), 0, (-4000-self.x[0][0])*(-np.cos(angle+self.x[0][2])/(np.sin(angle+self.x[0][2])**2))]])

    def differential_3(self, angle):
        return np.array([[0, -(1./np.cos(angle+self.x[0][2])), (4000-self.x[0][1])*(np.sin(angle+self.x[0][2])/(np.cos(angle+self.x[0][2])**2))]])

    def differential_4(self, angle):
        return np.array([[0, -(1./np.cos(angle+self.x[0][2])), (-4000-self.x[0][1])*(np.sin(angle+self.x[0][2])/(np.cos(angle+self.x[0][2])**2))]])

    def h_1(self, angle):
        tmp = (4000-self.x[0][0])/np.sin(angle+self.x[0][2])
        if tmp < 0 or tmp == np.inf:
            return np.inf
        else:
            return tmp

    def h_2(self, angle):
        tmp = (-4000-self.x[0][0])/np.sin(angle+self.x[0][2])
        if tmp < 0 or tmp == np.inf:
            return np.inf
        else:
            return tmp

    def h_3(self, angle):
        tmp = (4000-self.x[0][1])/np.cos(angle+self.x[0][2])
        if tmp < 0 or tmp == np.inf:
            return np.inf
        else:
            return tmp

    def h_4(self, angle):
        tmp = (-4000-self.x[0][1])/np.cos(angle+self.x[0][2])
        if tmp < 0 or tmp == np.inf:
            return np.inf
        else:
            return tmp

    def update2(self, sim):
        angle = 1.57
        #angle = 0
        filter_R = np.array([[1600]])
        log_P_tmp = -0.5*np.log(2*np.pi)-0.5*np.log(np.abs(LA.det(filter_R)))
        y = sim.get_multi_wall_length(angle)
        if y == np.inf:
            pass
        else :
            h_y = np.array([self.h_1(angle),self.h_2(angle),self.h_3(angle),self.h_4(angle)])
            print(h_y,y)
            log_P = log_P_tmp-0.5*((y-h_y)*(1/filter_R)*(y-h_y))
            #print(log_P)
            if log_P.max() < -10:
                pass
            else :
                argmax = log_P.argmax()
                if argmax == 0:
                    jacobian = self.differential_1(angle)
                elif argmax == 1:
                    jacobian = self.differential_2(angle)
                elif argmax == 2:
                    jacobian = self.differential_3(angle)
                else :
                    jacobian = self.differential_4(angle)
                kalman_gain = (self.Pxy @ jacobian.T) / (jacobian @ self.Pxy @ jacobian.T + filter_R)
                print("hoge")
                self.x += kalman_gain.T * (y - h_y[argmax])
                self.Pxy = (1 - kalman_gain @ jacobian) * self.Pxy
        #angle = 1.57
        angle = 3.14
        y = sim.get_multi_wall_length(angle)
        if y == np.inf:
            pass
        else :
            h_y = np.array([self.h_1(angle),self.h_2(angle),self.h_3(angle),self.h_4(angle)])
            log_P = log_P_tmp-0.5*((y-h_y)*(1/filter_R)*(y-h_y))
            print(h_y,y)
            if log_P.max() < -10:
                print("piyo")
                pass
            else :
                argmax = log_P.argmax()
                if argmax == 0:
                    jacobian = self.differential_1(angle)
                elif argmax == 1:
                    jacobian = self.differential_2(angle)
                elif argmax == 2:
                    jacobian = self.differential_3(angle)
                else :
                    jacobian = self.differential_4(angle)
                kalman_gain = (self.Pxy @ jacobian.T) / (jacobian @ self.Pxy @ jacobian.T + filter_R)
                print("fuga")
                self.x += kalman_gain.T * (y - h_y[argmax])
                self.Pxy = (1 - kalman_gain @ jacobian) * self.Pxy
