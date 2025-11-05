from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


import maya.OpenMayaUI as omui
from shiboken2 import wrapInstance


import maya.cmds as cmds


def get_maya_main_win():
    main_win = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_win), QtWidgets.QWidget)

class HouseGenWin(QtWidgets.QDialog):
    """House Window Class"""

    def __init__(self):
        # runs the init code of the parent QDialog class
        super().__init__(parent=get_maya_main_win())
        self.houseGen = House()
        self.setWindowTitle("House Generator")
        self.resize(800, 200)
        self._mk_main_layout()
        self._connect_signals()

    def _connect_signals(self):
        self.enable_grp_name_cb.stateChanged.connect(self.toggle_grpname)
        self.cancel_btn.clicked.connect(self.cancel)
        self.build_btn.clicked.connect(self.build)

    @QtCore.Slot()
    def toggle_grpname(self):
        is_custom_grpname_enabled = self.enable_grp_name_cb.isChecked()
        self.grp_name_ledit.setDisabled(not is_custom_grpname_enabled)

    @QtCore.Slot()
    def cancel(self):
        self.close()

    @QtCore.Slot()
    def build(self):
        self._update_housegen_properties()
        self.houseGen.build()

    def _update_housegen_properties(self):
        self.houseGen.__init__() # reset properties to default
        self.houseGen.roof_height = self.roof_height_dspnbox.value()        
        self.houseGen.wall_height = self.wall_height_spnbx.value()
        self.houseGen.number_of_floors = self.number_of_floors_spnbox.value()
        self.houseGen.number_of_windows = self.number_of_windows_spnbox.value()
        self.houseGen.number_of_doors = self.door_spnbox.value()
        self.houseGen.housename = self.grp_name_ledit.text()

    def _mk_main_layout(self):
        self.main_layout = QtWidgets.QVBoxLayout()
        self._add_name_label()
        self._add_form_layout()
        self._mk_btn_layout()
        self.setLayout(self.main_layout)

    def _add_form_layout(self):
        self.form_layout = QtWidgets.QFormLayout()
        self._add_roof_height()
        self._add_wall_height()
        self._add_floors()        
        self._add_windows()
        self._add_doors()
        self._add_custom_grpname()
        self.main_layout.addLayout(self.form_layout)

    def _add_custom_grpname(self):
        self.enable_grp_name_cb = QtWidgets.QCheckBox("Enable Custom House Name")
        self.grp_name_ledit = QtWidgets.QLineEdit("House")
        self.grp_name_ledit.setDisabled(True)
        self.form_layout.addRow(self.enable_grp_name_cb)
        self.form_layout.addRow("Group", self.grp_name_ledit)

    def _add_windows(self):
        self.number_of_windows_spnbox = QtWidgets.QSpinBox()
        self.number_of_windows_spnbox.setValue(2)
        self.form_layout.addRow("Window Number", self.number_of_windows_spnbox)

    def _add_floors(self):
        self.number_of_floors_spnbox = QtWidgets.QSpinBox()
        self.number_of_floors_spnbox.setValue(1)
        self.form_layout.addRow("Number of Floors", self.number_of_floors_spnbox)

    def _add_roof_height(self):
        self.roof_height_dspnbox = QtWidgets.QDoubleSpinBox()
        self.roof_height_dspnbox.setValue(1)
        self.form_layout.addRow("Roof Height", self.roof_height_dspnbox)

    def _add_doors(self):
        self.door_spnbox = QtWidgets.QSpinBox()
        self.door_spnbox.setValue(1)
        self.door_spnbox.setMaximum(2)
        self.form_layout.addRow("Door Number", self.door_spnbox)

    def _add_wall_height(self):
        self.wall_height_spnbx = QtWidgets.QSpinBox()
        self.wall_height_spnbx.setValue(5)
        self.form_layout.addRow("Wall Height", self.wall_height_spnbx)

    def _add_name_label(self):
        self.name_lbl = QtWidgets.QLabel("House Generator")
        self.name_lbl.setStyleSheet("background-color: purple;"
                                    "color: white;"
                                    "font: bold 24px;")
        self.name_lbl.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.name_lbl)

    def _mk_btn_layout(self):
        self.btn_layout = QtWidgets.QHBoxLayout()
        self.build_btn = QtWidgets.QPushButton("Build")
        self.cancel_btn = QtWidgets.QPushButton("Cancel")
        self.btn_layout.addWidget(self.build_btn)
        self.btn_layout.addWidget(self.cancel_btn)
        self.main_layout.addLayout(self.btn_layout)

