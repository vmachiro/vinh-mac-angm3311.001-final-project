import maya.cmds as cmds

# house model is specifically for environment bgs, not for level exploration
class House():
    def __init__(self):
        self.number_of_floors = 1        
        self.wall_height = 8 # this is impacted by number of floors
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
        pass

    def get_center_of_wall(self):
        # Find 0.5 of the width
        # used in door and window placement
        pass
    
    # define the method that makes the house body
    def mkhousebody(self):
        print("Making your house!")
        # TODO:
        # Use polycube to make the main body based on wall_height and number_of_floors
        xform, shape = cmds.polyCube(height= self.wall_height,
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
        # in the mind of scope, there's probably not gonna be a window sill/frame thing for now

    def mkdoors(self):
        print("Making doors...")
        # TODO:
        # Make cube based on door_height and door_width
        # Number_of_doors won't be used here, it'll be used for populating the house in the build method. 
        # Specifying the different object kinds of doors will suck big bad and may cause problems later

    # define the method that makes the house roof
    def mkhouseflatroof(self):
        print("Making the house's flat roof!")
        # This is a separate method so that the user can choose not to have a roof in the menu
        # This should have options whether to be triangular or flat roof
        # This doesn't need to check if there's no roof because that'll be checked in the build function
        # TODO:
        # Create a cube based on roof_height
        # No roof_width because we're depending on house body width
        # Tranform the cube according to width of the house to have an overhang.
    
    def mkhousetriangleroof(self):
        print("Making the house's pointy roof!")
        
        # This is a separate method so that the user can choose not to have a roof in the menu
        # This should have options whether to be triangular or flat roof
        # TODO:
        # This doesn't need to check if there's no roof because that'll be checked in the build function
        # This is the same thing as flat roof, but diff poly
    
    # define method that builds the object
    def build(self):
        """Builds the house"""
        # TODO:
        house_things=[]
        # Create the house body
        housebody = self.mkhousebody()
        house_things.append(housebody)
        # Check if there is a roof.
        if self.roof_height != 0:
            # IF ROOF: Check what kind of roof. (DO THIS LATER)
            # Create the roof (set to flatroof for now bc easier)
            houseroof = self.mkhouseflatroof()
            house_things.append(houseroof)
        # Create the front door
        housedoor1 = self.mkdoors()
        house_things.append(housedoor1) # Figure out multiple doors later
        # Place the front door 
        cmds.xform(xform, translation = [self.get_center_of_wall,0,0])
        # If more than one door, place second door
        # Place the windows 0.4 of the door     
        cmds.group(house_things, name="House1") 
        pass 
    
    
if __name__ == "__main__":
    house1 = House()
    house1.wall_height = 4
    house1.roof_height = 8
    print(house1.wall_height)
    print(house1.roof_height)