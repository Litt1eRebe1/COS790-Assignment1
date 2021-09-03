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
        
    def copy(self):
        new_shapes = []
        
        for s in self.shapes:
            new_shape = Polygon(s)
            new_shapes.append(new_shape)
            
        new_obj = Object(1000, 1000)
        problem_copy = Problem(self.num_shapes, new_shapes, 1000*1000, self.solution_fitness)
        return problem_copy