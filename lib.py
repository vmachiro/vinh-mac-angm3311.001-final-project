import maya.cmds as cmds

# house model is specifically for environment bg population, not for interior map level exploration, so there will not be multiple walls or a floor
class House():
    def __init__(self):
        self.number_of_floors = 1        
        self.wall_height = 8 
        self.house_width = 8
        self.roof_height = 4 # this should be something that can be 0 and still work, for stuff like skyscrapers or apartments with flat roofs. 
        self.number_of_windows = 4
        self.window_height = 2
        self.window_width = 2
        self.number_of_doors = 1 
        self.door_height = 2
        self.door_width = 1
    
    def get_window_height_from_base(self):
        # TODO:
        # If more than one floor: Find lowest point of the house
        # Place window halfway through the height of the house
        window_placement = self.wall_height/2
        return window_placement

    def get_center_of_wall(self):
        center_of_wall = self.house_width/2
        # how the heck do i align this to the exterior edge of the house. transforms? do we just transform???
        return center_of_wall
    
    def mkhousebody(self):
        print("Making your house!")
        xform, shape = cmds.polyCube(height= self.wall_height * self.number_of_floors,
                                    width = self.house_width,
                                    depth = self.wall_height/self.house_width,
                                    name = "housebody")
        
        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
        
        return xform

    def mkwindows(self):
        print("Making windows...")
        # TODO:
        # Make cube based on window_height and window_width
        xform, shape = cmds.polyCube(height= self.window_height,
                                    width = self.window_width,
                                    depth = .5,
                                    name = "window1")
        
        # keep doing this until we hit amount of windows desired
        
        # in the mind of scope, there's probably not gonna be a window sill/frame thing for now

    def mkdoors(self):
        print("Making doors...")
        
        xform, shape = cmds.polyCube(height= self.door_height,
                                    width = self.door_width,
                                    depth = 1,
                                    name = "door1")
        
        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
            
        # Move the front door to the wall
        self.transform_door(xform, door_num=self.number_of_doors)

        # If more than one door, place second door

        return xform

    def transform_door(self, door, door_num):
        print("Transforming door...")

        x_pos = self.get_center_of_wall()
        # figure out how to . find the wall...

        pos = [x_pos, 0, 0]

        # do this until all doors have been moved
        cmds.xform(door, translation=pos)

    def transform_window(self, window, window_num):
        # TODO:
        # Take the distance from base for window height placement
        # Find the exterior wall. ANY OF THEM. Maybe by scaling the placement until it matches the width of the house???
        print("Transforming windows...")

        y_pos = self.get_window_height_from_base()
        # figure out how to . find the wall...

        pos = [0, y_pos, 0]

        # TURN THE WINDOW. ROTATE THE WINDOW! I FORGOT
        # window rotation will be based on which wall. 30-60-90

        cmds.xform(window, translation=pos)
        
        # Keep doing this for all of the windows...
    
    # define the method that makes the house roof
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
    
    def build(self):
        """Builds the house"""
        # TODO:
        house_things = []

        housebody = self.mkhousebody()
        house_things.append(housebody)

        if self.roof_height != 0:
            # IF ROOF: Check what kind of roof. (DO THIS LATER)
            # Create the roof (set to flatroof for now bc easier)
            houseroof = self.mkhouseflatroof()
            house_things.append(houseroof)
        # Create the front door
        housedoor1 = self.mkdoors()
        house_things.append(housedoor1) # Figure out multiple doors later
        
        # Create the windows
        windows_grp = self.mkwindows()
        house_things.append(windows_grp)

        # Doors and windows are transformed in their methods because the xform would have to be called and defined like a bazillion times

        cmds.group(house_things, name="House1") 
        
        pass     
    
if __name__ == "__main__":
    house1 = House()
    house1.wall_height = 4
    house1.roof_height = 8
    print(house1.wall_height)
    print(house1.roof_height)