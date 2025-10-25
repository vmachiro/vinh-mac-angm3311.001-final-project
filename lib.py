import maya.cmds as cmds

# declare class of generated model
# house model is specifically for environment bgs, not for level exploration
class House():
    # define init and the basic parameters that'll be changed (5-10)
    def __init__(self):
        self.number_of_floors = 1        
        self.wall_height = 8 # this is impacted by number of floors
        self.roof_height = 4 # this should be something that can be 0 and still work, for stuff like skyscrapers or apartments with flat roofs. maybe make it toggle-able between triangle and cube???
        self.number_of_windows = 4
        self.window_height = 2
        self.window_width = 2
        self.number_of_doors = 1 # will there be double doors or will it just be a single door placed front and back??
        self.door_height = 2
        self.door_width = 1

    # define methods that would be useful for calculation
    
    def get_window_height_from_base():
        # TODO:
        # If more than one floor: Find lowest point of the house
        # Place window halfway through the height of the house
        pass
    
    # define the method that makes the house body
    def mkhousebody(self):
        print("Making your house!")
        # TODO:
        # Use polycube to make the main body based on wall_height and number_of_floors

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
        # Create the house body
        # Check if there is a roof.
        # IF so, Create the roof
        # Place the windows (Do windows have to be made in a separate method? Aw man)
        # Place the front door 
        # If more than one door, place second door
    
    
# define main

if __name__ == "__main__":
    house1 = House()
    house1.wall_height = 4
    house1.roof_height = 8
    print(house1.wall_height)
    print(house1.roof_height)