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
        window_placement = self.wall_height/self.get_height_of_house() + (self.wall_height/2)
        return window_placement

    def get_center_of_wall(self):
        center_of_wall = self.house_width/2
        return center_of_wall
    
    def set_pivot_to_house_origin(self,xform):
        print("Setting pivot of the current window...")

        position = cmds.xform('housebody', query=True, translation=True, worldSpace=True)
        print(f"World Space Position of {'housebody'}: {position}")

        cmds.manipPivot(p=position)

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
        degrees = [0,90]

        for windows_num in range(self.number_of_windows):
            xform, shape = cmds.polyCube(height= self.window_height,
                                        width = self.window_width,
                                        depth = self.door_width/4,
                                        name = "window1")
            cmds.select(xform)
            self.set_pivot_to_house_origin(xform)

            rotation = cmds.xform(xform, query=True, worldSpace=True, translation=True)
            rotation[1] = degrees[windows_num%2]
            cmds.xform( r=True, ro=(rotation) )

            self.transform_window(xform)        

            window_GRP.append(xform)

        cmds.group(window_GRP, name="windows_GRP", parent="House1_GRP")


    def mkdoors(self):
        print("Making doors...")
        door_GRP = []        
        
        for door_num in range(self.number_of_doors):
            xform, shape = cmds.polyCube(height= self.door_height,
                                        width = self.door_width,
                                        depth = .5,
                                        name = "door1")
            
            self.transform_door(xform)

            door_GRP.append(xform)
            
            cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)   

        cmds.group(door_GRP, name="doors_GRP", parent="House1_GRP")
        
        return xform

    def mkhouseflatroof(self):
        print("Making the house's flat roof!")
        # This doesn't need to check if there's no roof because that'll be checked in the build function

        xform, shape = cmds.polyCube(height= self.roof_height/4,
                                    width = self.house_width*1.25,
                                    depth = self.house_width*1.25,
                                    name = "houseflatroof")

        cmds.xform(xform, translation = [0,self.wall_height,0])

        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
        return xform
    
    def transform_door(self, door):
        print("Transforming door...")

        z_pos = self.get_center_of_wall()
        y_pos = self.wall_height/self.get_height_of_house()
        pos = [0, y_pos, z_pos]

        cmds.xform(door, translation=pos)

    def transform_window(self, window):
        print("Transforming windows...")

        z_pos = self.get_center_of_wall()
        y_pos = self.get_window_height_from_base()

        pos = [0, y_pos, z_pos]
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
     