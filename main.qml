import QtQuick 2.3
import QtQuick.Controls 2.3
import Renderer 1.0

Item {
    width: 1920
    height: 1080

    FBORenderer{
        id: fboRenderItem
        anchors.fill: parent
    }

    Text {
        id: text1
        anchors.bottom: fboRenderItem.bottom
        x: 20
        wrapMode: Text.WordWrap

        text: "This is an openGl rendering with QQuickFrameBufferObject"
    }

    Button {
        x: 100
        y: 100
        text: "Button"
    }

    Timer {
        id: timer1
        interval: 1000
        repeat: true
        running: true
        triggeredOnStart: true
        onTriggered: {
            text1.text = Date()
            fboRenderItem.update()
        }
    }
}