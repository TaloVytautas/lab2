from tkinter import *
from model import *
import time

root = Tk()
canvas = Canvas(root, bg="white", width=800, height=600)
canvas.pack()

def to_canvas_coords(canvas, x):
    height = canvas.winfo_reqheight()
    width = canvas.winfo_reqwidth()
    vector = height/20*x
    vector = Vec(vector.x, -vector.y)
    return vector + Vec(height/2, width/2)

def move_oval_to(o, u1, u2):
    v1=to_canvas_coords(canvas, u1)
    v2=to_canvas_coords(canvas, u2)

    canvas.coords(o,v1.x,v1.y,v2.x,v2.y)

def create_oval(canvas, particle):
    oval = canvas.create_oval(0, 0, particle.radius, particle.radius, fill="blue")
    u1, u2 = particle.boundin_box()
    move_oval_to(oval, u1, u2)

# test
for n in range(5):
  particle = Particle(0, Vec(n,n), Vec(0,0), 0.2)
  create_oval(canvas, particle)
  canvas.update()
  time.sleep(1)
