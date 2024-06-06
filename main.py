import sys
from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc
)

from Main.Main import MainApp

if __name__ == "__main__":
    app = qtw.QApplication()
    app.setStyle("Fusion")
    window = MainApp()
    window.show()
    # Just to force trigger the resize event to resize graphics view
    # window.resize(window.size()*1.1)
    sys.exit(app.exec())
