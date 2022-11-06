from OpenGL.GL import *
from PySide2.QtCore import QUrl, qDebug, QObject
from PySide2.QtGui import QGuiApplication, QOpenGLFramebufferObjectFormat, QOpenGLFramebufferObject
from PySide2.QtQml import qmlRegisterType
from PySide2.QtQuick import QQuickItem, QQuickView, QQuickFramebufferObject


class FbItemRenderer(QQuickFramebufferObject.Renderer):
    def __init__(self, parent=None):
        super(FbItemRenderer, self).__init__()
        qDebug("Creating FbItemRenderer")

    def createFrameBufferObject(self, size):
        qDebug("Creating FrameBufferObject")
        format = QOpenGLFramebufferObjectFormat()
        format.setAttachment(QOpenGLFramebufferObject.Depth)
        return QOpenGLFramebufferObject(size, format)

    def synchronize(self, item):
        qDebug("Synchronizing")

    def render(self):
        qDebug("Render")
        # Called with the FBO bound and the viewport set.
        # ... Issue OpenGL commands.


class FBORenderItem(QQuickFramebufferObject):
    def __init__(self, parent=None):
        qDebug("Create fborenderitem")
        super(FBORenderItem, self).__init__(parent)
        self._renderer = None

    def createRenderer(self):
        qDebug("Create renderer")
        self._renderer = FbItemRenderer()
        return self._renderer


if __name__ == '__main__':
    import sys

    app = QGuiApplication(sys.argv)

    qmlRegisterType(FBORenderItem, "Renderer", 1, 0, "FBORenderer")

    view = QQuickView()
    view.setSource(QUrl("main.qml"))
    view.show()

    sys.exit(app.exec_())