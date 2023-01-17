import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import QRect

scroll_style = """
    QScrollBar:vertical {
        background: rgb(10,10,10);
        width: 4px;
        margin: 0px 0 0px 0;
        border: 1px transparent #2A2929;
        border-radius: 4px;
        }

    QScrollBar::handle:vertical {
        border: 1px rgb(0, 0, 0);
        background: rgb(255, 85, 85);
        border-radius: 4px;
        }

"""


#    QPushButton#MyCustomButtonWidgetID{
button2Style = """
    QPushButton#MyCustomButtonWidgetID{
        background-color: rgb(109,113,168);
        border-radius: 10px;
        min-width: 30px;
        min-height: 30px;
        font-weight: 900;


    }
    QPushButton#MyCustomButtonWidgetID:hover {
        background-color: rgb(255,133,198);
        min-width: 30px;
        min-height: 30px;  
    }
    """


button3Style = """
    QPushButton#PlusButton{
        background-color: rgb(109,113,168);
        border-radius: 10px;
        min-width: 80px;
        min-height: 30px;
        font-weight: 900;


    }
    QPushButton#PlusButton:hover {
        background-color: rgb(255,133,198);
        min-width: 30px;
        min-height: 30px;  
    }
    """

setLineEditSheet = """
    QLineEdit{
        background-color: rgb(109,113,168);
        border-radius: 10px;
        min-width: 30px;
        min-height: 30px;
        font-weight: 900;
        color: white;
        padding-left: 10px;
        padding-bottom: 3px;
    }
    
"""

setLineSheet = """
    QFrame#line{
        border: none;
        border-bottom: 1px solid rgb(109,113,168);
        margin-left: 10px;
        margin-right: 5px;
    }

"""


class SelectionSetWidget(QtWidgets.QWidget):

    itClicked = QtCore.Signal()

    def __init__(self, object_path=None, selection=None, selection_name=""):
        super(SelectionSetWidget, self).__init__()

        self.object_path = object_path
        self.selection = set(selection)
        self.add_sel = {}
        self.selection_name = selection_name
        self.state_which_button = True

        self.setup_ui()

#--------------------context menu---------------------------------------

        self.popMenu = QtWidgets.QMenu(self)

        self.popMenu_add_obj_to_sel = QtWidgets.QAction('Add to selection', self)
        self.popMenu.addAction(self.popMenu_add_obj_to_sel)
        self.popMenu_add_obj_to_sel.triggered.connect(self.add_obj_to_sel)

        self.popMenu_remove_obj_from_sel = QtWidgets.QAction('Remove from selection', self)
        self.popMenu.addAction(self.popMenu_remove_obj_from_sel)
        self.popMenu_remove_obj_from_sel.triggered.connect(self.remove_obj_from_sel)

        self.popMenu_rename = QtWidgets.QAction('Rename', self)
        self.popMenu.addAction(self.popMenu_rename)
        self.popMenu_rename.triggered.connect(self.ctxRenameSet)

        self.popMenu_delete = QtWidgets.QAction('Delete', self)
        self.popMenu.addAction(self.popMenu_delete)
        self.popMenu_delete.triggered.connect(self.delete_selection_set)

        self.setMouseTracking(True)
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenu)

# -----------------------------------------------------------

    def setup_ui(self):
        self.setMinimumSize(260, 40)

        self.setAutoFillBackground(True)

        #layout
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        #button for a set
        self.set_button = QtWidgets.QPushButton(self.selection_name)
        self.set_button.setObjectName("MyCustomButtonWidgetID")
        self.set_button.setStyleSheet(button2Style)
        self.set_button.clicked.connect(self.set_button_clicked)
        self.main_layout.addWidget(self.set_button)

        #rename
        self.rename = QtWidgets.QLineEdit()
        self.rename.setVisible(0)
        self.rename.setObjectName("rename_qline")
        self.rename.setStyleSheet(setLineEditSheet)
        self.rename.returnPressed.connect(self.set_new_name)
        self.main_layout.addWidget(self.rename)

    def set_new_name(self):
        text = self.rename.text()
        self.set_button.setText(text)

        self.ctxRenameSet()
    #
    def ctxRenameSet(self):
        if self.set_button.isVisible():
            self.set_button.setVisible(0)
            self.rename.setVisible(1)

            self.rename.setText(self.set_button.text())
            self.rename.setFocus()
        else:
            self.set_button.setVisible(1)
            self.rename.setVisible(0)


    def delete_selection_set(self):
        self.deleteLater()

    def add_obj_to_sel(self):
        self.get_sel()

        for i in self.add_sel:
            self.selection.add(i)

    def remove_obj_from_sel(self):
        self.get_sel()

        for i in self.add_sel:
            if i in self.selection:
                self.selection.remove(i)


    def mouseReleaseEvent(self, event):
        if self.state_which_button == True:
            self.itClicked.emit()

        super(SelectionSetWidget, self).mouseReleaseEvent(event)


    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.state_which_button = True
        elif event.buttons() == QtCore.Qt.RightButton:
            self.state_which_button = False

        super(SelectionSetWidget, self).mousePressEvent(event)

    def onContextMenu(self, point):
        self.popMenu.exec_(self.mapToGlobal(point))

    def get_sel(self):
        self.add_sel = cmds.ls(sl=1, l=1)


    def set_button_clicked(self):
        cmds.select(self.selection)


