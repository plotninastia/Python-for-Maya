from PySide2 import QtWidgets, QtGui, QtCore
import maya.cmds as cmds
import maya.mel as mel
from maya.app.general.mayaMixin import MayaQWidgetBaseMixin
import json

from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class MyMIME(QtCore.QMimeData):
    def __init__(self):
        super(MyMIME, self).__init__()
        self.someText = "none"
        self.command = ""
        self.iconpath = ""

    def setText(self, text=""):
        self.someText = text

    def getText(self):
        return self.someText

    def setCommand(self, command):
        self.command = command

    def getCommand(self):
        return self.command

    def setIconpath(self, iconpath):
        self.iconpath = iconpath

    def getIconpath(self):
        return self.iconpath



class ButtonWidget(QtWidgets.QWidget):
    def __init__(self, label="TEST", command="", iconpath=""):
        super(ButtonWidget, self).__init__()

        # self.setObjectName("ButtonWidget")
        self.setFixedSize(200, 52)

        #bg color
        self.setAutoFillBackground(True)
        color = 80
        self.p = QtWidgets.QApplication.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
        self.setPalette(self.p)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.setLayout(self.mainLayout)

        # self.addCommand()
        # self.addIconpath()

        self.command = command
        self.iconpath = iconpath

        self.label = QtWidgets.QLabel(label)
        self.mainLayout.addWidget(self.label)


    def addLabel(self, t=""):
        self.label.setText(t)

    def addCommand(self, command=""):
        self.command = command

    def addIconpath(self, iconpath=""):
        self.iconpath = iconpath

        if iconpath != "":
            self.icon_label = QtWidgets.QLabel(self)
            self.pixmap = QtGui.QPixmap(self.iconpath).scaled(35, 35, QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.icon_label.setPixmap(self.pixmap)
            # self.mainLayout.addWidget(self.icon_label)
            # self.icon_label.setFixedSize(40, 40)
            # self.pixmap.scaled(20, 20)
            self.mainLayout.insertWidget(0, self.icon_label)

    def getLabel(self):
        return self.label.text()

    def getCommand(self):
        return self.command

    def getIconpath(self):
        return self.iconpath


    def mousePressEvent(self, event):
        if event.buttons() != QtCore.Qt.LeftButton:
            return

        mimeData = MyMIME()
        mimeData.setText(self.label.text())
        mimeData.setCommand(self.command)
        mimeData.setIconpath(self.iconpath)
        # mimeData.setPixmapIcon(self.iconpath)

        self.pixmap = self.grab()
        painter = QtGui.QPainter(self.pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(self.pixmap.rect(), QtGui.QColor(80, 80, 80, 127))
        painter.end()

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(QtCore.Qt.LinkAction | QtCore.Qt.MoveAction)



class FieldWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super(FieldWidget, self).__init__()

        self.buttonsList = []

        self.widgets_info = {}

        self.setFixedSize(240, 300)
        self.setAcceptDrops(True)

        #bg color
        self.setAutoFillBackground(True)
        color = 40
        self.p = QtWidgets.QApplication.palette()
        self.p.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
        self.setPalette(self.p)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)

        #scroll area
        self.scrollArea = QtWidgets.QScrollArea()
        self.scrollArea.setMinimumWidth(200)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scrollArea.setWidget(self.scroll_area_widget)
        self.scroll_layout = QtWidgets.QGridLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0,0,2,0)
        self.scroll_layout.setSpacing(5)
        self.scroll_area_widget.setLayout(self.scroll_layout)
        self.mainLayout.addWidget(self.scrollArea)


    def return_containing_widgets(self):

        self.all_widgets = {}

        for i in range(self.scroll_layout.count()):
            wdg = self.scroll_layout.itemAt(i).widget()
            label = self.scroll_layout.itemAt(i).widget().getLabel()
            # self.all_widgets[i] = self.scroll_layout.itemAt(i).widget().getLabel()
            all_values = {}
            all_values['command'] = wdg.getCommand()
            all_values['iconpath'] = wdg.getIconpath()
            self.all_widgets[label] = all_values

        return self.all_widgets

        # for key in self.all_widgets:
        #     print(key, self.all_widgets[key])


            # for i in self.all_widgets:
        #     print(self.all_widgets(i))

        # for i in range(self.scroll_layout.count()):
        #     item = self.scroll_layout.itemAt(i).widget()
        #     if isinstance(item, ButtonWidget):
        #         # self.widgets_info = {}
        #         print('ok')
        #         print(item)



    def feedButtons(self):
        # for i in range(10):
        #     button = ButtonWidget()
        #     button.addLabel(t = "Button {}".format(i))
        #     self.buttonsList.append(button)
        #     self.scroll_layout.addWidget(button)


        ngskin_btn = ButtonWidget()
        ngskin_btn.addLabel("NgSkin")
        ngskin_btn.addCommand("import ngSkinTools2; ngSkinTools2.open_ui()")
        ngskin_btn.addIconpath("C:/Users/admin/Documents/maya/2020/prefs/icons/ngskin.png")
        self.buttonsList.append(ngskin_btn)
        self.scroll_layout.addWidget(ngskin_btn)

        qrenametool_btn = ButtonWidget()
        qrenametool_btn.addLabel("RenameTool")
        qrenametool_btn.addCommand("Quick_rename_tool ()")
        qrenametool_btn.addIconpath("C:/Users/admin\Dropbox (Личный)/PROJECTS_ONGOING/Python_For_Maya_Anim/week8/draw.png")
        self.buttonsList.append(qrenametool_btn)
        self.scroll_layout.addWidget(qrenametool_btn)

        skinMagic_btn = ButtonWidget()
        skinMagic_btn.addLabel("skinMagic")
        skinMagic_btn.addIconpath("C:/Users/admin/Documents/maya/2020/scripts/SkinMagic/icons/Title.png")
        skinMagic_btn.addCommand("execfile(r'C:\\Users\\admin\Documents\\maya\\2020\\scripts\\SkinMagic\\skinMagic.py')")
        self.buttonsList.append(skinMagic_btn)
        self.scroll_layout.addWidget(skinMagic_btn)

        GraphEditor_btn = ButtonWidget()
        GraphEditor_btn.addLabel("GraphEditor")
        GraphEditor_btn.addIconpath("C:/Users/admin\Dropbox (Личный)/PROJECTS_ONGOING/Python_For_Maya_Anim/week8/curve.png")
        GraphEditor_btn.addCommand("mel.eval('GraphEditor')")
        self.buttonsList.append(GraphEditor_btn)
        self.scroll_layout.addWidget(GraphEditor_btn)

        freezetransformations_btn = ButtonWidget()
        freezetransformations_btn.addLabel("Freeze")
        freezetransformations_btn.addIconpath("C:/Users/admin\Dropbox (Личный)/PROJECTS_ONGOING/Python_For_Maya_Anim/week8/snowflake.png")
        freezetransformations_btn.addCommand("mel.eval('FreezeTransformationsOptions')")
        self.buttonsList.append(freezetransformations_btn)
        self.scroll_layout.addWidget(freezetransformations_btn)


    def dragEnterEvent(self, e):
        e.acceptProposedAction()

    def dropEvent(self, e):
        mimeData = e.mimeData()
        mimeText = mimeData.getText()
        mimeIconPath = mimeData.getIconpath()
        mimeCommand = mimeData.getCommand()
        e.source().deleteLater()

        button = ButtonWidget()
        button.addLabel(t = mimeText)
        button.addIconpath(mimeIconPath)
        button.addCommand(mimeCommand)
        self.scroll_layout.addWidget(button)

    def dragMoveEvent(self, e):
        e.acceptProposedAction()



