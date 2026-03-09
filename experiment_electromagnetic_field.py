#This experiment demonstrates particles moving perpendicular to an electromagnetic field. This causes all positively charged particles to move clockwise in circles and negatively charged particles to move counter clockwise.

from view import *

n = 20
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 8 * u
    vel = -1 * u 
    particles.append(Particle(1,pos,vel,0.6))
    particles[i].set_charge(cos(theta*4))

def combined_forces(dt, particles, forces=[electromagnetic_field]):
    for f in forces:
        f(dt, particles)

simulation_loop(combined_forces, 0.0001, particles)
