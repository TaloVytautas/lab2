from math import *

class Vec:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x},{self.y})"
    def __rmul__(self, factor):
        return Vec(self.x*factor, self.y*factor)
    def __add__(self, other):
        return Vec(self.x+other.x, self.y+other.y)
    def __sub__(self, other):
        return Vec(self.x-other.x, self.y-other.y)
    def norm(self):
        return sqrt(self.x**2 + self.y**2)
    def get_coords(self):
        return (self.x, self.y)

def dot(u, v):
    vector1 = u.get_coords()
    vector2 = v.get_coords()
    return vector1[0]*vector2[0]+vector1[1]*vector2[1]

class Particle:
    def __init__(self, mass, position, velocity, radius):
        self.mass = mass
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.charge = 0
    def inertial_move(self, dt):
        self.position += dt*self.velocity
    def apply_force(self, dt, f):
        self.velocity += dt/self.mass*f
    def bounding_box(self):
        topl=Vec(self.position.x-self.radius,self.position.y+self.radius)
        botr=Vec(self.position.x+self.radius,self.position.y-self.radius)
        return (topl,botr)
    def set_charge(self, new_charge):
        self.charge = new_charge

class Spring:
    def __init__(self, particle1, particle2, l, k):
        self.particle1 = particle1
        self.particle2 = particle2
        self.l = l
        self.k = k
    def length(self):
        return (self.particle1.position - self.particle2.position).norm()
    def force(self, dt):
        dire = self.particle2.position - self.particle1.position
        len = self.length()
        x = (len - self.l)/len
        f = self.k*x*dire
        self.particle1.apply_force(dt, f)
        self.particle2.apply_force(dt, -1*f)

def constant_gravitational_field(dt, particles, g=10):
    d = Vec(0, -1)
    for p in particles:
        p.apply_force(dt, g*p.mass*d)

#I came up with some basic optimizations like not doing every calculation twice and defining variables as little as possible but couldn't be bothered to do something very clever like implimenting Barnes-Hut
#Every interaction only requires a particles position and one trait of the particles so the helper function takes an inner function which does the math and the name of the trait and a constant which the inner function requires
def all_particles(dt, particles, trait, inner_fn, constant):
    n = len(particles)
    forces = [Vec(0,0) for _ in range(n)]

    for i in range(n):
        p1 = particles[i]
        p1_pos = p1.position
        V1 = getattr(p1, trait)
        for j in range(i+1,n):
            p2 = particles[j]
            p2_pos = p2.position
            V2 = getattr(p2, trait)
            dire=(p2_pos-p1_pos)
            r=dire.norm()
            f=inner_fn(dire, r, V1, V2, constant)
            forces[i] += f
            forces[j] -= f
    
    for p, f in zip(particles, forces):
        p.apply_force(dt,f)

#All inner functions add a small number to the divisor so that the math is accurate enough but dont end up with it dividing by almost zero in certain situations cus that causes very weird behaviour
def gravity_inner(dire, r, p1_mass, p2_mass, G):
    inv_r3 = 1/(r*r*r+1e-6)
    return G*p1_mass*p2_mass*inv_r3*dire

def gravitational_force(dt, particles, G=150):
    all_particles(dt, particles, "mass", gravity_inner, G)

def vanderwaals_inner(dire, r, R1, R2, A):
    inv_r3 = 1/(r*r*r*6*(R1+R2)+1e-6)
    return A*R1*R2*inv_r3*dire

def vanderwaals_force(dt, particles, A=100):
    all_particles(dt, particles, "radius", vanderwaals_inner, A)

def collision_inner(dire, r, R1, R2, k):
    if r > R1+R2:
        return Vec(0,0)
    inv_r = 1/(r+1e-6)
    return -k*(R1+R2-r)*inv_r*dire

#We have picked rather large values for the defualt value of k for collisions and circular arena because the more rigid colisions are more easy to intuit
def collision(dt, particles, k=1000000):
    all_particles(dt, particles, "radius", collision_inner, k)

#The wall_force function lacks default values because it doesn't really makes sense to have any default values
def wall_force(dt, particles, k, n, a):
    for p in particles:
        d = dot((p.position - a), n)
        if d < 0:
            p.apply_force(dt,-k*d*n)

def friction(dt, particles, friction_mag=0.5):
    for p in particles:
        speed = p.velocity.norm()
        if speed < 1e-6:
            p.velocity = 0*p.velocity
            continue
        direction = 1/speed*p.velocity
        mass = getattr(p, 'mass')
        force_to_stop = (speed * mass) / dt
        applied_friction_mag = min(friction_mag, force_to_stop)
        friction_force = -applied_friction_mag*direction
        p.apply_force(dt, friction_force)

def drag(dt, particles, drag=0.01):
    for p in particles:
        p.apply_force(dt,-drag*p.velocity.norm()*p.velocity)

def circular_arena(dt, particles, k=1000000, R=10):
    for p in particles:
        r = p.position.norm()
        if R <= r:
            p.apply_force(dt, k*(R-r)/r*p.position)

#The coloumb force equation is basically the same thing as the gravity equation but with a negative constant (otherwise same charges attract) and charge instead of mass
def coulomb_force(dt, particles, k=100):
    all_particles(dt, particles, "charge", gravity_inner, -k)

def electromagnetic_field(dt, particles, B=10, mu=0.1):
    for p in particles:
        vx, vy = p.velocity.get_coords()
        pF = Vec(vy, -vx)
        p.apply_force(dt, mu*B*p.charge*pF)

def spring_force(dt, springs):
    for s in springs:
        s.force(dt)