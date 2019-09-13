from drawer import drawer

def init(drawer):
    img = drawer.draw_line([-4000,-4000], [-4000,4000],"k")
    img = drawer.draw_line([4000,4000], [4000,-4000],"k")
    img = drawer.draw_line([4000,4000], [-4000,4000],"k")
    img = drawer.draw_line([4000,-4000], [-4000,-4000],"k")
    return img
