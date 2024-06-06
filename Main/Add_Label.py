from __future__ import annotations
from functools import wraps

from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc,
)
from PySide6.QtCore import Qt
from Main.UI.Add_Label_ui import Ui_Dialog

from settings import settings

from Utils import *

class Add_Label_Dialog(qtw.QDialog, Ui_Dialog):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.textEdit.setFocus()

    def keyPressEvent(self, event:qtg.QKeyEvent): 
        if event.key() == Qt.Key.Key_Return:
            self.accept()

