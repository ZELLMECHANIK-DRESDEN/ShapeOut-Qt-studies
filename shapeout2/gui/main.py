import pathlib
import pkg_resources
import signal
import sys
import traceback

from PyQt5 import uic, QtWidgets

from .._version import version as __version__

# load QMainWindow from ui file
ui_path = pkg_resources.resource_filename("shapeout2.gui", "main.ui")
MainBase = uic.loadUiType(ui_path)[0]


class ShapeOutQMdiSubWindow(QtWidgets.QMdiSubWindow):
    def closeEvent(self, QCloseEvent):
        """Correctly de-register a data set before removing the subwindow"""
        mainwidget = self.mdiArea().parentWidget().parentWidget()
        mainwidget.rem_subwindow(self.windowTitle())
        super(ShapeOutQMdiSubWindow, self).closeEvent(QCloseEvent)



class ShapeOut2(QtWidgets.QMainWindow, MainBase):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        MainBase.__init__(self)
        self.setupUi(self)
        self.setWindowTitle("Shape-Out {}".format(__version__))
        # Disable native menubar (e.g. on Mac)
        self.menubar.setNativeMenuBar(False)
        # Subwindows
        self.subwindows = []
        self.subwindow_data = []
        self.mdiArea.cascadeSubWindows()
        self.showMaximized()


    def add_subwindow(self, widget, obj):
        """Add a subwindow, register data set and add to menu"""
        sub = ShapeOutQMdiSubWindow()
        sub.setWidget(widget)
        self.mdiArea.addSubWindow(sub)
        sub.show()
        self.subwindows.append(sub)
        self.subwindow_data.append(obj)


    def rem_subwindow(self, title):
        """De-register a data set and remove from the menu"""
        for ii, sub in enumerate(self.subwindows):
            if sub.windowTitle() == title:
                self.subwindows.pop(ii)
                self.subwindow_data.pop(ii)
                break
        
        for action in self.menuExport.actions():
            if action.text() == title:
                self.menuExport.removeAction(action)
                break


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
