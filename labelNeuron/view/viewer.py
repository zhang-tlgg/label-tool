from typing import Tuple

import numpy as np
from OpenGL import GLU
from PyQt5 import QtGui, QtOpenGL
import pyqtgraph.opengl as gl
from pyqtgraph.opengl import GLViewWidget

from ..definitions.types import Color4f, Point2D

# Main widget for presenting the 3D image
class GLViewWidget(GLViewWidget):

    def __init__(self, parent=None, devicePixelRatio=None, rotationMethod='euler'):
        super().__init__(parent, devicePixelRatio, rotationMethod)
        
        # Objects to be drawn
        self.crosshair_pos: Point2D = (0, 0)
        self.crosshair_col: Color4f = (0, 1, 0, 1)
        
    # Translates the 2D cursor position from screen plane into 3D world space coordinates
    def get_world_coords(self, x: float, y: float) -> Tuple[float, float, float]:
        viewport = self.getViewport()
        modelview = np.array(self.viewMatrix().data()).reshape(4, 4)
        projection = np.array(self.projectionMatrix().data()).reshape(4, 4)
        real_y = viewport[3] - y  # adjust for down-facing y positions

        mod_x, mod_y, mod_z = GLU.gluUnProject(
            x, real_y, 1, modelview, projection, viewport
        )
        camera_pos = self.cameraPosition()
        self.draw_line([camera_pos.x(), camera_pos.y(), camera_pos.z()], [mod_x, mod_y, mod_z])
        return mod_x, mod_y, mod_z

    def draw_line(self, pos1, pos2):
        line = gl.GLLinePlotItem(pos=[pos1, pos2], color=(1, 1, 0, 1), width=2)
        self.addItem(line)
        
