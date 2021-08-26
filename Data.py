from shapely.geometry import Point, LinearRing, LineString, Polygon
from Problem import Problem

class Data:
    def __init__(self):
        self.problems = []
        
    def readData(self):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R']
        for l in letters:
            current_problems = self.readDataHelper(l)
            self.problems = self.problems + current_problems
            
           
    def readDataHelper(self,letter):
        current_problems = []
        filenameData = 'Data/T' + letter
        filenameOptimal = 'Data/OpT' + letter
        fileextension = '.txt'
        
        self.shapes = []
        self.num_shapes = 0
        self.objects_size = 0
        
        for i in range(1,31):
            self.shapes = []
            self.num_shapes = 0
            self.objects_size = 0
            self.solution_shapes = []
            self.objects_solution_size = 0
            self.object_arrangements = []
            
            int_countval = i
            string_countval = str(int_countval)
            string_countval = string_countval.zfill(3)
            
            file1 = open(filenameData+string_countval+fileextension, 'r')
            file2 = open(filenameOptimal+string_countval+fileextension, 'r')
            
            Lines = file1.readlines()
            Lines2 = file2.readlines()
            
            count = 0
            for line in Lines: #for each problem do the below
                count += 1
                
                
                if count == 1: #first line of file
                    self.num_shapes = int(line.strip())
                    
                elif count == 2: #size of objects
                    points = line.split()
                    self.objects_size = int(points[0]) * int(points[1])
                
                else:
                    points = line.split()
                    points.pop(0)
                    pointsArray = []
                    p = 0
                    while p < len(points):
                        pointsArray.append(Point(int(points[p]),int(points[p+1])))
                        p = p + 2
                    self.shapes.append(Polygon(pointsArray))
            
             
            
            
            count = 0
            self.object_arrangements = []
            for line in Lines2: #for each solution do the below
                count += 1
            
                if count == 1: #first line of file
                    line1 = line.split()
                    self.num_objects = int(line1.pop(0))
                    self.object_arrangements = line1
                    
                elif count == 2: #size of objects
                    points = line.split()
                    self.objects_solution_size = int(points[0]) * int(points[1])
                
                else:
                    points = line.split()
                    points.pop(0)
                    pointsArray = []
                    p = 0
                    while p < len(points):
                        pointsArray.append(Point(int(points[p]),int(points[p+1])))
                        p = p + 2
                    
                  
                    self.solution_shapes.append(Polygon(pointsArray))
            
            num = 0
            current_fit = 0
            total_area = 0
            for a in self.object_arrangements: #Go through each arrangement and get area
                current_area = 0

                for n in range(0, int(a)):
                    current_area = current_area + self.solution_shapes[num].area
                    num = num + 1
                    
                total_area = total_area + ( current_area / self.objects_solution_size)
                
            
            current_fit = total_area
           
            current_fit = (current_fit) / self.num_objects
                
            current_problems.append(Problem(self.num_shapes, self.shapes, self.objects_size, current_fit))    

        return current_problems      
                   
                    
              