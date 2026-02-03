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


