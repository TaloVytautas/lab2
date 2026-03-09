#This experiment demonstrates gravity between particles. Due to the mass of these particles varying with the mass being 3 att the top of the screen and 1 att the bottom the particles are more attraced to the ones at the top

from view import *

n = 20
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 10 * u
    vel = -0 * u 
    particles.append(Particle(2 + sin(theta),pos,vel,0.6))

def combined_forces(dt, particles, forces=[gravitational_force, collision]):
    for f in forces:
        f(dt, particles)

simulation_loop(combined_forces, 0.00005, particles)