class SelectionSetImplementation(QtWidgets.QDockWidget):
    def __init__(self):
        super(SelectionSetImplementation, self).__init__()

        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        self.selection = []
        self.set_name = ""

        self.setup_ui()


    def setup_ui(self):
        self.setWindowTitle("Selection Sets")
        self.setObjectName("SelectionSetImplementationUIId")
        self.setMinimumSize(300, 110)
        self.resize(300, 300)

        self.mainWidget = QtWidgets.QWidget()
        self.setWidget(self.mainWidget)

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(QtCore.Qt.AlignTop)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(3)
        self.mainWidget.setLayout(self.main_layout)

        #scroll area
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setMinimumWidth(300)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.scroll_bar = QtWidgets.QScrollBar()
        self.scroll_bar.setObjectName("customScroll")
        self.scroll_bar.setStyleSheet(scroll_style)
        self.scroll_area.setVerticalScrollBar(self.scroll_bar)

        self.scroll_area_widget = QtWidgets.QWidget()
        self.scroll_area.setWidget(self.scroll_area_widget)

        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setAlignment(QtCore.Qt.AlignTop)
        self.scroll_layout.setContentsMargins(0, 5, 5, 5)
        self.scroll_layout.setSpacing(0)
        self.scroll_area_widget.setLayout(self.scroll_layout)
        self.main_layout.addWidget(self.scroll_area)

        #addind label and + button for creating a new set
        self.add_layout = QtWidgets.QHBoxLayout()
        self.add_layout.setAlignment(QtCore.Qt.AlignTop)
        self.add_layout.setContentsMargins(10, 5, 5, 8)
        self.add_layout.setSpacing(10)
        self.scroll_layout.addLayout(self.add_layout)

        self.set_label = QtWidgets.QLineEdit()
        self.set_label.setObjectName("SetName")
        self.set_label.setPlaceholderText("Enter name for a Set")
        self.set_label.setMinimumWidth(100)
        self.set_label.setStyleSheet(setLineEditSheet)
        self.add_layout.addWidget(self.set_label)

        self.plus_button = QtWidgets.QPushButton("+")
        self.plus_button.setObjectName("PlusButton")
        self.plus_button.setStyleSheet(button3Style)
        self.plus_button.clicked.connect(self.on_button_plus_clicked)
        # self.plus_button.setFixedWidth(150)
        # self.plus_button.setMinimumWidth(50)
        self.add_layout.addWidget(self.plus_button)

        self.line = QtWidgets.QFrame()
        self.line.setObjectName("line")
        self.line.setGeometry(QRect(60, 110, 751, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        # self.line.setLineWidth(0)
        self.line.setStyleSheet(setLineSheet)
        self.scroll_layout.addWidget(self.line)


    def on_button_plus_clicked(self):
        self.get_selection()

        self.set_name = self.set_label.text()
        if self.set_name == "":
            self.set_name = "My selection"

        self.create_new_set()
        self.set_label.clear()

    def create_new_set(self):
        self.obj_widget = SelectionSetWidget(selection=self.selection, selection_name=self.set_name)
        self.scroll_layout.addWidget(self.obj_widget)

    def get_selection(self):
        self.selection = cmds.ls(sl=1, l=1)



def main():

    if cmds.window("SelectionSetImplementationUIId", exists=1):
        cmds.deleteUI("SelectionSetImplementationUIId")

    if cmds.windowPref("SelectionSetImplementationUIId", exists=1):
        cmds.windowPref("SelectionSetImplementationUIId", remove=1)

    global myUI
    myUI = SelectionSetImplementation()
    myUI.show()


if __name__ == "__main__":
    main()
