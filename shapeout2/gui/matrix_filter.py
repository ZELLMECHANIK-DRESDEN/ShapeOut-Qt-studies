import pkg_resources

from PyQt5 import uic, QtWidgets, QtCore


class MatrixFilter(QtWidgets.QWidget):
    def __init__(self, title="Name"):
        QtWidgets.QWidget.__init__(self)
        path_ui = pkg_resources.resource_filename(
            "shapeout2.gui", "matrix_filter.ui")
        uic.loadUi(path_ui, self)

        self.setFixedSize(QtCore.QSize(80, 80))
        self.resize(QtCore.QSize(80, 80))
        self.setMaximumSize(QtCore.QSize(80, 80))

        self.label.setToolTip(title)
        if len(title) > 8:
            title = title[:5]+"..."
        self.label.setText(title)
