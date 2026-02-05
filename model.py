import math

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
        return math.sqrt(self.x**2 + self.y**2)
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
    def inertial_move(self, dt):
        self.position += dt*self.velocity
    def apply_force(self, dt, f):
        self.velocity += dt/self.mass*f
    def bounding_box(self):
        topl=Vec(self.position.x-self.radius,self.position.y+self.radius)
        botr=Vec(self.position.x+self.radius,self.position.y-self.radius)
        return (topl,botr)

def constant_gravitational_field(dt, particles, g=10):
    d = Vec(0, -1)
    for p in particles:
        p.apply_force(dt, g*p.mass*d)

def gravitational_force(dt, particles, G=150):
    n = len(particles)
    forces = [Vec(0,0) for _ in range(n)]

    for i in range(n):
        p1 = particles[i]
        p1_pos = p1.position
        p1_mass = p1.mass
        for j in range(i+1,n):
            p2 = particles[j]
            p2_pos = p2.position
            p2_mass = p2.mass
            dire=(p2_pos-p1_pos)
            r=dire.norm()
            inv_r3 = 1/(r*r*r)
            f=G*p1_mass*p2_mass*inv_r3*dire
            forces[i] += f
            forces[j] -= f
    
    for p, f in zip(particles, forces):
        p.apply_force(dt,f)

def vanderwaals_force(dt, particles, A=100):
    n = len(particles)
    forces = [Vec(0,0) for _ in range(n)]

    for i in range(n):
        p1 = particles[i]
        p1_pos = p1.position
        R1 = p1.radius
        for j in range(i+1,n):
            p2 = particles[j]
            p2_pos = p2.position
            R2 = p2.radius
            dire=(p2_pos-p1_pos)
            r=dire.norm()
            inv_r3 = 1/(r*r*r*6*(R1+R2))
            f=A*R1*R2*inv_r3*dire
            forces[i] += f
            forces[j] -= f
    
    for p, f in zip(particles, forces):
        p.apply_force(dt,f)


def collision(dt, particles, k=1000000):
    n = len(particles)
    forces = [Vec(0,0) for _ in range(n)]

    for i in range(n):
        p1 = particles[i]
        p1_pos = p1.position
        R1 = p1.radius
        for j in range(i+1,n):
            p2 = particles[j]
            p2_pos = p2.position
            R2 = p2.radius
            dire=(p2_pos-p1_pos)
            r=dire.norm()
            if r > R1+R2:
                continue
            inv_r = 1/r
            f=k*(R1+R2-r)*inv_r*dire
            forces[i] -= f
            forces[j] += f
    
    for p, f in zip(particles, forces):
        p.apply_force(dt,f)

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