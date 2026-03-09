#Collision doesn't have its own experiment because it is demonstrated in other experiments
#We have elected to have default values definied in model.pyso that we don't have to define a function for most experiments
#This experiment demonstrates a constant gravitational field, but also walls and collisions so that the particles stay on the screen. The particles are initiated with some velocity so that they dont just fall down and instead get to bounce around a bit, in various diretions. A slightly unexpected thing is that while the particles stay symmetrical at first they quickly become chaotic due to what I assume is floating point errors. Due to this and most other experiments not having drag or friction they will go on forever
#Decreasing the timestep increases accuracy but slows down the simulation while increasing it decreases accuracy and increases simulation speed. The reason for most experiments having a much larger timestep compared to experiment_inertial is mainly due to them using one of the functions that use the helper function all_particles due to it being O(n^2).

from view import *

n = 20
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 10 * u
    vel = -1 * u 
    particles.append(Particle(1,pos,vel,0.6))

def combined_forces(dt, particles, forces=[circular_arena, constant_gravitational_field, collision]):
    for f in forces:
        f(dt, particles)

simulation_loop(combined_forces, 0.0003, particles)
