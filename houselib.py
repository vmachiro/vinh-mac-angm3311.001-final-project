import maya.cmds as cmds

class House():

    def __init__(self):
        self.number_of_floors = 2        
        self.wall_height = 8 
        self.house_width = 8
        self.roof_height = 2 
        self.number_of_windows = 4
        self.window_height = 2
        self.window_width = 2
        self.number_of_doors = 2
    
    def get_height_of_house(self):
        house_height = self.wall_height * self.number_of_floors
        return house_height

    def get_base_of_house(self):
        base_height = self.wall_height/self.get_height_of_house() * self.number_of_floors
        return base_height

    def get_window_height_from_base(self):
        window_placement = self.wall_height/self.get_height_of_house() + (self.wall_height/2)
        return window_placement

    def get_center_of_wall(self):
        center_of_wall = self.house_width/2
        # This depends on the depth of the house body being equal to the width
        return center_of_wall
    
    def mkhousebody(self):
        print("Making your house!")
        xform, shape = cmds.polyCube(height= self.get_height_of_house(),
                                    width = self.house_width,
                                    depth = self.house_width,
                                    name = "housebody1")
        
        cmds.xform(xform, translation = [0,self.get_height_of_house()/2,0])          
        
        return xform

    def rotate_window(self, xform, windows_num):
        degrees = [0,90]

        world_pos = cmds.xform(xform, query=True, worldSpace=True, translation=True)

        is_rotated = windows_num%2
        world_pos[1] = degrees[is_rotated]
        cmds.xform( r=True, ro=(world_pos) )

        return is_rotated

    def mkwindows(self):
        print("Making windows...")
        floor_num=1


        for floor_num in range(self.number_of_floors):
            # TODO:
            # Move the windows up by a floor for every 2 windows.
            window_GRP = []

            for windows_num in range(self.number_of_windows):
                xform, shape = cmds.polyCube(height= self.window_height,
                                        width = self.window_width,
                                        depth = self.window_width/4,
                                        name = "window1")

                window_pos = cmds.xform(xform, query=True, worldSpace=True, translation=True)
                
                self.transform_window(xform)
                self.transform_window_up(xform, window_pos[1], floor_num)
                
                # Move the window to the back of the building every other window.
                if windows_num%2 == 1:
                    self.transform_window_to_back(xform, window_pos[2], floor_num)
                
                window_GRP.append(xform)
            
            cmds.group(window_GRP, name="windowsgrp1", parent="House1")
            window_GRP.clear()

            

    def mkdoors(self):
        print("Making doors...")
        door_GRP = []        
        
        for door_num in range(self.number_of_doors):
            xform, shape = cmds.polyCube(height= self.wall_height/4,
                                        width = self.house_width/10,
                                        depth = .5,
                                        name = "door1")
            
            self.transform_door(xform)
            
            if door_num > 0:
                self.transform_door_to_back(xform)
            
            door_GRP.append(xform)
            
            cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)   

        cmds.group(door_GRP, name="doors_GRP", parent="House1")
        
        return xform

    def mkhouseflatroof(self):
        print("Making the house's flat roof!")
        # This doesn't need to check if there's no roof because that'll be checked in the build function

        xform, shape = cmds.polyCube(height= self.roof_height,
                                    width = self.house_width*1.25,
                                    depth = self.house_width*1.25,
                                    name = "houseflatroof1")

        cmds.xform(xform, translation = [0,self.get_height_of_house(),0])

        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
        return xform
    
    def transform_door(self, door):
        print("Transforming door...")

        z_pos = self.get_center_of_wall()
        y_pos = self.get_base_of_house()
        pos = [0, y_pos, z_pos]

        cmds.xform(door, translation=pos)

    def transform_door_to_back(self, xform):
        z_pos = self.get_center_of_wall()
        y_pos = self.get_base_of_house()
        pos = [0, y_pos, z_pos*-1]

        cmds.xform(xform, translation=pos)

    def transform_window(self, window):
        print("Transforming windows...")

        z_pos = self.get_center_of_wall()
        y_pos = self.get_window_height_from_base()

        pos = [0, y_pos, z_pos]

        cmds.xform(window, translation=pos)

    def transform_window_up(self, window, window_y_pos, floor_num):
        print("Moving windows up a floor...")

        # z_pos = self.get_center_of_wall()
        y_pos = window_y_pos * floor_num
        
        # only changing one axis at a time. so what's a cmd that does that?
        # pos = [0, y_pos, z_pos]

        cmds.move( y_pos, y=True )


    def transform_window_to_back(self, window, window_z_pos, floor_num):
        print("Transforming windows to back...")

        z_pos = window_z_pos
        # y_pos = window_y_pos * floor_num

        # pos = [0, y_pos, z_pos*-1]

        #cmds.xform(window, translation=pos)

    def build(self):

        house_things = []

        housebody = self.mkhousebody()
        house_things.append(housebody)

        if self.roof_height != 0:
            # IF ROOF: Check what kind of roof. (DO THIS LATER)
            houseroof = self.mkhouseflatroof()
            house_things.append(houseroof)

        cmds.group(house_things, name="House1") 
        
        # Windows and doors are made after the HouseGRP because we declare parent when their groups are made

        doors_grp = self.mkdoors()
        house_things.append(doors_grp) 
        
        windows_grp = self.mkwindows()
        house_things.append(windows_grp)

        """cmds.makeIdentity("House1", apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)   """

     
    
if __name__ == "__main__":
    pass
     