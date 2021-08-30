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
                placed = False
                while placed == False:
                   
                    placed = True
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
                placed = False
                while placed == False:
                   
                    placed = True
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
                placed = False
                while placed == False:
                  
                    placed = True
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
            return transform(lambda x, y, z=None: (x-xp, y-yp), shape) 
        elif xp > 0 and yp < 0:
            return transform(lambda x, y, z=None: (x+xp, y-yp), shape) 
        elif xp < 0 and yp > 0:
            return transform(lambda x, y, z=None: (x-xp, y+yp), shape) 
        else:
            return transform(lambda x, y, z=None: (x+xp, y+yp), shape)
          
    
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
      
        fit_in_object = self.fitInObject(object, shape)
        
        if fit_in_object: #space in object
            fits = self.placeShapeInObjectTopRight(shape, object)
        else: #create new object
            new_object = Object(1000, 1000)
            fits = self.placeShapeInObjectTopRight(shape, new_object)
            problem.used_objects.append(new_object)
       
        return fits
        
    def placeShapeInObjectTopRight(self, shape, object):
        initial_fit = self.fitInObject(object, shape)
     
        collide = not initial_fit
        in_bound = True
        while not collide and in_bound: #Move down
            
            shape = self.moveDown(shape)
          
            collide = not self.fitInObject(object, shape)
            in_bound = self.insideBounds(1000, 1000, shape)
           
        shape = self.moveUp(shape)
        
        collide = not self.fitInObject(object, shape)
        in_bound = True
        while not collide and in_bound: #Move left
            shape = self.moveLeft(shape)
            collide = not self.fitInObject(object, shape)
            in_bound = self.insideBounds(1000, 1000, shape)
        shape = self.moveRight(shape)
        
        if initial_fit:
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
    
    
        
        
        
        