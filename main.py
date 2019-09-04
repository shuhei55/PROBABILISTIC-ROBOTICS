#! /usr/bin/python3
from sim import simulator
from drawer import drawer


def plot(data):
    simulator.update()
    #ball_img = drawer.draw_arraw(simulator.x,simulator.y, simulator.x + 0, simulator.y + 100)
    ball_img = drawer.draw_point(simulator.x, simulator.y)
    ball_img = drawer.draw_circle(simulator.x,simulator.y, 500, 100)
    return ball_img

simulator = simulator.Sim(0,0,0,0,0,0)
simulator.setacc(0,0,0)
simulator.setpos(-500,-500,10,10,0,0)

drawer = drawer.Drawing(plot)

drawer.show()
