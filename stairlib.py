import maya.cmds as cmds

class Stair():
    
    def __init__(self):
        self.total_rise = 1
        self.total_run = 12
        self.width = 2
        self.step_count = 10
        
    def get_step_rise(self):
        step_rise = self.total_rise/self.step_count
        return step_rise

    def get_step_run(self):
        step_run = self.total_run/self.step_count
        return step_run

    def mkstep(self):
        print("Making step...")

        xform, shape = cmds.polyCube(height= self.get_step_rise(),
                                    width = self.width,
                                    depth = self.total_run/self.step_count,
                                    name = "step1")

        cmds.xform(xform, translation = [0,self.get_step_rise()/2,0])

        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
        return xform

    def transform_step(self, step_name, step_num):
        print("Transforming step...")
        y_pos = self.get_step_rise() * step_num
        z_pos = self.get_step_run() * step_num
    
        pos = [0, y_pos, z_pos]    
        cmds.xform(step_name, translation=pos)
        
    def build(self):
        """Builds the stair"""
        # TODO:
        steps = []
        for step_num in range(self.step_count):
            # create a step
            step_name = self.mkstep()
            steps.append(step_name)
            # postition step
            self.transform_step(step_name,step_num)
            # repeat until we have a staircase
        cmds.group(steps, name="stair")
        pass
        
if __name__ == "__main__":
    # this instances an object
    stair1 = Stair()
    stair1.rise = 2.5
    stair1.run = 5.0
    print(stair1.rise)
    print(stair1.run)

    stair2 = Stair()