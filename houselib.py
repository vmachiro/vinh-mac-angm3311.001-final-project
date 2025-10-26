import maya.cmds as cmds

# house model is specifically for environment bg population, not for interior map level exploration, so there will not be multiple walls or a floor
class House():

    def __init__(self):
        self.number_of_floors = 1        
        self.wall_height = 8 
        self.house_width = 8
        self.roof_height = 4 
        self.number_of_windows = 4
        self.window_height = 2
        self.window_width = 2
        self.number_of_doors = 1
        self.door_height = 2
        self.door_width = 1
    
    def get_height_of_house(self):
        house_height = self.wall_height * self.number_of_floors
        return house_height

    def get_window_height_from_base(self):
        # TODO:
        # If more than one floor: Find lowest point of the house
        window_placement = self.wall_height/self.get_height_of_house() + (self.wall_height/2)
        return window_placement

    def get_center_of_wall(self):
        center_of_wall = self.house_width/2
        return center_of_wall
    
    def mkhousebody(self):
        print("Making your house!")
        xform, shape = cmds.polyCube(height= self.get_height_of_house(),
                                    width = self.house_width,
                                    depth = self.house_width,
                                    name = "housebody")
        
        cmds.xform(xform, translation = [0,self.wall_height/2,0])          

        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)   
        
        return xform

    def mkwindows(self):
        print("Making windows...")
        window_GRP = []

        for windows_num in range(self.number_of_windows):
            xform, shape = cmds.polyCube(height= self.window_height,
                                        width = self.window_width,
                                        depth = .5,
                                        name = "window1")
            self.transform_window(xform)        

            cmds.select(xform)
            cmds.rotate( 0, '90deg', 0, r=True )    

            window_GRP.append(xform)

        cmds.group(window_GRP, name="windows_GRP", parent="House1_GRP")
        
        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)  

    def mkdoors(self):
        print("Making doors...")
        door_GRP = []        
        
        for door_num in range(self.number_of_doors):
            xform, shape = cmds.polyCube(height= self.door_height,
                                        width = self.door_width,
                                        depth = .5,
                                        name = "door1")
            
            self.transform_door(xform)

            cmds.select(xform)
            cmds.rotate( 0, '90deg', 0, r=True )

            door_GRP.append(xform)

        cmds.group(door_GRP, name="doors_GRP", parent="House1_GRP")
        
        return xform

    def mkhouseflatroof(self):
        print("Making the house's flat roof!")
        # This is a separate method so that the user can choose not to have a roof in the menu
        # This doesn't need to check if there's no roof because that'll be checked in the build function

        xform, shape = cmds.polyCube(height= self.roof_height/4,
                                    width = self.house_width*1.25,
                                    depth = self.house_width*1.25,
                                    name = "houseflatroof")

        cmds.xform(xform, translation = [0,self.wall_height,0])

        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
        return xform
    
        # No roof_width because we're depending on house body width
        # Tranform the cube according to width of the house to have an overhang.
    
    def mkhousetriangleroof(self):
        print("Making the house's pointy roof!")
        
        # This is a separate method so that the user can choose not to have a roof in the menu
        # This should have options whether to be triangular or flat roof
        
        # TODO:
        # This doesn't need to check if there's no roof because that'll be checked in the build function
        # This is the same thing as flat roof, but diff poly
    
    def transform_door(self, door):
        print("Transforming door...")

        x_pos = self.get_center_of_wall()
        y_pos = self.wall_height/self.get_height_of_house()
        pos = [x_pos, y_pos, 0]

        cmds.xform(door, translation=pos)

    def transform_window(self, window):
        # TODO:
        # Take the distance from base for window height placement
        print("Transforming windows...")

        x_pos = self.get_center_of_wall()
        y_pos = self.get_window_height_from_base()

        pos = [x_pos, y_pos, 0]
        cmds.xform(window, translation=pos)


    def build(self):

        house_things = []

        housebody = self.mkhousebody()
        house_things.append(housebody)

        if self.roof_height != 0:
            # IF ROOF: Check what kind of roof. (DO THIS LATER)
            # Create the roof (set to flatroof for now bc easier)
            houseroof = self.mkhouseflatroof()
            house_things.append(houseroof)

        cmds.group(house_things, name="House1_GRP") 
        
        # Windows and doors are made after the HouseGRP because we declare parent when their groups are made

        doors_grp = self.mkdoors()
        house_things.append(doors_grp) 
        
        windows_grp = self.mkwindows()
        house_things.append(windows_grp)
     
    
if __name__ == "__main__":
    pass
     