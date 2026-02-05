from tkinter import *
from model import *
import time

root = Tk()
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack()

def to_canvas_coords(canvas, x):
    height = canvas.winfo_reqheight()-4
    width = canvas.winfo_reqwidth()-4
    vector = height/20*x
    vector = Vec(vector.x, -vector.y)
    return vector + Vec(width/2, height/2)

def move_oval_to(o, u1, u2):
    v1=to_canvas_coords(canvas, u1)
    v2=to_canvas_coords(canvas, u2)
    canvas.coords(o,v1.x,v1.y,v2.x,v2.y)

def move_line_to(l, u1, u2):
    v1=to_canvas_coords(canvas, u1)
    v2=to_canvas_coords(canvas, u2)
    canvas.coords(l,v1.x,v1.y,v2.x,v2.y)

def create_oval(canvas, particle):
    color = "green"
    if particle.charge > 0:
        color = "red"
    if particle.charge < 0:
        color = "blue"
    oval = canvas.create_oval(0, 0, 2*particle.radius, 2*particle.radius, fill=color)
    u1, u2 = particle.bounding_box()
    move_oval_to(oval, u1, u2)
    return oval

def create_line(canvas, spring):
    p1_pos = spring.particle1.position
    p2_pos = spring.particle2.position
    line = canvas.create_line(p1_pos.x, p1_pos.y, p2_pos.x, p2_pos.y, fill="black", width=2)
    return line

def simulation_loop(f, timestep, particles, springs = None):
    partovals = {}
    springlines = {}
    if springs is not None:
        for s in springs:
            springlines[s] = create_line(canvas, s)

    for p in particles:
        partovals[p] = create_oval(canvas, p)
    
    past = time.time()
    while True:
        f(timestep, particles)
        for p in particles:
            p.inertial_move(timestep)
        if time.time() >= past + 1/30:
            if springs is not None:
                for s in springs:
                    u1, u2 = s.particle1.position, s.particle2.position
                    move_line_to(springlines[s], u1, u2)
            for p in particles:
                u1, u2 = p.bounding_box()
                move_oval_to(partovals[p], u1, u2)
            past = time.time()
            canvas.update()
