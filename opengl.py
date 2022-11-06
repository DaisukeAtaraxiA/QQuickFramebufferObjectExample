from OpenGL.GL import *
from PySide2.QtCore import QUrl, qDebug, QObject, QElapsedTimer
from PySide2 import QtCore, QtGui
from PySide2.QtGui import QGuiApplication, QOpenGLFramebufferObjectFormat, QOpenGLFramebufferObject
from PySide2.QtQml import qmlRegisterType
from PySide2.QtQuick import QQuickItem, QQuickView, QQuickFramebufferObject


class FbItemRenderer(QQuickFramebufferObject.Renderer):
    def __init__(self, parent=None):
        super(FbItemRenderer, self).__init__()
        qDebug("Creating FbItemRenderer")
        self._window = None
        self._program = None
        self._profile = QtGui.QOpenGLVersionProfile()
        self._profile.setVersion(3, 3)
        self.gl = None
        self._y = 0.5
        self._timer = QElapsedTimer()
        self._timer.start()

    def createFrameBufferObject(self, size):
        qDebug("Creating FrameBufferObject")
        format = QOpenGLFramebufferObjectFormat()
        format.setSamples(4)
        return QOpenGLFramebufferObject(size, format)

    def synchronize(self, item):
        qDebug("Synchronizing")
        nsec = self._timer.nsecsElapsed()
        self._timer.restart()
        if nsec > 0:
            fps = 1.0E+9 / nsec
            qDebug("FPS " + str(round(fps, 3)))

        super().synchronize(item)
        self._y += 0.01

    def render(self):
        qDebug("Render")
        # Called with the FBO bound and the viewport set.
        # ... Issue OpenGL commands.
        if self._program is None:
            self._my_initialize()

        # self.gl.glClearColor(0.8, 0.8, 0.8, 1)
        # self.gl.glClear(GL_COLOR_BUFFER_BIT)
        glClearColor(0.8, 0.8, 0.8, 1)
        glClear(GL_COLOR_BUFFER_BIT)

        values = [
            0.5, -0.5,
            -0.5, -0.5,
            0.0, self._y,
        ]

        self._program.bind()
        self._program.setUniformValue("myColor", QtGui.QVector3D(0, 1, 0))
        self._program.enableAttributeArray(0)
        self._program.setAttributeArray(0, values, 2)

        # self.gl.glDrawArrays(GL_TRIANGLES, 0, 3)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 3)

        self._program.disableAttributeArray(0)
        self._program.release()

        # Not sure this is necessary
        # self._window.resetOpenGLState()

    def _my_initialize(self):
        qDebug("_my_initialize")
        if self._window is None:
            return

        self.gl = self._window.openglContext().versionFunctions(self._profile)
        self.gl = QtGui.QOpenGLFunctions(QtGui.QOpenGLContext.currentContext())
        self._program = QtGui.QOpenGLShaderProgram()
        self._program.addCacheableShaderFromSourceCode(
            QtGui.QOpenGLShader.Vertex,
            """
            # version 330 core
            layout (location = 0) in vec2 vertices;
            void main() {
                gl_Position = vec4(vertices, 0.0, 1.0);
            }
            """)
        self._program.addCacheableShaderFromSourceCode(
            QtGui.QOpenGLShader.Fragment,
            """
            #version 330 core
            uniform vec3 myColor;
            void main() {
                gl_FragColor = vec4(myColor,1.0);
            }
            """)
        self._program.bindAttributeLocation( "vertices", 0 )
        self._program.link()

    def set_window(self, window):
        qDebug("set_window")
        self._window = window


class FBORenderItem(QQuickFramebufferObject):
    def __init__(self, parent=None):
        qDebug("Create fborenderitem")
        super(FBORenderItem, self).__init__(parent)
        self._renderer = None

    def createRenderer(self):
        qDebug("Create renderer")
        self._renderer = FbItemRenderer()
        self._renderer.set_window(self.window())
        return self._renderer


if __name__ == '__main__':
    import sys

    app = QGuiApplication(sys.argv)

    qmlRegisterType(FBORenderItem, "Renderer", 1, 0, "FBORenderer")

    view = QQuickView()
    view.setSource(QUrl("main.qml"))
    view.show()

    sys.exit(app.exec_())