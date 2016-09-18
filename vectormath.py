import math



def magnitude(v):
    return math.hypot(v[0], v[1])
    
def normalize(v):
    mag = magnitude(v)
    norm_v = [v[0]/mag, v[1]/mag]
    return norm_v
    
def add(v, u):
    return [(a+b) for (a, b) in zip(v, u)]

def subtract(v, u):
    return [(a-b) for (a, b) in zip(v, u)]
    
def distance(v, u):
    return math.hypot(subtract(v, u))
    
def direction(v, u):
    """
    Normalizes if direction is at 45 degrees.
    """
    diff = subtract(v, u)
    dist = distance(v, u)
    direction = [diff[0]/dist, diff[1]/dist]
    if all(direction):
        direction = [direction[0]/math.sqrt(2), direction[1]/math.sqrt(2)]
    return direction
    
def dot_product(v, u):
    return sum((a*b) for a, b in zip(v, u))
    
def angle(v1, v2):
    return math.acos(dot_product(v1, v2) / (magnitude(v1)*magnitude(v2)))

