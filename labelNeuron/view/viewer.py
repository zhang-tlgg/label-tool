from pyqtgraph.opengl import GLViewWidget

from ..definitions.types import Color4f, Point2D

# Main widget for presenting the 3D image
class GLViewWidget(GLViewWidget):

    def __init__(self, parent=None, devicePixelRatio=None, rotationMethod='euler'):
        super().__init__(parent, devicePixelRatio, rotationMethod)
        
        # Objects to be drawn
        self.crosshair_pos: Point2D = (0, 0)
        self.crosshair_col: Color4f = (0, 1, 0, 1)