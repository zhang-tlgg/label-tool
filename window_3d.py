import sys, os
from PyQt5.QtWidgets import *
import numpy as np
import pyqtgraph.opengl as gl
import skimage

import ui.Ui_window3d as Ui_window3d

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_window3d.Ui_MainWindow()
        self.ui.setupUi(self)

        # 3d组件
        self.view_widget = gl.GLViewWidget(self.ui.centralwidget)
        self.view_widget.setCameraPosition(distance=500)
        self.ui.gridLayout.addWidget(self.view_widget, 0, 1, 1, 1)
        # 添加 item
        g = gl.GLGridItem()
        g.setSize(10, 10)
        g.scale(100, 100, 100)
        self.view_widget.addItem(g)
        
        # 信号与槽绑定
        self.ui.actionOpen.triggered.connect(self.open_file)
        self.ui.horizontalSlider.valueChanged.connect(self.set_value)
        self.ui.doubleSpinBox.valueChanged.connect(self.set_value)
        self.ui.horizontalSlider.sliderReleased.connect(self.show_img_3d)
        self.ui.doubleSpinBox.editingFinished.connect(self.show_img_3d)
        
    # 槽函数
    def set_value(self):
        if(self.sender() == self.ui.horizontalSlider):
            value = self.ui.horizontalSlider.value()
            self.ui.doubleSpinBox.setValue(value/1000)
        elif(self.sender() == self.ui.doubleSpinBox):
            value = self.ui.doubleSpinBox.value()
            self.ui.horizontalSlider.setValue(value*1000)

    def open_file(self):
        if(not hasattr(self, 'recent_path')):
            self.recent_path = '.'
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", self.recent_path, "Image files (*.jpg *.gif *.png *.jpeg *.tif)")
        self.recent_path, _ = os.path.split(file_name)
        print(file_name)
        # 读取图片
        self.img = skimage.io.imread(file_name)
        # self.img = self.img.transpose(1,2,0)
        # 全读有点卡，先切一部分
        self.img = self.img.transpose(1,2,0)[:500, :500, :100]
        self.show_img_3d()

    def show_img_3d(self):
        '''
        对比度和透明度的调节还可以优化
        '''
        # 增强对比度
        img = np.array(self.img)
        max_num = np.uint16(img.max() * self.ui.doubleSpinBox.value())
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
            self.view_widget.addItem(self.volume_item)
        else:
            self.volume_item.setData(data)

if __name__ == '__main__':
    # PyQt5 程序固定写法
    app = QApplication(sys.argv)

    # 将绑定了绘图控件的窗口实例化并展示
    window = Window()
    window.show()

    # PyQt5 程序固定写法
    sys.exit(app.exec())
