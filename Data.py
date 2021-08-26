from shapely.geometry import Point, LinearRing, LineString, Polygon

class Data:
    def __init__(self):
        with open('Data/TA001.txt') as f:
            contents = f.read()
            print(contents)
            
        
        line = Polygon([Point(0,240),Point(0,0),Point(386,0),Point(660,162),Point(660,314),Point(374,428),Point(136,428)])
        line2 = Polygon([Point(0,310),Point(0,0),Point(422,0),Point(422,318)])
        print(line2.area)