class MyDDWnd(MayaQWidgetBaseMixin, QtWidgets.QDialog):

    path_to_file_signal = QtCore.Signal(str)

    def __init__(self):
        super(MyDDWnd, self).__init__()

        self.setObjectName("dragNdropWindow")
        self.setWindowTitle("Scripts customizator")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(500, 350)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(1)
        self.main_layout.setContentsMargins(0, 5, 0, 0)
        self.setLayout(self.main_layout)

        self.dnd_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.dnd_layout)

        self.w1 = FieldWidget()
        self.w1.feedButtons()

        self.w2 = FieldWidget()

        self.dnd_layout.addWidget(self.w1)
        self.dnd_layout.addWidget(self.w2)


        self.v_layout = QtWidgets.QHBoxLayout()
        # self.v_layout.setSpacing(1)
        # self.v_layout.setContentsMargins(0, 5, 0, 0)
        self.main_layout.addLayout(self.v_layout)

        self.savebtn = QtWidgets.QPushButton("Save")
        self.v_layout.setAlignment(QtCore.Qt.AlignBottom)
        self.savebtn.setMinimumHeight(40)
        self.savebtn.clicked.connect(self.save_widgets)
        # self.savebtn.setContentsMargins(10, 0, 10, 0)
        self.v_layout.addWidget(self.savebtn)


    def save_widgets(self):
        self.all_widgets_json_data = self.w2.return_containing_widgets()

        # for key in self.all_widgets_json_data:
        #     print(key, self.all_widgets_json_data[key])

        self.path_to_file = cmds.fileDialog2(fileFilter="*.json", dialogStyle=2, caption="Save")[0]
        # global path_to_file
        # path_to_file = cmds.fileDialog2(fileFilter="*.json", dialogStyle=2, caption="Save")[0]

        with open(self.path_to_file, 'w') as outfile:
            json.dump(self.all_widgets_json_data, outfile, indent=4)

        if self.path_to_file:
            self.path_to_file_signal.emit(self.path_to_file)

        self.close()


