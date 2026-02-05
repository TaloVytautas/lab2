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

def collision(dt, particles, k=1000000):
    all_particles(dt, particles, "radius", collision_inner, k)

def wall_force(dt, particles, k, n, a):
    for p in particles:
        d = dot((p.position - a), n)
        if d < 0:
            p.apply_force(dt,-k*d*n)

def friction(dt, particles, friction=0.5):
    for p in particles:
        p.apply_force(dt,-friction*p.velocity)

def drag(dt, particles, drag=0.01):
    for p in particles:
        p.apply_force(dt,-drag*p.velocity.norm()*p.velocity)

def circular_arena(dt, particles, k=1000, R=10):
    for p in particles:
        r = p.position.norm()
        if R <= r:
            p.apply_force(dt, k*(R-r)/r*p.position)

#Coloumb kraft ekvationen är väldigt lik gravitationen men med en annan konstant och med repulsion med två positiva massor/laddningar så bass ekvationen är negativ
def coulomb_force(dt, particles, k=100):
    all_particles(dt, particles, "charge", gravity_inner, -k)

def electromagnetic_field(dt, particles, B, mu):
    for p in particles:
        vx, vy = p.velocity.get_coords()
        pF = Vec(vy, -vx)
        p.apply_force(dt, mu*B*p.charge*pF)

def spring_force(dt, springs):
    for s in springs:
        s.force(dt)