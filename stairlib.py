from PySide2 import QtWidgets, QtCore
import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance


import maya.cmds as cmds

def get_maya_main_win():
        # Boilerplate code, just keep it somewhere. It's useful. 
        # Don't worry about what specifically it does LOL
        main_win = omui.MQtUtil.mainWindow()
        return wrapInstance(int(main_win), QtWidgets.QWidget)
    
class StairGenWin(QtWidgets.QDialog):
    """Stair Window Class"""
    
    def __init__(self):
        # runs the init code of the parent QDialog class
        super().__init__(parent=get_maya_main_win())
        self.stairGen = Stair()
        self.setWindowTitle("Stair Generator")
        self.resize(500,200)
        self._mk_main_layout()
        self._connect_signals()
    
    def _connect_signals(self):
        self.cancel_btn.clicked.connect(self.cancel)
        self.build_btn.clicked.connect(self.build)
    
    @QtCore.Slot()
    def cancel(self):
        self.close()
        
    @QtCore.Slot()
    def build(self):
        self.stairGen.build()
    
    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._mk_btn_layout()
        self.setLayout(self.main_layout)

    def _mk_btn_layout(self):
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.btn_layout.addWidget(self.build_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.btn_layout)
    

class Stair():
    
    def __init__(self):
        self.total_rise = 1
        self.total_run = 12
        self.width = 2
        self.step_count = 10
        
    def get_step_rise(self):
        return self.total_rise/self.step_count

    def get_step_run(self):
        return self.total_run/self.step_count

    def mkstep(self):

        xform, shape = cmds.polyCube(height= self.get_step_rise(),
                                    width = self.width,
                                    depth = self.total_run/self.step_count,
                                    name = "step1")

        cmds.xform(xform, translation = [0,self.get_step_rise()/2,0])
        # Freeze transforms so we don't have to care about the half step we did every time this makes another step.
        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
        return xform

    def transform_step(self, step_name, step_num):
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