class ChooseWindow(MayaQWidgetDockableMixin, QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(ChooseWindow, self).__init__(parent=parent)

# class ChooseWindow(MayaQWidgetBaseMixin, QtWidgets.QDialog):
#     def __init__(self):
#         super(ChooseWindow, self).__init__()

        self.setObjectName("chooseWindow")
        self.setWindowTitle("Fav scripts")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.setMinimumSize(100, 50)
        # self.resize(300, 500)
        self.resize(250, 70)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setSpacing(1)
        self.main_layout.setContentsMargins(5, 0, 5, 5)
        self.setLayout(self.main_layout)

        #layout for a choose button

        self.choose_layout = QtWidgets.QVBoxLayout()
        self.choose_layout.setSpacing(1)
        self.choose_layout.setContentsMargins(5, 0, 5, 10)
        self.choose_layout.setAlignment(QtCore.Qt.AlignBottom)
        self.main_layout.addLayout(self.choose_layout)

        self.choose_scripts = QtWidgets.QPushButton("Choose fav scripts")
        # self.somebtn.setIcon(QtGui.QIcon('C:/Users/admin/Dropbox (Личный)/PROJECTS_ONGOING/Python_For_Maya_Anim/week8/icon.png'))
        self.choose_scripts.clicked.connect(self.runDragNDropWnd)
        self.choose_scripts.setMinimumHeight(40)
        self.choose_layout.addWidget(self.choose_scripts)

        # self.btbtbtb = QtWidgets.QPushButton('lalalala')
        # # self.btbtbtb.clicked.connect("mel.eval('FreezeTransformationsOptions')")
        # self.btbtbtb.clicked.connect(cmds.select('pCylinder1'))
        # self.choose_layout.addWidget(self.btbtbtb)

        #layout for scripts buttons

        self.buttons_layout = QtWidgets.QVBoxLayout()
        self.buttons_layout.setSpacing(3)
        self.buttons_layout.setContentsMargins(5, 5, 5, 5)
        # self.main_layout.addLayout(self.buttons_layout)
        self.main_layout.insertLayout(0, self.buttons_layout)

        self.line_layout = QtWidgets.QVBoxLayout()
        # self.line_layout.setSpacing(1)
        self.line_layout.setContentsMargins(5, 5, 5, 0)
        self.main_layout.insertLayout(1, self.line_layout)


    def load_json_buttons(self, path_to_file):

        with open(path_to_file, 'r') as read_file:
            json_data = json.load(read_file)

        #delete previous widgets
        for i in reversed(range(self.buttons_layout.count())):
            self.buttons_layout.itemAt(i).widget().setParent(None)

        #create buttons and insert into a layout

        # for script_name, script_data in json_data.items():
        #     btn = QtWidgets.QPushButton(script_name)
        #     for command, iconpath in script_data.items():
        #         btn.clicked.connect(script_data[command])
        #         btn.setIcon(QtGui.QIcon(iconpath))
        #         btn.setIconSize(QtCore.QSize(30, 30))
        #         self.buttons_layout.addWidget(btn)
        #         print()

        for script_name, script_data in json_data.items():
            btn = QtWidgets.QPushButton(script_name)
            for key_commands, value in script_data.items():
                # print(key_commands)
                # print('----------')

                if key_commands == 'iconpath':
                    btn.setIcon(QtGui.QIcon(value))
                    btn.setIconSize(QtCore.QSize(35, 35))


                # btn.clicked.connect(value_taken[0])
                # btn.setIcon(QtGui.QIcon(value_taken[1]))
                # btn.setIconSize(QtCore.QSize(30, 30))
                self.buttons_layout.addWidget(btn)

        self.connect_btn_to_functions()
        self.resize_after_adding_buttons()
        self.add_separator()

    # def command_btn(self, command):
    #     # mel.eval('FreezeTransformationsOptions')
    #     # execfile(r'C:\Users\admin\Documents\maya\2020\scripts\SkinMagic\skinMagic.py')
    #     exec(command)

    def connect_btn_to_functions(self):

        for i in reversed(range(self.buttons_layout.count())):
            btn = self.buttons_layout.itemAt(i).widget()
            if btn.text() == 'NgSkin':
                btn.clicked.connect(self.ng_func)
            elif btn.text() == 'RenameTool':
                btn.clicked.connect(self.rename_func)
            elif btn.text() == 'skinMagic':
                btn.clicked.connect(self.skinMagic_func)
            elif btn.text() == 'GraphEditor':
                btn.clicked.connect(self.graphEditor_func)
            elif btn.text() == 'Freeze':
                btn.clicked.connect(self.freeze_func)

    def ng_func(self):
        exec('import ngSkinTools2; ngSkinTools2.open_ui()')
        # cmds.select('pCylinder1')

    def rename_func(self):
        mel.eval('Quick_rename_tool ()')

    def skinMagic_func(self):
        execfile(r'C:\\Users\\admin\Documents\\maya\\2020\\scripts\\SkinMagic\\skinMagic.py')

    def graphEditor_func(self):
        mel.eval('GraphEditor')

    def freeze_func(self):
        mel.eval('FreezeTransformationsOptions')


    def resize_after_adding_buttons(self):
        height = 90 + self.buttons_layout.count() * 48
        # self.setMinimumSize(150, height)
        # self.resize(250, height)
        # self.setFixedSize(200, height)
        self.setMinimumSize(130, height)
        self.setFixedHeight(height)
        self.resize(250, height)
        self.buttons_layout.setContentsMargins(5, 13, 5, 5)

    def add_separator(self):
        line = QtWidgets.QFrame()
        line.setGeometry(QtCore.QRect(60, 110, 751, 20))
        line.setFrameShape(QtWidgets.QFrame.HLine)
        # line.setContentsMargins(5, 5, 5, 10)
        # self.line_layout.setContentsMargins(5, 5, 5, 10)
        # line.setFrameShadow(QtWidgets.QFrame.Sunken)
        # self.choose_scripts.setContentsMargins(0, 10, 0, 0)

        # self.main_layout.addWidget(line)
        # self.main_layout.insertWidget(1, line)
        # self.choose_layout.insertWidget(0, line)

        #delete previous widgets
        for i in reversed(range(self.line_layout.count())):
            self.line_layout.itemAt(i).widget().setParent(None)

        self.line_layout.addWidget(line)
        self.line_layout.setContentsMargins(5, 5, 5, 10)



    def update_btn(self):
        self.somebtn.setText("Options")


    def runDragNDropWnd(self):

        if cmds.window("dragNdropWindow", exists=1):
            cmds.deleteUI("dragNdropWindow")

        if cmds.windowPref("dragNdropWindow", exists=1):
            cmds.windowPref("dragNdropWindow", remove=1)

        myDragDropWnd = MyDDWnd()
        myDragDropWnd.setWindowIcon(QtGui.QIcon('C:/Users/admin/Dropbox (Личный)/PROJECTS_ONGOING/Python_For_Maya_Anim/week8/icon.png'))
        myDragDropWnd.path_to_file_signal.connect(self.load_json_buttons)
        myDragDropWnd.show()


def main():

    if cmds.window("chooseWindow", exists = 1):
        cmds.deleteUI("chooseWindow")

    if cmds.windowPref("chooseWindow", exists = 1):
        cmds.windowPref("chooseWindow", remove = 1)

    chooseWindow = ChooseWindow()
    chooseWindow.show()




    # chooseWindow.show(dockable=True)



#---------------------------------------------------------------
    # myWidget = MyQWidget()
    # # myWidget.show(dockable=True, floating=False, area='right')
    # myWidget.show(dockable=True)

#---------------------------------------------------------------


if __name__ == "__main__":
    main()