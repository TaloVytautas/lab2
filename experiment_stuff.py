from view import *

n = 1000
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 8 * u
    vel = -5 * u 
    particles.append(Particle(1,pos,vel,0.6))

def combined_walls(dt, particles):
    wall_force(dt, particles, k=10, n=Vec(1, 0), a=Vec(-4,0))
    wall_force(dt, particles, k=10, n=Vec(0, 1), a=Vec(0,-4))
    wall_force(dt, particles, k=10, n=Vec(-1, 0), a=Vec(4,0))
    wall_force(dt, particles, k=10, n=Vec(0, -1), a=Vec(0,4))

def combined_forces(dt, particles, forces=[combined_walls]):
    for f in forces:
        if f is spring_force:
            f(dt, springs)
            continue
        f(dt, particles)
    

simulation_loop(combined_forces, 0.01, particles)
