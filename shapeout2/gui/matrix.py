from PyQt5 import QtCore, QtWidgets

from .matrix_dataset import MatrixDataset
from .matrix_filter import MatrixFilter
from .matrix_element import MatrixElement


class DataMatrix(QtWidgets.QWidget):
    def __init__(self, parent=None, analysis=range(3)):
        super(DataMatrix, self).__init__(parent)

        self.layout = QtWidgets.QGridLayout()
        self.layout.setSpacing(2)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.setAcceptDrops(True)

        self.add_filter()
        self.repaint()
        self.add_dataset(path="data 1")
        self.add_dataset(path="dataset 2 with a long title")

    def add_dataset(self, path, row=None):
        nrows = self.layout.rowCount()
        if row is None:
            self.layout.addWidget(MatrixDataset(path), nrows, 0)
        else:
            assert False
        self.fill_elements()
        self.adjust_size()

    def add_filter(self, evt=None):
        ncols = self.layout.columnCount()
        name = "FS{}".format(ncols)
        self.layout.addWidget(MatrixFilter(name), 0, ncols)
        self.fill_elements()
        self.adjust_size()

    def fill_elements(self):
        ncols = self.layout.columnCount()
        nrows = self.layout.rowCount()
        for ii in range(1, nrows):
            for jj in range(1, ncols):
                if self.layout.itemAtPosition(ii, jj) is None:
                    self.layout.addWidget(MatrixElement(), ii, jj)

    def adjust_size(self):
        ncols = self.layout.columnCount()
        nrows = self.layout.rowCount()
        if ncols > 1 and nrows > 1:
            hwidth = self.layout.itemAtPosition(0, 1).geometry().width() + 2
            hheight = self.layout.itemAtPosition(0, 1).geometry().height() + 2
            dwidth = self.layout.itemAtPosition(1, 0).geometry().width() + 2
            dheight = self.layout.itemAtPosition(1, 0).geometry().height() + 2

            self.setMinimumSize((ncols-1)*hwidth+dwidth,
                                (nrows-1)*dheight+hheight)

    def clear(self):
        # TODO
        raise NotImplementedError("Clear not implemented")

    def dragEnterEvent(self, event):
        print("drag enter event on data matrix")
        event.ignore()

    def dropEvent(self, event):
        print("drag drop event on data matrix")
        event.ignore()

    def update_content(self):
        ncols = self.layout.columnCount()
        nrows = self.layout.rowCount()
        for ii in range(1, nrows):
            for jj in range(1, ncols):
                item = self.layout.itemAtPosition(ii, jj)
                if isinstance(item, MatrixElement):
                    item.update_content()
