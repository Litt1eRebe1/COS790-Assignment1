from shapely.geometry import Point, LinearRing, LineString, Polygon
from Object import Object

class Problem:
    def __init__(self, num_s, shapes, object_s, solution_fitness):
        self.num_shapes = num_s
        self.shapes = shapes
        self.object_size = object_s
        self.solution_fitness = solution_fitness
        self.used = False
        self.used_objects = []