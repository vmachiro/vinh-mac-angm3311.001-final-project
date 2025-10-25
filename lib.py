import maya.cmds as cmds

# declare class of generated model
# house model is specifically for environment bgs, not for level exploration
class House():
    # define init and the basic parameters that'll be changed (5-10)
    def __init__(self):
        self.number_of_floors = 1        
        self.wall_height = 6 # this is impacted by number of floors
        self.roof_height = 4 # this should be something that can be 0 and still work, for stuff like skyscrapers or apartments with flat roofs. maybe make it toggle-able between triangle and cube???
        self.number_of_windows = 4
        self.number_of_doors = 1

    # define methods that would be useful for calculation
    
    def get_window_height_from_base():
        # TODO:
        # If more than one floor: Find lowest point of the house
        # Place window halfway through the height of the house
        pass
    
    # define the method that makes the object
    def mkhouse(self):
        print("Making your house!")
        # Polycube that bad boy
    
    # define method that builds the object
    def build(self):
        """Builds the house"""
        # TODO:
        # Create the house body
        # Create the roof
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