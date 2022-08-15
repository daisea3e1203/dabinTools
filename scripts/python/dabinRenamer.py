import hou

from PySide2 import QtCore
from PySide2 import QtWidgets

label_size = 150
editor_size = 200


class Renamer(QtWidgets.QWidget):
    def __init__(self):
        super(Renamer, self).__init__()
        # QtWidgets.QWidget.__init__(self, parent)
        
        # Window
        # ----------------------------------------------------------------------
        self.setParent(hou.qt.mainWindow(), QtCore.Qt.Window) # Without this the window closes automatically
        main_layout = QtWidgets.QVBoxLayout()
        # self.setGeometry(500, 300, 250, 110)
        self.setWindowTitle("Demo")
        
        # Add search box
        # ----------------------------------------------------------------------
        hlayout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel()
        label.setText("Search for:")
        label.setMinimumSize(QtCore.QSize(label_size,0))        
        hlayout.addWidget(label)

        self.search_text = QtWidgets.QLineEdit()
        self.search_text.setMinimumSize(QtCore.QSize(editor_size,0))
        hlayout.addWidget(self.search_text)

        main_layout.addLayout(hlayout)

        # Add replace with box
        # ----------------------------------------------------------------------
        hlayout = QtWidgets.QHBoxLayout()

        label = QtWidgets.QLabel()
        label.setText("Replace with:")
        label.setMinimumSize(QtCore.QSize(label_size,0))        
        hlayout.addWidget(label)

        self.replace_text = QtWidgets.QLineEdit()
        self.replace_text.setMinimumSize(QtCore.QSize(editor_size,0))
        hlayout.addWidget(self.replace_text)

        main_layout.addLayout(hlayout)

        # Add spacer
        # ----------------------------------------------------------------------
        spacer = QtWidgets.QSpacerItem(0, 40, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        main_layout.addItem(spacer)

        # Add rename button
        # ----------------------------------------------------------------------
        button = QtWidgets.QPushButton("Rename", self)
        button.clicked.connect(self.on_click_rename)
        main_layout.addWidget(button)
        
        # Finalize layout
        # ----------------------------------------------------------------------
        self.setLayout(main_layout)

            
    def on_click_rename(self):
        search_str = self.search_text.text()
        replace_str = self.replace_text.text()
        
        selected_nodes = hou.selectedNodes()

        with hou.undos.group("Rename nodes"):
            original_names = []

            for node in selected_nodes:
                original_name = node.name()
                original_names.append(original_name)
                node.setName(original_name + "_bak")

            for i, node in enumerate(selected_nodes):
                original_name = original_names[i]
                replaced_name = original_name.replace(search_str, replace_str)
                node.setName(replaced_name)

