#! /usr/bin/python3
from sim import simulator
from drawer import drawer
import math


def plot(data):
    simulator.update()
    ball_img = drawer.draw_arraw(simulator.x,simulator.y, simulator.x+500*math.sin(simulator.theta), simulator.y+500*math.cos(simulator.theta))
    ball_img = drawer.draw_point(simulator.x, simulator.y)
    print(simulator.get_wall_length(1.57))
    print(simulator.get_wall_length(-1.57))
    return ball_img

simulator = simulator.Sim(0,0,0,0,0,0) #x,y,theta,dx,dy,dtheta
simulator.setacc(0,0,0) #ddx,ddy,ddtheta
simulator.setpos(-3000,-3000,5,5,0,0.0001) #x,y,theta,dx,dy,dtheta

drawer = drawer.Drawing(plot)
ball_img = drawer.draw_line([-4000,-4000], [-4000,4000],"k")
ball_img = drawer.draw_line([4000,4000], [4000,-4000],"k")
ball_img = drawer.draw_line([4000,4000], [-4000,4000],"k")
ball_img = drawer.draw_line([4000,-4000], [-4000,-4000],"k")

drawer.show()
