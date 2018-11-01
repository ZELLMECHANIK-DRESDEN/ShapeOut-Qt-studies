from PyQt5.QtCore import (pyqtSignal, QByteArray, QDataStream, QIODevice,
        QMimeData, QPoint, QRect, QSize, Qt)
from PyQt5.QtGui import QDrag, QColor, QCursor, QIcon, QPainter, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QFrame, QHBoxLayout,
        QListView, QListWidget, QListWidgetItem, QMainWindow, QMessageBox,
        QSizePolicy, QWidget)


from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

class DataMatrix(QWidget):
    def __init__(self, parent=None, analysis=range(3)):
        super(DataMatrix, self).__init__(parent)

        self.column1Pixmaps = []
        self.iconPixmaps = []
        self.iconRects = []
        self.iconLocations = []

        for ii in analysis:
            im = Image.new('RGB', (80, 80))
            draw = ImageDraw.Draw(im)
            draw.text((0, 0),"Dataset {}".format(ii),(255,255,255))
            im.save("test.png")
            pixmap = QPixmap("test.png")
            self.column1Pixmaps.append(pixmap)
            square =  QRect(0, ii * 80, 80, 80)
            location = QPoint(0, ii * 80)
            self.iconLocations.append(location)
            self.iconPixmaps.append(pixmap)
            self.iconRects.append(square)
            self.update(square)

        self.highlightedRect = QRect()
        self.inPlace = 0

        self.setAcceptDrops(True)
        self.setMinimumSize(400, 400)
        self.setMaximumSize(400, 400)

    def clear(self):
        # TODO
        raise NotImplementedError("Clear not implemented")

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat('image/x-matrix-entry'):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        updateRect = self.highlightedRect
        self.highlightedRect = QRect()
        self.update(updateRect)
        event.accept()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.united(self.targetSquare(event.pos()))

        if event.mimeData().hasFormat('image/x-matrix-entry') and self.findPiece(self.targetSquare(event.pos())) == -1:
            self.highlightedRect = self.targetSquare(event.pos())
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QRect()
            event.ignore()

        self.update(updateRect)

    def dropEvent(self, event):
        if event.mimeData().hasFormat('image/x-matrix-entry') and self.findPiece(self.targetSquare(event.pos())) == -1:
            pieceData = event.mimeData().data('image/x-matrix-entry')
            dataStream = QDataStream(pieceData, QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = QPixmap()
            location = QPoint()
            dataStream >> pixmap >> location

            self.iconLocations.append(location)
            self.iconPixmaps.append(pixmap)
            self.iconRects.append(square)

            self.hightlightedRect = QRect()
            self.update(square)

            event.setDropAction(Qt.MoveAction)
            event.accept()

        else:
            self.highlightedRect = QRect()
            event.ignore()

    def findPiece(self, pieceRect):
        try:
            return self.iconRects.index(pieceRect)
        except ValueError:
            return -1

    def mousePressEvent(self, event):
        square = self.targetSquare(event.pos())
        found = self.findPiece(square)

        if found == -1:
            return

        location = self.iconLocations[found]
        pixmap = self.iconPixmaps[found]
        
        # TODO:
        # - only delete if not in first column
        del self.iconLocations[found]
        del self.iconPixmaps[found]
        del self.iconRects[found]

        if location == QPoint(square.x() / 80, square.y() / 80):
            self.inPlace -= 1

        self.update(square)

        itemData = QByteArray()
        dataStream = QDataStream(itemData, QIODevice.WriteOnly)

        dataStream << pixmap << location

        mimeData = QMimeData()
        mimeData.setData('image/x-matrix-entry', itemData)

        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - square.topLeft())
        drag.setPixmap(pixmap)

        if drag.exec_(Qt.MoveAction) != Qt.MoveAction:
            self.iconLocations.insert(found, location)
            self.iconPixmaps.insert(found, pixmap)
            self.iconRects.insert(found, square)
            self.update(self.targetSquare(event.pos()))

            if location == QPoint(square.x() / 80, square.y() / 80):
                self.inPlace += 1

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), Qt.white)

        if self.highlightedRect.isValid():
            painter.setBrush(QColor("#ffcccc"))
            painter.setPen(Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for rect, pixmap in zip(self.iconRects, self.iconPixmaps):
            painter.drawPixmap(rect, pixmap)

        painter.end()

    def targetSquare(self, position):
        return QRect(position.x() // 80 * 80, position.y() // 80 * 80, 80, 80)

