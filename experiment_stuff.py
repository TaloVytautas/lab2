from view import *

n = 20
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 10 * u
    vel = -1 * u 
    particles.append(Particle(1,pos,vel,0.6))   

def combined_walls(dt, particles):
    wall_force(dt, particles, k=10, n=Vec(1, 0), a=Vec(-4,0))
    wall_force(dt, particles, k=10, n=Vec(0, 1), a=Vec(0,-4))
    wall_force(dt, particles, k=10, n=Vec(-1, 0), a=Vec(4,0))
    wall_force(dt, particles, k=10, n=Vec(0, -1), a=Vec(0,4))

def combined_forces(dt, particles, forces=[constant_gravitational_field, combined_walls]):
    for f in forces:
        f(dt, particles)

simulation_loop(combined_forces, 0.00005, particles)
