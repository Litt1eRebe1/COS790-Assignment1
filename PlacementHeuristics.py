from functools import total_ordering
import random
from re import T
from Object import Object
from shapely.ops import transform
from shapely.geometry import Point, LinearRing, LineString, Polygon

class PlacementHeuristics:
    def __init__(self, id, seed):
        self.id = id
        self.seed = seed
        random.seed(self.seed)  #random.random()
        
    def applyHeuristic(self, problem, selection_heuristic):
     
        id = self.id
        if id > 2:
            id = 1
            
        self.selection_heuristic = selection_heuristic
        selection_id = self.selection_heuristic.id
        
       
   
        if len(problem.used_objects) == 0: #Open new bin
            use_object = Object(1000, 1000)
            problem.used_objects.append(use_object)
        else:
            use_object = problem.used_objects[0] #else start at first object @TODO figure out if this is correct
        if selection_id < 3:
            shape = self.selection_heuristic.applyHeuristic(problem)
            if id == 0: #  Bottom-Left (BLI).  The piece starts at the top right corner of
               
                
                
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectBLI(shape, problem.used_objects[o], problem)
                    if placed:
                        break
                    
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    placed = self.placeShapeInObjectBLI(shape, use_object, problem)
                
           
            elif id == 1: # Constructive Approach (CA)
         
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectCA(shape, problem.used_objects[o], problem)
                    if placed:
                        break
                    
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    placed = self.placeShapeInObjectCA(shape, use_object, problem)
                    
               
        
           
            else: # Constructive-Approach (Minimum Area) (CAA)
             
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectCAA(shape, problem.used_objects[o], problem)
                    if placed:
                        break     
                        
              
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    placed = self.placeShapeInObjectCAA(shape, use_object, problem)
                    
                
        
        elif selection_id == 3: # # Filler + FFD. This places as many pieces as possible within the open objects.
            
            if id == 0: #  Bottom-Left (BLI).  The piece starts at the top right corner of
         
                while len(problem.shapes) > 0:
                    
                    shape = self.selection_heuristic.applyHeuristic(problem)
                    for o in range(0, len(problem.used_objects)):
                        placed = self.placeShapeInObjectBLI(shape, problem.used_objects[o], problem)
                        if placed:
                            break
                    
                    
                    if not placed:
                        use_object = Object(1000, 1000)
                        problem.used_objects.append(use_object)
                        placed = self.placeShapeInObjectBLI(shape, use_object, problem)
                       
                    
          
            elif id == 1: # Constructive Approach (CA)
          
                # while len(problem.shapes) > 0:
             
                #     shape = self.selection_heuristic.applyHeuristic(problem)
                #     for o in range(0, len(problem.used_objects)):
                #         placed = self.placeShapeInObjectCA(shape, problem.used_objects[o], problem)
                #         if placed:
                #             break
                 
                #     if not placed:
                #         use_object = Object(1000, 1000)
                #         problem.used_objects.append(use_object)
                #         placed = self.placeShapeInObjectCA(shape, use_object, problem)
                
                while len(problem.shapes) > 0:
                    
                    shape = self.selection_heuristic.applyHeuristic(problem)
                    for o in range(0, len(problem.used_objects)):
                        placed = self.placeShapeInObjectBLI(shape, problem.used_objects[o], problem)
                        if placed:
                            break
                    
                    
                    if not placed:
                        use_object = Object(1000, 1000)
                        problem.used_objects.append(use_object)
                        placed = self.placeShapeInObjectBLI(shape, use_object, problem)

                    
             
            else: # Constructive-Approach (Minimum Area) (CAA)
              
                shape = self.selection_heuristic.applyHeuristic(problem)
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectCAA(shape, problem.used_objects[o], problem)
                    if placed:
                        break
                   
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    placed = self.placeShapeInObjectCAA(shape, use_object, problem)
                   
                    
                
        else: # Worst Fit (WF). It places the item in the opened object where it worst fits (that is, with the largest available room)
         
            if id == 0: #  Bottom-Left (BLI).  The piece starts at the top right corner of
           
                worst_area = 1
                worst_shape = None
                for s in range(0, len(problem.shapes) - 1):
                    
                    
                    shape = self.selection_heuristic.applyHeuristic(problem)
                
                    for o in range(0, len(problem.used_objects)):
                        used_area = self.placeShapeInObjectBLITemp(shape, problem.used_objects[o], problem)
                        if used_area > 0:
                            break
                        
                        
                    if used_area < 0:
                        use_object = Object(1000, 1000)
                        # problem.used_objects.append(use_object)
                        used_area = self.placeShapeInObjectBLITemp(shape, use_object, problem)
                    if used_area < worst_area:
                        worst_shape = shape
                        worst_area = used_area
                        
                
                self.removeShapeFromProblem(worst_shape, problem)
                use_object.shapes.append(worst_shape)
          
            elif id == 1: # Constructive Approach (CA)
           
                shape = self.selection_heuristic.applyHeuristic(problem)
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectCA(shape, problem.used_objects[o], problem)
                    if placed:
                        break
                 
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    placed = self.placeShapeInObjectCA(shape, use_object, problem) 
                    
               
               
            else: # Constructive-Approach (Minimum Area) (CAA)
           
                shape = self.selection_heuristic.applyHeuristic(problem)
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectCAA(shape, problem.used_objects[o], problem)
                    if placed:
                        break     
                        
         
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    placed = self.placeShapeInObjectCAA(shape, use_object, problem) 
                
                
        
        return problem
    
    def removeShapeFromProblem(self, shape,problem):
        temp_shapes = []
     
        for s in problem.shapes:
            if shape.equals(s) == False:
                temp_shapes.append(s)
        problem.shapes = temp_shapes
   
    
    def placeShapeInObjectBLITemp(self, shape, object_p, problem):
        object = object_p
        in_y = self.insideBounds(1000, 1000, shape)
      
        while in_y == True:
            shape = self.moveUp(shape)
            in_y = self.insideBounds(1000, 1000, shape)
        shape = self.moveDown(shape)
        
        in_x = True
        while in_x == True:
            shape = self.moveRight(shape)
            in_x = self.insideBounds(1000, 1000, shape)
        shape = self.moveLeft(shape)
      
        fit_in_object = self.legalPlacement(shape, object)
        
        if fit_in_object: #space in object
            fits = self.placeShapeInObjectTopRight(shape, object)
        else: #create new object
            fits =  False
            
        if fits == True:
            return -1
        else:
            area = self.calculateAreaPercentage(object)
      
            return area
    
    def calculateAreaPercentage(self, object):
        total_area = 0
        for s in object.shapes:
            total_area = total_area + s.area
        return total_area / (1000 * 1000)
            
    
    def determineBoundingArea(self, shape, object):

        high_coords = []
        temp_shapes = object.shapes
        temp_shapes.append(shape)
        for s in temp_shapes:
            if len(high_coords) == 0:
                high_coords.append(s.bounds[2])
                high_coords.append(s.bounds[3])
            if s.bounds[2] > high_coords[0]:
                high_coords[0] = s.bounds[2]
            if s.bounds[3] > high_coords[1]:
                high_coords[1] = s.bounds[3]
                
        bound = Polygon([Point(0,0), Point(high_coords[0], 0), Point(high_coords[0], high_coords[1]), Point(0, high_coords[1])])
      
        return bound.area
            
            
    
    def placeShapeInObjectCAA(self, shape, object, point):
        placed = False
        # move to point
        if len(object.shapes) == 0:
            in_y = self.insideBounds(1000, 1000, shape)
        
            while in_y == True:
                shape = self.moveDown(shape)
                in_y = self.insideBounds(1000, 1000, shape)
            shape = self.moveUp(shape)
            
            in_x = True
            while in_x == True:
                shape = self.moveLeft(shape)
                in_x = self.insideBounds(1000, 1000, shape)
            shape = self.moveRight(shape)
            
            object.shapes.append(shape)
            placed = True
        else:
            points = self.calculateCAPoints(object)
        
            #find lowest point of shape
            lowest_point = [shape.bounds[0], shape.bounds[1]]

            
            accept = False
            small_point = []
            small_area = 1000 * 1000
            place_true = False
            for p in points:
                if accept == True:
                    break
                    
                point_to_move_to = p
                
                if lowest_point[0] > point_to_move_to[0]: #needs to move down
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveDown(shape)
                else: #needs to move up
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveUp(shape)
            
                if lowest_point[1] > point_to_move_to[1]: #needs to move left
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveLeft(shape)
                else: #needs to move right
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveRight(shape)
                accept = True
                
                
                
                
                
                if len(small_point) == 0:
                    small_point = p
                else:
                    if self.determineBoundingArea(shape, object) < small_area:
                        small_area = self.determineBoundingArea(shape, object)
                        small_point = p
                    
                    
        
            place_true = self.legalPlacement(shape, object)
            point_to_move_to = small_point
           
            placed = False
            if place_true == True:
                if lowest_point[0] > point_to_move_to[0]: #needs to move down
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveDown(shape)
                else: #needs to move up
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveUp(shape)
                
                if lowest_point[1] > point_to_move_to[1]: #needs to move left
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveLeft(shape)
                else: #needs to move right
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveRight(shape)
                accept = True
                    
                place_true = self.legalPlacement(shape, object)       

                if not place_true:
                    accept = False 
                else:
                    object.shapes.append(shape)
                    placed = True
        return placed 
        
    
    def getRandomInt(self, a, b):
        return random.randint(a, b) 
    
    def moveXY(self, shape, xp, yp):
        
        if xp < 0 and yp < 0:
            return transform(lambda x, y, z=None: (x-float(xp), y-float(yp)), shape) 
        elif xp > 0 and yp < 0:
            return transform(lambda x, y, z=None: (x+float(xp), y-float(yp)), shape) 
        elif xp < 0 and yp > 0:
            return transform(lambda x, y, z=None: (x-float(xp), y+float(yp)), shape) 
        else:
            return transform(lambda x, y, z=None: (x+float(xp), y+float(yp)), shape)
        
    
    def moveDown(self, shape):
        return transform(lambda x, y, z=None: (x+0.0, y-1.0), shape)
    
    def moveLeft(self, shape):
        return transform(lambda x, y, z=None: (x-1.0, y-0.0), shape)
    
    def moveUp(self, shape):
        return transform(lambda x, y, z=None: (x-0.0, y+1.0), shape)
    
    def moveRight(self, shape):
        return transform(lambda x, y, z=None: (x+1.0, y+0.0), shape)
    
    def moveToTop(self, shape):
        none = None
    
    def placeShapeInObjectBLI(self, shape, object, problem):
        in_y = self.insideBounds(1000, 1000, shape)
      
        while in_y == True:
            shape = self.moveUp(shape)
            in_y = self.insideBounds(1000, 1000, shape)
        shape = self.moveDown(shape)
        
        in_x = True
        while in_x == True:
            shape = self.moveRight(shape)
            in_x = self.insideBounds(1000, 1000, shape)
        shape = self.moveLeft(shape)
      
        fit_in_object = self.legalPlacement(shape, object)
        
        if fit_in_object: #space in object
            fits = self.placeShapeInObjectTopRight(shape, object)
        else: #create new object
            fits =  False
       
        return fits
    
    def placeShapeInObjectCATemp(self, shape, object_temp, problem):
        object = object_temp
        placed = False
        if len(object.shapes) == 0:
            in_y = self.insideBounds(1000, 1000, shape)
        
            while in_y == True:
                shape = self.moveDown(shape)
                in_y = self.insideBounds(1000, 1000, shape)
            shape = self.moveUp(shape)
            
            in_x = True
            while in_x == True:
                shape = self.moveLeft(shape)
                in_x = self.insideBounds(1000, 1000, shape)
            shape = self.moveRight(shape)
            
            object.shapes.append(shape)
            placed = True
            if not placed == True:
                return -1
            else:
                area = self.calculateAreaPercentage(object)  
        else:
            points = self.calculateCAPoints(object)
       
            #find lowest point of shape
            lowest_point = [shape.bounds[0], shape.bounds[1]]
          
            accept = False
            for p in points:
                if accept == True:
                    break
                
                point_to_move_to = p
              
                if lowest_point[0] > point_to_move_to[0]: #needs to move down
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveDown(shape)
                else: #needs to move up
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveUp(shape)
          
                if lowest_point[1] > point_to_move_to[1]: #needs to move left
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveLeft(shape)
                else: #needs to move right
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveRight(shape)
                accept = True
              
                for s in object.shapes:
                    place_true = self.legalPlacement(shape, object)
               
                    if not place_true:
                        accept = False 
                        break
                    else:
                        object.shapes.append(shape)
                        placed = True
                    
            if not placed == True:
                return -1
            else:
                area = self.calculateAreaPercentage(object)     
            
            #move shape to one of the points
        return area
    
    def placeShapeInObjectCA(self, shape, object, problem):
        placed = False
        if len(object.shapes) == 0:
            in_y = self.insideBounds(1000, 1000, shape)
        
            while in_y == True:
                shape = self.moveDown(shape)
                in_y = self.insideBounds(1000, 1000, shape)
            shape = self.moveUp(shape)
            
            in_x = True
            while in_x == True:
                shape = self.moveLeft(shape)
                in_x = self.insideBounds(1000, 1000, shape)
            shape = self.moveRight(shape)
            
            object.shapes.append(shape)
            placed = True
        else:
            points = self.calculateCAPoints(object)
       
            #find lowest point of shape
            lowest_point = [shape.bounds[0], shape.bounds[1]]
          
            accept = False
            for p in points:
                if accept == True:
                    break
                
                point_to_move_to = p
              
                if lowest_point[0] > point_to_move_to[0]: #needs to move down
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveDown(shape)
                else: #needs to move up
                    distance = point_to_move_to[0] - lowest_point[0]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveUp(shape)
          
                if lowest_point[1] > point_to_move_to[1]: #needs to move left
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveLeft(shape)
                else: #needs to move right
                    distance = point_to_move_to[1] - lowest_point[1]
                    for r in range(0, int(distance) - 1):
                        shape = self.moveRight(shape)
                accept = True
              
                for s in object.shapes:
                    place_true = self.legalPlacement(shape, object)
               
                    if not place_true:
                        accept = False 
                        break
                    else:
                        object.shapes.append(shape)
                        placed = True
            #move shape to one of the points
        return placed
    
    def legalPlacement(self, shape, object):
        
        object_shape = Polygon([Point(0, 0), Point(1000, 0), Point(1000, 1000), Point(1000, 0)])
        valid = True
        in_obj = object_shape.contains(shape)
      
        if in_obj:
            for s in object.shapes:
                
                if not s.disjoint(shape):
                    valid = False
                    break
            return valid
        else:
            return False
        
    def calculateCAPoints(self, object):
        points = []
        for s in object.shapes:
            x0, y0, x1, y1 = s.bounds[0], s.bounds[1], s.bounds[2], s.bounds[3]
            points.append( [0, y1])
            # points.append([x0, y0])
            points.append( [x1, y1])
            points.append( [x1, 0])
            
        
        new_points = []
        for s in object.shapes:
            
            for p in points:
                if s.disjoint(Point(p[0], p[1])):
                    new_points.append(p)

        
        return new_points      
        
    def placeShapeInObjectTopRight(self, shape, object):
      
        collide = False
        while not collide: #Move down
            shape = self.moveDown(shape)
            collide = not self.legalPlacement(shape, object)
    
        shape = self.moveUp(shape)
        
        collide = not self.legalPlacement(shape, object)
        while not collide: #Move left
            shape = self.moveLeft(shape)
            collide = not self.legalPlacement(shape, object)

        shape = self.moveRight(shape)
        if self.legalPlacement(shape, object):
            object.shapes.append(shape)
            return True
        else:
            return False
        
    def fitInObject(self, object, shape):
        collide = False
        for s in object.shapes:
           collide = s.intersects(shape) 
        return not collide  
        
    def insideBounds(self, x, y, shape):
        y_bound = y
        x_bound = x
        bounds = Polygon([[0, 0], [0, y_bound], [x_bound, y_bound], [x_bound, 0]])
        inside = shape.within(bounds)
        return inside
    
    
        
        
        
        