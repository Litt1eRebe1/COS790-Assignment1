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
        self.selection_heuristic = selection_heuristic
        selection_id = self.selection_heuristic.id
   
        if len(problem.used_objects) == 0: #Open new bin
            use_object = Object(1000, 1000)
            problem.used_objects.append(use_object)
        else:
            use_object = problem.used_objects[0] #else start at first object @TODO figure out if this is correct
        if selection_id != 3 and selection_id != 4:
            shape = self.selection_heuristic.applyHeuristic(problem)
            if id == 0: #  Bottom-Left (BLI).  The piece starts at the top right corner of
            # the object and it slides down and left with a sequence of movements until no other movement is possible
            # If the final position does not overlap the object boundaries
                
                
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectBLI(shape, problem.used_objects[o], problem)
                    if placed:
                        break
                    
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    self.placeShapeInObjectBLI(shape, use_object, problem)
           
            elif id == 1: # Constructive Approach (CA)
            # The heuristic starts by placing the first piece at the bottom
            # and left of the object. Then, the next piece is placed in one of the five positions:
            # (x,¯ 0),(0, y),(x ¯ , y),( ¯ x,¯ y)¯ and (x,y ¯ ), where x¯, x, y¯, and y are the maximum and minimum coordinates in x and y in relation to the first piece
            # Given that some positions might coincide, each position appears only once in the list.   
            #  For each position in the list, the next piece slides vertically and horizontally following down and left movements   
            #  Positions with overlapping pieces or exceeding the object dimensions are discarded
            #  All others are considered as candidate positions, and the one that places the piece deepest (bottom and left) is chosen
                shape = self.selection_heuristic.applyHeuristic(problem)
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectCA(shape, problem.used_objects[o], problem)
                    if placed:
                        break
                    
                if not placed:
                    use_object = Object(1000, 1000)
                    problem.used_objects.append(use_object)
                    self.placeShapeInObjectCA(shape, use_object, problem)
        
           
            else: # Constructive-Approach (Minimum Area) (CAA)
            # This is a modification of the previous
            # heuristic. The variation consists of selecting the best position from the list based on which
            # one yields the bounding rectangle with minimum area, containing all pieces, and that fits
            # in the bottom left corner of the object
                placed = False
                while placed == False:
                   
                    placed = True
        
        elif selection_id == 3: # # Filler + FFD. This places as many pieces as possible within the open objects.
            
            if id == 0: #  Bottom-Left (BLI).  The piece starts at the top right corner of
            # the object and it slides down and left with a sequence of movements until no other movement is possible
            # If the final position does not overlap the object boundaries
                while len(problem.shapes) > 0:
                      
                    shape = self.selection_heuristic.applyHeuristic(problem)
                    for o in range(0, len(problem.used_objects)):
                        placed = self.placeShapeInObjectBLI(shape, problem.used_objects[o], problem)
                        if placed:
                            break
                    
                    
                    if not placed:
                        use_object = Object(1000, 1000)
                        problem.used_objects.append(use_object)
                        self.placeShapeInObjectBLI(shape, use_object, problem)
          
            elif id == 1: # Constructive Approach (CA)
            # The heuristic starts by placing the first piece at the bottom
            # and left of the object. Then, the next piece is placed in one of the five positions:
            # (x,¯ 0),(0, y),(x ¯ , y),( ¯ x,¯ y)¯ and (x,y ¯ ), where x¯, x, y¯, and y are the maximum and minimum coordinates in x and y in relation to the first piece
            # Given that some positions might coincide, each position appears only once in the list.   
            #  For each position in the list, the next piece slides vertically and horizontally following down and left movements   
            #  Positions with overlapping pieces or exceeding the object dimensions are discarded
            #  All others are considered as candidate positions, and the one that places the piece deepest (bottom and left) is chosen
                while len(problem.shapes) > 0:
                    shape = self.selection_heuristic.applyHeuristic(problem)
                    for o in range(0, len(problem.used_objects)):
                        placed = self.placeShapeInObjectCA(shape, problem.used_objects[o], problem)
                        if placed:
                            break
                        
                    if not placed:
                        use_object = Object(1000, 1000)
                        problem.used_objects.append(use_object)
                        self.placeShapeInObjectCA(shape, use_object, problem)
                
             
            else: # Constructive-Approach (Minimum Area) (CAA)
            # This is a modification of the previous
            # heuristic. The variation consists of selecting the best position from the list based on which
            # one yields the bounding rectangle with minimum area, containing all pieces, and that fits
            # in the bottom left corner of the object
                placed = False
                while placed == False:
                    placed = True
                
        else: # Worst Fit (WF). It places the item in the opened object where it worst fits (that is, with the largest available room)
            
            if id == 0: #  Bottom-Left (BLI).  The piece starts at the top right corner of
            # the object and it slides down and left with a sequence of movements until no other movement is possible
            # If the final position does not overlap the object boundaries
                none = None
                    
            elif id == 1: # Constructive Approach (CA)
            # The heuristic starts by placing the first piece at the bottom
            # and left of the object. Then, the next piece is placed in one of the five positions:
            # (x,¯ 0),(0, y),(x ¯ , y),( ¯ x,¯ y)¯ and (x,y ¯ ), where x¯, x, y¯, and y are the maximum and minimum coordinates in x and y in relation to the first piece
            # Given that some positions might coincide, each position appears only once in the list.   
            #  For each position in the list, the next piece slides vertically and horizontally following down and left movements   
            #  Positions with overlapping pieces or exceeding the object dimensions are discarded
            #  All others are considered as candidate positions, and the one that places the piece deepest (bottom and left) is chosen
                shape = self.selection_heuristic.applyHeuristic(problem)
                for o in range(0, len(problem.used_objects)):
                    placed = self.placeShapeInObjectCA(shape, problem.used_objects[o], problem)
                    if placed:
                        break     
                        
                    if not placed:
                        use_object = Object(1000, 1000)
                        problem.used_objects.append(use_object)
                        self.placeShapeInObjectCA(shape, use_object, problem) 
               
            else: # Constructive-Approach (Minimum Area) (CAA)
            # This is a modification of the previous
            # heuristic. The variation consists of selecting the best position from the list based on which
            # one yields the bounding rectangle with minimum area, containing all pieces, and that fits
            # in the bottom left corner of the object
                placed = False
                while placed == False:
                   
                    placed = True
        
        return problem
    
    
    
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
    
    
        
        
        
        