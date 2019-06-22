import pkg_resources

from PyQt5 import uic, QtWidgets, QtCore


class MatrixElement(QtWidgets.QWidget):
    _quick_view_instance = None

    def __init__(self, title="Name"):
        QtWidgets.QWidget.__init__(self)
        path_ui = pkg_resources.resource_filename(
            "shapeout2.gui", "matrix_element.ui")
        uic.loadUi(path_ui, self)

        self.selected = False
        self.enabled = True

        self.update_content()

    def mousePressEvent(self, event):
        # toggle selection
        if event.modifiers() == QtCore.Qt.ShiftModifier:
            quickview = True
        else:
            self.selected = not self.selected
            quickview = False
        self.update_content(quickview)
        event.accept()

    def update_content(self, quickview=False):
        if self.selected and self.enabled:
            color = "#86E789"  # green
            label = "active"
            tooltip = "Click to deactivate\nShift+Click for QuickView"
        elif self.selected and not self.enabled:
            color = "#A4D5A7"  # gray-green
            label = "active\n(disabled)"
            tooltip = "Click to deactivate\nShift+Click for QuickView"
        elif not self.selected and self.enabled:
            color = "#EFEFEF"  # light gray
            label = "inactive"
            tooltip = "Click to activate\nShift+Click for QuickView"
        else:
            color = "#C0C1C0"  # gray
            label = "inactive"
            tooltip = "Click to activate\nShift+Click for QuickView"

        curinst = MatrixElement._quick_view_instance
        if curinst is self:
            do_quickview = True
        elif quickview:
            # reset color of old quick view instance
            if curinst is not None and self is not curinst:
                MatrixElement._quick_view_instance = None
                curinst.update_content()
            MatrixElement._quick_view_instance = self
            do_quickview = True
        else:
            do_quickview = False
        if do_quickview:
            color = "#F0A1D6"
            label += "\n(QV)"

        self.setStyleSheet("background-color:{}".format(color))
        self.label.setText(label)
        self.setToolTip(tooltip)
        self.label.setToolTip(tooltip)
