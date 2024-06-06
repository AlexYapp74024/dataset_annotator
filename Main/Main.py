from __future__ import annotations
from functools import wraps

from PySide6 import (
    QtWidgets as qtw, 
    QtGui as qtg, 
    QtCore as qtc,
)
from PySide6.QtCore import Qt
from Main.UI.Main_ui import Ui_MainWindow
from Main.Add_Label import  Add_Label_Dialog

from settings import settings
from Utils import *

from typing import Dict
import re

class MainApp(qtw.QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.pb_add_class.clicked.connect(self.add_label_dialog)
        self.label_to_buttons : Dict[str, qtw.QPushButton] = {}
        self.current_label : str = ""

    def add_images(self):
        print("AAA")

    def add_label_dialog(self):
        add_label_dialog = Add_Label_Dialog()
        
        def accepted():
            text = add_label_dialog.textEdit.toPlainText()
            classes = [line.strip() for line in re.split(r',|\n',text)]
            [self.add_label(c) for c in classes if c != '']

        add_label_dialog.accepted.connect(accepted)
        add_label_dialog.exec()
        
    def add_label(self, class_label:str):
        # Return if the class label already exists
        if self.label_to_buttons.get(class_label, False): return

        def select_label_setup(label:str):
            def action(): self.select_label(label)
            return action

        button = qtw.QPushButton(text=class_label)
        button.setCheckable(True)
        button.clicked.connect(select_label_setup(class_label))
        self.label_group.layout().addWidget(button)

        if self.current_label == "" :
            self.current_label = class_label
            button.setChecked(True)

        self.label_to_buttons[class_label] = button
        self.update()

    def select_label(self, label):
        self.label_to_buttons[self.current_label].setChecked(False)

        self.current_label = label
        self.label_to_buttons[label].setChecked(True)

    def _lock_table():
        def func(foo, ):
            @wraps(foo)
            def magic(self:MainApp, *args, **kwargs):
                try:
                    out = foo(self, *args,**kwargs)
                except Exception as e: 
                    raise e
                
                return out

            return magic
        return func
