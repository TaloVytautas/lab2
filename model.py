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
    for p1 in particles:
        fsum=Vec(0,0)
        for p2 in particles:
            dire=(p2.position-p1.position)
            r=dire.norm()
            if r==0:
                continue
            F2=G*p1.mass*p2.mass/r**3*dire
            fsum+=F2
        p1.apply_force(dt, fsum)

def vanderwaals_force(dt, particles, A=100):
    for p1 in particles:
        fsum=Vec(0,0)
        for p2 in particles:
            dire=(p2.position-p1.position)
            r=dire.norm()
            R1 = p1.radius
            R2 = p2.radius
            if r==0:
                continue
            F2=A*R1*R2/((R1+R2)*6*r**3)*dire
            fsum+=F2
        p1.apply_force(dt, fsum)

def collision(dt, particles, k=1000000):
    for p1 in particles:
        fsum=Vec(0,0)
        for p2 in particles:
            dire=(p2.position-p1.position)
            R1 = p1.radius
            R2 = p2.radius
            r=dire.norm()
            if r > R1+R2:
                continue
            if r==0:
                continue
            F2=-k*(R1+R2-r)/r*dire
            fsum+=F2
        p1.apply_force(dt, fsum)


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