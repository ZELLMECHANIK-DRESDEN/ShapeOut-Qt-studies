import pkg_resources

from PyQt5 import uic, QtWidgets, QtCore


class MatrixElement(QtWidgets.QWidget):
    def __init__(self, title="Name"):
        QtWidgets.QWidget.__init__(self)
        path_ui = pkg_resources.resource_filename("shapeout2.gui", "matrix_element.ui")
        uic.loadUi(path_ui, self)
        self.pushButton.clicked.connect(self.mousePressEvent)

        self.selected = False
        self.enabled = True

        self.update_content()

    def mousePressEvent(self, event):
        # toggle selection
        self.selected = not self.selected
        self.update_content()

    def update_content(self):
        if self.selected and self.enabled:
            color = "#86E789"  # green
            label = "active"
        elif self.selected and not self.enabled:
            color = "#A4D5A7"  # gray-green
            label = "active\n(disabled)"
        elif not self.selected and self.enabled:
            color = "#EFEFEF"  # light gray
            label = "inactive"
        else:
            color = "#C0C1C0" # gray
            label = "inactive"
        self.setStyleSheet("background-color:{}".format(color))
        self.label.setText(label)