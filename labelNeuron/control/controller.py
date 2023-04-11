import os
import numpy as np
import skimage
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QFileDialog
import pyqtgraph.opengl as gl

from ..view.gui import GUI


class Controller:
    def __init__(self) -> None:
        """Initializes all controllers and managers."""
        self.view: "GUI"
        
        # Drawing states

        # Control states
        self.curr_cursor_pos: QPoint = None  # updated by mouse movement
        self.last_cursor_pos: QPoint = None  # updated by mouse click

        # temp
        self.img: np.ndarray = None

    def startup(self, view: "GUI") -> None:
        """Sets the view in all controllers and dependent modules; Loads labels from file."""
        self.view = view
    
    def loop_gui(self) -> None:
        """Function collection called during each event loop iteration."""
        self.set_cursor_pos()

    # CORRECTION METHODS
    def set_cursor_pos(self) -> None:
        """Sets the crosshair position in the glViewWidget to the current cursor position."""
        if self.curr_cursor_pos:
            self.view.glview_widget.crosshair_pos = (
                self.curr_cursor_pos.x(),
                self.curr_cursor_pos.y(),
            )

    # EVENT PROCESSING
    def mouse_clicked(self, a0: QtGui.QMouseEvent) -> None:
        """Triggers actions when the user clicks the mouse."""
        self.last_cursor_pos = a0.pos()
        self.view.glview_widget.get_world_coords(a0.x(), a0.y())
            

    def mouse_move_event(self, a0: QtGui.QMouseEvent) -> None:
        """Triggers actions when the user moves the mouse."""
        self.curr_cursor_pos = a0.pos()  # Updates the current mouse cursor position



    # 槽函数（暂时，不应该放这，细分模块）
    def open_file(self):
        if(not hasattr(self, 'recent_path')):
            self.recent_path = '.'
        file_name, _ = QFileDialog.getOpenFileName(self.view, "Open file", self.recent_path, "Image files (*.jpg *.gif *.png *.jpeg *.tif)")
        self.recent_path, _ = os.path.split(file_name)
        print(file_name)
        # 读取图片
        self.img = skimage.io.imread(file_name) # np.ndarray[uint16]
        # self.img = self.img.transpose(1,2,0)
        # 全读有点卡，先切一部分
        self.img = self.img.transpose(1,2,0)[:500, :500, :100]

        self.paint_image()

    def paint_image(self):
        '''
        对比度和透明度的调节还可以优化
        '''
        if(self.img is None):
            return
        
        # 增强对比度
        img = np.array(self.img)
        max_num = np.uint16(img.max() * self.view.spinbox_contrast.value())
        img = np.where(img > max_num, max_num, img)
        if(max_num):
            img = np.uint8(img / max_num * 255)
        else:
            img = np.ones(img.shape, dtype=np.uint8) * 255
        # 绘图
        data = np.empty(img.shape + (4,), dtype=np.ubyte)
        data[..., 2] = data[..., 1] = data[..., 0] = img
        data[..., 3] = img
        if(not hasattr(self, 'volume_item')):
            self.volume_item = gl.GLVolumeItem(data)
            self.volume_item.translate(-data.shape[0]/2, -data.shape[1]/2, 0)
            self.view.glview_widget.addItem(self.volume_item)
        else:
            self.volume_item.setData(data)
    