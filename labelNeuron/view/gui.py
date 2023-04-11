import os
import sys
import logging
from pathlib import Path
from typing import TYPE_CHECKING

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QAction,
    QActionGroup,
    QColorDialog,
    QFileDialog,
    QInputDialog,
    QLabel,
    QMessageBox,
)
import pyqtgraph
import pyqtgraph.opengl as gl

from ..ui.Ui_mainwindow import Ui_MainWindow

if TYPE_CHECKING:
    from ..control.controller import Controller


class GUI(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, control: "Controller") -> None:
        super(GUI, self).__init__()
        # pyqtgraph.setConfigOption('useOpenGL', True)
        self.setupUi(self)
        self.resize(1024, 600)
        self.setWindowTitle("labelNeuron")
        self.glview_widget.setCameraPosition(distance=500)
        g = gl.GLGridItem()
        g.setSize(10, 10)
        g.scale(100, 100, 100)
        self.glview_widget.addItem(g)
        
        self.controller = control

        # Connect all events to functions
        self.connect_events()
        
        # Connect with controller
        self.controller.startup(self)
        
        # Start event cycle
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(20)  # period, in milliseconds
        self.timer.timeout.connect(self.controller.loop_gui)
        self.timer.start()
        
    # Event connectors
    def connect_events(self) -> None:
        # CONTRAST CONTROL
        self.slider_contrast.valueChanged.connect(
            lambda: self.spinbox_contrast.setValue(self.slider_contrast.value() / 1000)
        )

        self.slider_contrast.sliderReleased.connect(
            self.controller.paint_image
        )

        self.spinbox_contrast.valueChanged.connect(
            lambda: self.slider_contrast.setValue(self.spinbox_contrast.value() * 1000)
        )

        self.spinbox_contrast.editingFinished.connect(
            self.controller.paint_image
        )

        # MENU BAR
        self.action_open_file.triggered.connect(self.controller.open_file)
    
    # Collect, filter and forward events to viewer
    def eventFilter(self, event_object, event) -> bool:
        # Mouse Events
        if (event.type() == QEvent.MouseMove) and (event_object == self.glview_widget):
            self.controller.mouse_move_event(event)
        elif (event.type() == QEvent.MouseButtonPress) and (event_object == self.glview_widget):
            if (event.buttons() == QtCore.Qt.RightButton):
                self.controller.mouse_clicked(event)
            # elif (event.buttons() == QtCore.Qt.LeftButton):
            #     print('right mouse button press')

        return False
    