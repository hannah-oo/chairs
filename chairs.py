#coding:utf-8
import rhinoscriptsyntax as rs
import random
import math

class Chair:
    # setup
    def __init__(self):
        # x = length, y = width, z = depth
        self.seat_x = random.randint(300,450)
        self.seat_y = random.randint(220,360)
        self.seat_z = random.randint(6,14)
        self.back_x = random.randint(200,330)
        self.back_y = random.randint(600,1000)
        self.back_z = random.randint(6,12)
        self.seat_angle = random.randint(-180, 0)
        self.back_angle = random.randint(450, 600)
        

    def drawBox(self, corners, position, color = None):
        id = rs.AddBox(corners)
        rs.MoveObject(id, position)
        if color != None:
            rs.ObjectColor(id, color)
        else:   
            black = rs.CreateColor(0,0,0)
            rs.ObjectColor(id,black)
            
        return id
    
    def makeBoxCorners(self, origin, x, y, z, type):
        # for long blocks
        if type == 0:
            corners = [[0,0,0],[x,0,0],[x,y,0],[0,y,0],[0,0,z],[x,0,z],[x,y,z],[0,y,z]]
        # for seat
        elif type == 1:
            corners = [[0,0,0],[x,0,0],[x,y,self.seat_angle],[0,y,self.seat_angle],[0,0,z],[x,0,z],[x,y,z+self.seat_angle],[0,y,z+self.seat_angle]]
        # for back
        elif type == 2:
            corners = [[0,0,0],[x,0,0],[x,y-self.back_angle,self.back_angle],[0,y-self.back_angle,self.back_angle],[0,0,z],[x,0,z],[x,y-self.back_angle,z+self.back_angle],[0,y-self.back_angle,z+self.back_angle]]

        for i,corner in enumerate(corners):
            corners[i] = rs.VectorAdd(origin, corner)

        return corners

    def drawChair(self, startpos):
        # Left Front Leg
        leg_z = 330 + self.seat_z
        corners = self.makeBoxCorners([0,0,0], 30, 30, leg_z,0)
        id = self.drawBox(corners, startpos)

        # Right Front Leg
        corners = self.makeBoxCorners([max(self.back_x,self.seat_x)+30,0,0],30,30,leg_z,0)
        id = self.drawBox(corners, startpos)
        
        # Left Back Leg
        leg_z = self.back_y
        leg_y_start = self.seat_y - 10 + (self.back_y/2) - 150
        corners = self.makeBoxCorners([0,leg_y_start,0], 30,30,470,0)
        id = self.drawBox(corners, startpos)

        # Right Back Leg
        corners = self.makeBoxCorners([max(self.back_x,self.seat_x)+30,leg_y_start,0], 30,30,470,0)
        id = self.drawBox(corners, startpos)
        
        # Left Armrest
        corners = self.makeBoxCorners([-30,leg_y_start+40, 470],90,-430,30,0)
        id = self.drawBox(corners, startpos)
        
        # Right Armrest
        corners = self.makeBoxCorners([max(self.back_x, self.seat_x), leg_y_start+40, 470],90,-430,30,0)
        id = self.drawBox(corners, startpos)
        
        # Left Armrest Post
        armrest_y_start = (leg_y_start+20)/2 
        corners = self.makeBoxCorners([0, armrest_y_start, 40], 30,30,430,0)
        id = self.drawBox(corners, startpos)
        
        # Right Armrest Post
        corners = self.makeBoxCorners([max(self.back_x,self.seat_x)+30, armrest_y_start ,40], 30,30,430,0)
        id = self.drawBox(corners, startpos)

        # Back Batten
        batten_y_start = (leg_y_start+20)/2 + ((armrest_y_start+self.back_y)/2)
        corners = self.makeBoxCorners([-70,leg_y_start-30,440],max(self.back_x,self.seat_x)+180,30,30,0)
        id = self.drawBox(corners,startpos)
        
        # Left Long Rail
        corners = self.makeBoxCorners([0, leg_y_start+65, leg_y_start * 1/5], 30, -(leg_y_start+100),30,0)
        id = self.drawBox(corners, startpos)

        # Right Long Rail
        corners = self.makeBoxCorners([max(self.back_x, self.seat_x)+30, leg_y_start+65, leg_y_start * 1/5], 30, -(leg_y_start+100),30,0)
        id = self.drawBox(corners, startpos)
        
        # Seat
        corners = self.makeBoxCorners([50,0,300],self.seat_x,self.seat_y,self.seat_z,1)
        seat_id = self.drawBox(corners,startpos, rs.CreateColor(4, 55, 242))
    
        # Back 
        corners = self.makeBoxCorners([50,armrest_y_start,300+self.seat_angle-50],self.back_x,self.back_y,self.back_z,2)
        back_id = self.drawBox(corners,startpos, rs.CreateColor(227, 66, 52))
        
        # Crossrail (the one near the origin and under the seat)
        corners = self.makeBoxCorners([-30,30,250],(max(self.seat_x,self.back_x))+120,30,30,0)
        id = self.drawBox(corners,startpos)
        
        # Crossrail (the one further from origin and under the seat)
        corners = self.makeBoxCorners([-30,armrest_y_start,self.seat_angle+300-30],(max(self.seat_x,self.back_x))+120,30,30,0)
        id = self.drawBox(corners,startpos)
        
        # Crossrail (the one near the origin and not connected to the seat)
        corners = self.makeBoxCorners([-30, 30, (leg_y_start * 1/5) + 30],(max(self.seat_x,self.back_x))+120, 30,30, 0)
        id = self.drawBox(corners,startpos)
        
        # Crossrail (the one under back)
        corners = self.makeBoxCorners([-30,armrest_y_start+30, 300+self.seat_angle-70],(max(self.seat_x,self.back_x))+120, 30,30, 0)
        id = self.drawBox(corners,startpos)
        

# draw 100 chairs
for x in range(10):
    for y in range(10):   
        chair = Chair()
        chair.drawChair([x*1000,y*1000,0])
    

    