import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


class PolyCreateWindow(QtWidgets.QDialog):

    def __init__(self):
        super(PolyCreateWindow, self).__init__()

        self.setObjectName("PolyCreateWindow")
        self.setWindowTitle("Poly Create")
        self.setMinimumSize(300, 200)
        self.setMaximumSize(300, 200)
        self.resize(300, 200)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        #layouts
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.objectNameUI()
        self.radioButtonsUI()
        self.sliderUI()
        self.actionButtonsUI()
        self.dropdownUI()

    def objectNameUI(self):

        #object name layout
        self.objNameLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.objNameLayout)

        self.objNameLine = QtWidgets.QLineEdit()
        self.objNameLine.setObjectName("ObjectName")
        self.objNameLine.setPlaceholderText("Object Name")
        self.objNameLayout.addWidget(self.objNameLine)

    def radioButtonsUI(self):

        #radio buttons
        self.radioButLayout = QtWidgets.QHBoxLayout()
        self.radioButLayout.setSpacing(2)
        self.radioButLayout.setContentsMargins(0,0,0,0)

        self.grp_radio_buttons = QtWidgets.QGroupBox()
        self.radio_groupLayout = QtWidgets.QHBoxLayout()
        self.grp_radio_buttons.setMaximumHeight(40)

        self.grp_radio_buttons.setLayout(self.radio_groupLayout)
        self.mainLayout.addWidget(self.grp_radio_buttons)

        self.rb1 = QtWidgets.QRadioButton('Sphere')
        self.rb1.setChecked(True)
        self.rb2 = QtWidgets.QRadioButton('Cone')
        self.rb3 = QtWidgets.QRadioButton('Cube')

        self.radio_groupLayout.addWidget(self.rb1)
        self.radio_groupLayout.addWidget(self.rb2)
        self.radio_groupLayout.addWidget(self.rb3)

    def sliderUI(self):

        #slider
        self.sliderLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.sliderLayout)

        self.slider = QtWidgets.QSlider()
        self.sliderLayout.addWidget(self.slider)
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMaximum(10)
        self.slider.setMinimum(1)

        self.slider_line = QtWidgets.QLineEdit()
        #self.slider_line = QtWidgets.QLabel()
        self.sliderLayout.addWidget(self.slider_line)
        self.slider_line.setMaximumSize(30, 25)
        self.slider_line.setReadOnly(1)

        self.slider.valueChanged.connect(self.slider_changed_value)


    def slider_changed_value(self):
        value = self.slider.value()
        self.slider_line.setText(str(value))

    def create_button(self):
        self.apply_button()
        self.close()

    def apply_button(self):

        name = self.objNameLine.text()

        if name == "":
            name = "MySphere"

        radius = self.slider.value()

        if self.rb1.isChecked():
            cmds.polySphere(n=name, r=radius)
        elif self.rb2.isChecked():
            cmds.polyCone(n=name, r=radius, h=radius)
        elif self.rb3.isChecked():
            cmds.polyCube(n=name, w=radius, h=radius, d=radius)


    def actionButtonsUI(self):

        #buttons
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.buttons_layout)

        self.but1 = QtWidgets.QPushButton("Create")
        self.but2 = QtWidgets.QPushButton("Apply")
        self.but3 = QtWidgets.QPushButton("Close")

        self.buttons_layout.addWidget(self.but1)
        self.buttons_layout.addWidget(self.but2)
        self.buttons_layout.addWidget(self.but3)

        #create commands for buttons. and how to apply them
        self.but1.clicked.connect(self.create_button)
        self.but2.clicked.connect(self.apply_button)
        self.but3.clicked.connect(self.close)

    def dropdownUI(self):
        self.dropdownLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addLayout(self.dropdownLayout)

        self.dropdown = QtWidgets.QComboBox()
        self.dropdownLayout.addWidget(self.dropdown)
        self.dropdown.setFixedHeight(25)

        self.dropdown.addItem("Sphere")
        self.dropdown.addItem("Cone")
        self.dropdown.addItem("Cube")

        self.dropdown_line = QtWidgets.QLabel()
        self.dropdownLayout.addWidget(self.dropdown_line)
        self.dropdown_line.setText("Select from the dropdown")
        self.dropdown.currentIndexChanged.connect(self.dropdown_change)


    def dropdown_change(self):

        i = "index = {}, text = {}".format(self.dropdown.currentIndex(), self.dropdown.currentText())
        self.dropdown_line.setText(i)


if cmds.window("PolyCreateWindow", q=1, exists=1):
    cmds.deleteUI("PolyCreateWindow")

if cmds.windowPref("PolyCreateWindow", exists=1):
    cmds.windowPref("PolyCreateWindow", remove=1)

myUI = PolyCreateWindow()
myUI.show()