class Rect :   # a rectangle on the map. used to characterize a room ( create the dimenions )
    def __init__(self,x,y,w,h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h

        #The __init__ function takes the x and y coordinates of the top left corner,
        #and computes the bottom right corner based on the w and h parameters (width and height)

    def center (self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return (center_x, center_y)

     # This function gives us the center point of a rectangle

    def intersect (self, other):
    #returns true if this rectangel inersects with another one 
        return (self.x1 <= other.x2 and self.x2 >= other.x1 and 
                self.y1 <= other.y2 and self.y2 >= other.y1 )    
   
   # This tell us if two rectangle overlapse. 