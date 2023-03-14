import sys

from PyQt5.QtWidgets import QApplication, QDesktopWidget

from labelNeuron.control.controller import Controller
from labelNeuron.view.gui import GUI

def main():
    start_gui()

def start_gui():
    app = QApplication(sys.argv)

    # Setup Model-View-Control structure
    control = Controller()
    view = GUI(control)

    # Install event filter to catch user interventions
    app.installEventFilter(view)

    # Start GUI
    view.show()

    app.setStyle("Fusion")
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - view.width()) // 2
    height = (desktop.height() - view.height()) // 2
    view.move(width, height)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
