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
    wall_force(dt, particles, k=1000000, n=Vec(1, 0), a=Vec(-10,0))
    wall_force(dt, particles, k=1000000, n=Vec(0, 1), a=Vec(0,-10))
    wall_force(dt, particles, k=1000000, n=Vec(-1, 0), a=Vec(10,0))
    wall_force(dt, particles, k=1000000, n=Vec(0, -1), a=Vec(0,10))

def combined_forces(dt, particles, forces=[combined_walls, constant_gravitational_field, collision]):
    for f in forces:
        if f is spring_force:
            f(dt, springs)
            continue
        f(dt, particles)
    

simulation_loop(combined_forces, 0.0005, particles)
