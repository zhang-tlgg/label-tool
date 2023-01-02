import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QGraphicsScene
from PyQt5.QtGui import QImage, QPixmap
import skimage
import numpy as np

import ui.Ui_mainwindow as Ui_mainwindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_mainwindow.Ui_MainWindow()
        self.ui.setupUi(self)
        
        # 信号与槽绑定
        self.ui.actionOpen.triggered.connect(self.open_file)
    
    # 槽函数
    def open_file(self):
        if(not hasattr(self, 'recent_path')):
            self.recent_path = '.'
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", self.recent_path, "Image files (*.jpg *.gif *.png *.jpeg *.tif)")
        self.recent_path, _ = os.path.split(file_name)
        print(file_name)
        self.load_img(file_name)

    def set_value(self, value):
        if(self.sender() == self.ui.horizontalSlider or self.sender() == self.ui.spinBox):
            self.ui.horizontalSlider.setValue(value)
            self.ui.spinBox.setValue(value)
        elif(self.sender() == self.ui.horizontalSlider_2 or self.sender() == self.ui.spinBox_2):
            self.ui.horizontalSlider_2.setValue(value)
            self.ui.spinBox_2.setValue(value)
        self.show_img()

    # 成员函数
    def load_img(self, file_name):
        # 读入图片
        self.img = skimage.io.imread(file_name)
        self.show_img()
        # 设置部件
        self.ui.horizontalSlider.setMaximum(self.img.shape[0] - 1)
        self.ui.horizontalSlider.valueChanged.connect(self.set_value)
        self.ui.spinBox.setMaximum(self.img.shape[0] - 1)
        self.ui.spinBox.valueChanged.connect(self.set_value)
        self.ui.horizontalSlider_2.valueChanged.connect(self.set_value)
        self.ui.spinBox_2.valueChanged.connect(self.set_value)
        
    def show_img(self):
        img = np.array(self.img[self.ui.horizontalSlider.value()])
        h = img.shape[0]
        w = img.shape[1]
        if(img.dtype == 'uint16'):
            img = np.where(img > self.ui.horizontalSlider_2.value(), 65535, img)
            frame = QImage(img, w, h, QImage.Format_Grayscale16)
        else:
            img = np.where(img > self.ui.horizontalSlider_2.value(), 255, img)
            frame = QImage(img, w, h, w, QImage.Format_Grayscale8)
        pix = QPixmap.fromImage(frame).scaled(500, 500)
        scene = QGraphicsScene()
        scene.addPixmap(pix)
        self.ui.graphicsView.setScene(scene)
    

if __name__ =="__main__":
    app = QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
