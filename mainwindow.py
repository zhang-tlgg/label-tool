import os
import sys

import numpy as np
import skimage
import ui.Ui_mainwindow as Ui_mainwindow
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.img = None
        self.recent_path = None
        self.ui = Ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)

        # 信号与槽绑定
        self.ui.actionOpen.triggered.connect(self.open_file)

    # 槽函数
    def open_file(self):
        if not hasattr(self, 'recent_path'):
            self.recent_path = '.'
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", self.recent_path, "Image files (*.jpg *.gif "
                                                                                        "*.png *.jpeg *.tif)")
        self.recent_path, _ = os.path.split(file_name)
        print(file_name)
        if file_name is not None:
            self.load_img(file_name)

    def set_value(self, value):
        if self.sender() == self.ui.horizontalSlider or self.sender() == self.ui.spinBox:
            self.ui.horizontalSlider.setValue(value)
            self.ui.spinBox.setValue(value)
        elif self.sender() == self.ui.horizontalSlider_2:
            self.ui.doubleSpinBox.setValue(value / 1000)
        elif self.sender() == self.ui.doubleSpinBox:
            self.ui.horizontalSlider_2.setValue(value * 1000)
        self.show_img()

    # 成员函数
    def load_img(self, file_name):
        # 读入图片
        try:
            self.img = skimage.io.imread(file_name)
            self.show_img()
            # 设置部件
            self.ui.horizontalSlider.setMaximum(self.img.shape[0] - 1)
            self.ui.horizontalSlider.valueChanged.connect(self.set_value)
            self.ui.spinBox.setMaximum(self.img.shape[0] - 1)
            self.ui.spinBox.valueChanged.connect(self.set_value)
            self.ui.horizontalSlider_2.valueChanged.connect(self.set_value)
            self.ui.doubleSpinBox.valueChanged.connect(self.set_value)
        except:
            pass

    def show_img(self):
        img = np.array(self.img[self.ui.horizontalSlider.value()])
        h = img.shape[0]
        w = img.shape[1]
        if img.dtype == 'uint16':
            max_num = np.uint16(img.max() * self.ui.doubleSpinBox.value())
            img = np.where(img > max_num, max_num, img)
            if max_num:
                img = np.uint16(img / max_num * 65535)
            else:
                img = np.ones(img.shape, dtype=np.uint16) * 65535
            frame = QImage(img, w, h, 2 * w, QImage.Format_Grayscale16)
        else:
            max_num = np.uint8(img.max() * self.ui.doubleSpinBox.value())
            img = np.where(img > max_num, max_num, img)
            if max_num:
                img = np.uint8(img / max_num * 255)
            else:
                img = np.ones(img.shape, dtype=np.uint8) * 255
            frame = QImage(img, w, h, w, QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(frame).scaled(500, 500)
        scene = QGraphicsScene()
        scene.addPixmap(pix)
        self.ui.graphicsView.setScene(scene)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
