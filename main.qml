import QtQuick 2.3
import Renderer 1.0

Item {
    width: 500
    height: 600

    FBORenderer{
        id: fboRenderItem
        anchors.fill: parent
    }

    Text {
        anchors.bottom: fboRenderItem.bottom
        x: 20
        wrapMode: Text.WordWrap

        text: "This is an openGl rendering with QQuickFrameBufferObject"
    }
}