class House():

    def __init__(self):
        self.number_of_floors = 2        
        self.wall_height = 8 
        self.house_width = 8
        self.roof_height = 1 
        self.number_of_windows = 4
        self.window_height = 2
        self.number_of_doors = 1
        self.housename = ""
    
    def get_height_of_house(self):
        return self.wall_height * self.number_of_floors

    def get_base_of_house(self):
        base_height = self.wall_height/self.get_height_of_house() * self.number_of_floors
        return base_height

    def get_window_height_from_base(self):
        window_placement = self.wall_height/self.get_height_of_house() + (self.wall_height/2)
        return window_placement

    def get_center_of_wall(self):
        # This depends on the depth of the house body being equal to the width
        return self.house_width/2
    
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
        for floor_num in range(self.number_of_floors):
            window_GRP = []

            for windows_num in range(self.number_of_windows):
                xform, shape = cmds.polyCube(height= self.window_height,
                                            width = 1,
                                            depth = 1,
                                            name = "window1")

                self.transform_window(xform)
                world_pos = cmds.xform(xform, query=True, worldSpace=True, translation=True)

                if windows_num%2 == 1:
                    self.transform_window_to_back(world_pos[2])

                if windows_num > 1:
                    self.transform_window_up(world_pos[1])            
                                        
                window_GRP.append(xform)
            
            cmds.group(window_GRP, name="windows_GRP")
            window_GRP.clear()

    def mkdoors(self):
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

        #cmds.group(door_GRP, name="doors_GRP")
        
        return xform

    def mkhouseflatroof(self):
        xform, shape = cmds.polyCube(height= self.roof_height,
                                    width = self.house_width*1.25,
                                    depth = self.house_width*1.25,
                                    name = "houseflatroof1")

        cmds.xform(xform, translation = [0,self.get_height_of_house(),0])

        cmds.makeIdentity(xform, apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)
        return xform
    
    def transform_door(self, door):
        z_pos = self.get_center_of_wall()
        y_pos = self.get_base_of_house()*.7
        pos = [0, y_pos, z_pos]

        cmds.xform(door, translation=pos)

    def transform_door_to_back(self, door):
        
        z_pos = self.get_center_of_wall()
        y_pos = self.get_base_of_house()
        pos = [0, y_pos, z_pos*-1]

        cmds.xform(door, translation=pos)

    def transform_window(self, window):
        z_pos = self.get_center_of_wall()
        y_pos = self.get_window_height_from_base()
        #x_pos = self.house_width/4

        pos = [0, y_pos, z_pos]

        cmds.xform(window, translation=pos)

    def transform_window_up(self, window_y_pos):
        y_pos = window_y_pos * self.number_of_floors

        cmds.move( y_pos, y=True )

    def transform_window_to_back(self, window_z_pos):
        z_pos = window_z_pos*-1

        cmds.move( z_pos, z=True )

    def build(self):

        house_things = []

        housebody = self.mkhousebody()
        house_things.append(housebody)

        if self.roof_height != 0:
            houseroof = self.mkhouseflatroof()
            house_things.append(houseroof)

        cmds.group(house_things, name=self.housename) 
        
        # Windows and doors are made after the HouseGRP because we declare parent when their groups are made

        doors_grp = self.mkdoors()
        house_things.append(doors_grp) 
        cmds.group(doors_grp, name="doors_GRP", parent=self.housename)
        
        windows_grp = self.mkwindows()
        house_things.append(windows_grp)

        """cmds.makeIdentity("House1", apply=True, translate=True, rotate=True, 
                          scale=True, normal=False, preserveNormals=True)   """

     
    
if __name__ == "__main__":
    pass
     