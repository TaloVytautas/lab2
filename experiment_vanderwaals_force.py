#This experiment demonstrates van der waals force. While the intial conditions are identical to the gravitational force experiment the results are rather different. Mainly that the particles seem to gather at the bottom of the screen as oppesed to the top and that the timestep is 10 times greater. This is due to the van der waals force being weaker and that the higher mass of the particles at the top made them move slower and attract other particles more while for van der waals the particles with higher mass were just slower and due to all of the particles having the same radius the forces are initially equal.

from view import *

n = 20
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 10 * u
    vel = -0 * u 
    particles.append(Particle(2 + sin(theta),pos,vel,0.6))

def combined_forces(dt, particles, forces=[vanderwaals_force, collision]):
    for f in forces:
        f(dt, particles)

simulation_loop(combined_forces, 0.0005, particles)
