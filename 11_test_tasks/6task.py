"""
Task 6 [UI]

Create a window which has two custom widgets.
These two widgets must be instances of the same class.

They should stand out against the background of the dialog box (change bg color of them).

When user clicks on one widget, the other widget should change color to a random one.

"""

from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
import random

class ObjectWidget(QtWidgets.QWidget):

    isClicked = QtCore.Signal(int, int, int)

    def __init__(self, label=''):
        super(ObjectWidget, self).__init__()

        self.label_name = label

        self.setup_ui()

    def setup_ui(self):

        self.setMinimumSize(50, 40)
        self.setMaximumHeight(40)

        self.setAutoFillBackground(True)
        self.set_background(60, 60, 60)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.main_layout)

        self.label = QtWidgets.QLabel(self.label_name)
        self.main_layout.addWidget(self.label)

    def set_background(self, r=60, g=60, b=60):
        self.p = QtGui.QPalette()
        self.color = QtGui.QColor(r,g,b)
        self.p.setColor(self.backgroundRole(), self.color)
        self.setPalette(self.p)

    def mouseReleaseEvent(self, event):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.isClicked.emit(r, g, b)


class MyCustomWidget(QtWidgets.QWidget):
    def __init__(self):
        super(MyCustomWidget, self).__init__()

        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Task 6")
        self.setObjectName("Task6UIId")
        self.setMinimumSize(400, 60)
        self.resize(400, 60)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setContentsMargins(5, 10, 5, 5)
        self.main_layout.setSpacing(3)
        self.setLayout(self.main_layout)

        self.first_widget = ObjectWidget('Click me')
        self.second_widget = ObjectWidget('Click me')
        self.main_layout.addWidget(self.first_widget)
        self.main_layout.addWidget(self.second_widget)

        self.first_widget.isClicked.connect(self.second_widget.set_background)
        self.second_widget.isClicked.connect(self.first_widget.set_background)


def main():

    if cmds.window("Task6UIId", exists=1):
        cmds.deleteUI("Task6UIId")

    if cmds.windowPref("Task6UIId", exists=1):
        cmds.windowPref("Task6UIId", remove=1)

    global myUI
    myUI = MyCustomWidget()
    myUI.show()


if __name__ == '__main__':
    main()