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
        self.view_widget.setCameraPosition(distance=20)
        self.ui.gridLayout.addWidget(self.view_widget, 0, 0, 1, 1)
        # 添加 item
        g = gl.GLGridItem()
        self.view_widget.addItem(g)
        self.scatter_plot = gl.GLScatterPlotItem()
        self.view_widget.addItem(self.scatter_plot)
        
        # 信号与槽绑定
        self.ui.actionOpen.triggered.connect(self.open_file)
    
    # 槽函数
    def open_file(self):
        if(not hasattr(self, 'recent_path')):
            self.recent_path = '.'
        file_name, _ = QFileDialog.getOpenFileName(self, "Open file", self.recent_path, "Image files (*.jpg *.gif *.png *.jpeg *.tif)")
        self.recent_path, _ = os.path.split(file_name)
        print(file_name)
        self.show_img_3d(file_name)

    def show_img_3d(self, file_name):
        self.img = skimage.io.imread(file_name)
        self.img = self.img.transpose(1,2,0)[:400, :400, :50]
        x,y,z = self.img.shape
        pos = np.mgrid[:x, :y, :z].transpose(1, 2, 3, 0) * 0.005 #0.005
        pos = pos.reshape(x*y*z, 3)
        img = self.img.reshape(self.img.size)
        color = np.empty((img.size, 4), dtype=np.float32)
        color[:,0] = color[:,1] = color[:,2] = img / np.max(img)
        color[:,3] = img / np.max(img) # color[:,3] = 0.02
        self.scatter_plot.setData(pos=pos, color=color, pxMode=True)

if __name__ == '__main__':
    # PyQt5 程序固定写法
    app = QApplication(sys.argv)

    # 将绑定了绘图控件的窗口实例化并展示
    window = Window()
    window.show()

    # PyQt5 程序固定写法
    sys.exit(app.exec())
