import pathlib
import pkg_resources
import signal
import sys
import traceback

from PyQt5 import uic, QtCore, QtWidgets

from . import info_view
from . import quick_view

from ..external import pyqtgraph as pg
from .._version import version as __version__



# global plotting configuration parameters
pg.setConfigOption("background", None)
pg.setConfigOption("antialias", False)
pg.setConfigOption("imageAxisOrder", "row-major")


class ShapeOut2(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        path_ui = pkg_resources.resource_filename("shapeout2.gui", "main.ui")
        uic.loadUi(path_ui, self)
        self.setWindowTitle("Shape-Out {}".format(__version__))
        # Disable native menubar (e.g. on Mac)
        self.menubar.setNativeMenuBar(False)
        # Initially hide buttons
        self.pushButton_preset_load.hide()
        self.pushButton_preset_save.hide()
        self.toolButton_show_dm.hide()
        # Subwindows
        self.subwindows = {}
        self.init_quick_view()
        self.init_info_view()
        self.mdiArea.cascadeSubWindows()
        self.showMaximized()

    def init_info_view(self):
        sub = QtWidgets.QMdiSubWindow()
        sub.hide()
        self.widget_info_view = info_view.InfoView()
        sub.setWidget(self.widget_info_view)
        self.mdiArea.addSubWindow(sub)
        self.toolButton_info_view.clicked.connect(sub.setVisible)
        self.subwindows["info_view"] = sub
        sub.setSystemMenu(None)
        sub.setWindowFlags(QtCore.Qt.CustomizeWindowHint
                           | QtCore.Qt.WindowTitleHint
                           | QtCore.Qt.Tool)

    def init_quick_view(self):
        sub = QtWidgets.QMdiSubWindow()
        sub.hide()
        self.widget_quick_view = quick_view.QuickView()
        sub.setWidget(self.widget_quick_view)
        self.mdiArea.addSubWindow(sub)
        self.toolButton_quick_view.clicked.connect(sub.setVisible)
        self.subwindows["quick_view"] = sub
        sub.setSystemMenu(None)
        sub.setWindowFlags(QtCore.Qt.CustomizeWindowHint
                           | QtCore.Qt.WindowTitleHint
                           | QtCore.Qt.Tool)


def excepthook(etype, value, trace):
    """
    Handler for all unhandled exceptions.
 
    :param `etype`: the exception type (`SyntaxError`, `ZeroDivisionError`, etc...);
    :type `etype`: `Exception`
    :param string `value`: the exception error message;
    :param string `trace`: the traceback header, if any (otherwise, it prints the
     standard Python header: ``Traceback (most recent call last)``.
    """
    vinfo = "Unhandled exception in Shape-Out version {}:\n".format(__version__)
    tmp = traceback.format_exception(etype, value, trace)
    exception = "".join([vinfo]+tmp)

    errorbox = QtWidgets.QMessageBox()
    errorbox.addButton(QtWidgets.QPushButton('Close'), QtWidgets.QMessageBox.YesRole)
    errorbox.addButton(QtWidgets.QPushButton('Copy text && Close'), QtWidgets.QMessageBox.NoRole)
    errorbox.setText(exception)
    ret = errorbox.exec_()
    if ret==1: 
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard )
        cb.setText(exception)


# Make Ctr+C close the app
signal.signal(signal.SIGINT, signal.SIG_DFL)
# Display exception hook in separate dialog instead of crashing
sys.excepthook = excepthook
