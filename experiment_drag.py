#This experiment demonstrates drag. It slows down the particles moving faster more

from view import *

n = 20
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 10 * u
    vel = -1 * u 
    particles.append(Particle(1,pos,vel,0.6))

def combined_forces(dt, particles, forces=[circular_arena, constant_gravitational_field, collision, drag]):
    for f in forces:
        f(dt, particles)

simulation_loop(combined_forces, 0.0003, particles)
