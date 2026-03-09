#This experiment demonstrates as spring as well as the coloumb force. The spring wants the particles to stay at the distance they are but the coloumb force causes them to get attracted and causes this bounce behaviour. I am very tired and am like two days late cus I forgot that I hadn't finished making the experiment files

from view import *

n = 2
particles = []
for i in range(n):
    theta = i*2*pi/n
    u = Vec(cos(theta),sin(theta))
    pos = 2 * u
    vel = -1 * u 
    particles.append(Particle(1,pos,vel,0.6))
    particles[i].set_charge((-1)**(i+1))

springs = [Spring(particles[0], particles[1], 4, 20)]

def combined_forces(dt, particles, forces=[spring_force, coulomb_force]):
    for f in forces:
        if f is spring_force:
            f(dt, springs)
            continue
        f(dt, particles)
    

simulation_loop(combined_forces, 0.000005, particles, springs)
