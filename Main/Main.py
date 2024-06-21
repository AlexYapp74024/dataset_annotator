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

from ProjectManager import ProjectManager
from ImageScene import ImageScene
from settings import settings
from Utils import *
from Labeling import Class_Label, LABELING_CLASSES

import pprint
from typing import Dict
import re

class MainApp(qtw.QMainWindow, Ui_MainWindow):

    class_update = qtc.Signal(np.ndarray)

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        self.label_to_buttons : Dict[Class_Label, qtw.QPushButton] = {}
        self.current_label : Class_Label = None
        self.proj_manager = ProjectManager()

        self.page_frame.hide()

        self.le_page.mousePressEvent = lambda _: self.le_page.selectAll()
        self.le_page.returnPressed.connect(lambda : (self.le_page.clearFocus(), self.set_page(int(self.le_page.text()))))

        self.scene = ImageScene(self.proj_manager)
        self.class_update.connect(self.scene.update_color)
        self.graphicsView.setScene(self.scene)
        self.scene.labels_changed.connect(self.update_list)
        self.scene.image_changed.connect(lambda : (self.graphicsView.resize(self.graphicsView.size()*1.1), self.graphicsView.resize(self.graphicsView.size()/1.1)))

        self.pb_add_class.clicked.connect(self.add_label_dialog)
        self.pb_open_proj.clicked.connect(self.change_project_dir_dialog)

        self.pb_next.pressed.connect(lambda : self.set_page(self.proj_manager.index + 1, True))
        self.pb_prev.pressed.connect(lambda : self.set_page(self.proj_manager.index - 1, True))

        self.bbox_list.currentItemChanged.connect(self.list_selected)
        self.pb_processed.clicked.connect(self.toggle_cheked)

        self.cb_mode.addItems(LABELING_CLASSES.keys())
        self.cb_mode.currentTextChanged.connect(lambda s : self.scene.set_up_label_manager(LABELING_CLASSES[s]))

        if settings["project_dir"] != "":
            self.change_project_dir(settings["project_dir"])

        self.pb_add_class.setEnabled(self.proj_manager.has_yaml_file())

    def add_label_dialog(self):
        add_label_dialog = Add_Label_Dialog()
        
        def accepted():
            text = add_label_dialog.textEdit.toPlainText()
            classes = [line.strip() for line in re.split(r',|\n',text)]
            for c in classes:
                if c == '': continue
                class_label = Class_Label(c)
                self.add_label(class_label) 
                self.proj_manager.classes += class_label

        add_label_dialog.accepted.connect(accepted)
        add_label_dialog.exec()

    def add_label(self, class_label:Class_Label):
        # Return if the button for class label already exists
        if self.label_to_buttons.get(class_label, False): return

        def select_label_setup(label:Class_Label):
            def action(): self.select_label(label)
            return action

        pixmap = qtg.QPixmap(100,100)
        pixmap.fill(qtg.QColor(*class_label.color))
        
        button = qtw.QPushButton(text=class_label.name,icon=qtg.QIcon(pixmap))
        button.setStyleSheet("text-align:left;")
        button.setCheckable(True)
        button.clicked.connect(select_label_setup(class_label))
        self.label_group.layout().addWidget(button)

        self.label_to_buttons[class_label] = button

        if self.current_label is None :
            self.current_label = class_label
            button.setChecked(True)
            self.class_update.emit(class_label)

        self.update()

    def select_label(self, label:Class_Label):
        self.label_to_buttons[self.current_label].setChecked(False)

        self.current_label = label
        self.label_to_buttons[label].setChecked(True)

        self.class_update.emit(label)

    def change_project_dir_dialog(self):
        file_name = qtw.QFileDialog()
        file_name.setFileMode(qtw.QFileDialog.FileMode.Directory)
        dir_name = file_name.getExistingDirectory(self, "Select Directory")
        self.change_project_dir(dir_name)        

    def change_project_dir(self, dir_name:str):
        if dir_name != '' : 
            settings["project_dir"] = dir_name
            self.save_settings()
            self.proj_manager.project_dir = dir_name

            [self.add_label(c) for c in self.proj_manager.classes.values()]
        
        self.pb_add_class.setEnabled(self.proj_manager.has_yaml_file())

        if self.proj_manager.has_image():
            self.setup_page_count()
        else: 
            self.page_frame.show()

    def save_settings(self):
        with open("settings.py", 'w') as f:
            out = pprint.pformat(settings, indent=4)
            f.write(f"settings = {out}")

    def setup_page_count(self):
        self.page_frame.show()
        self.le_page.setEnabled(True)
        max_page : int = len(self.proj_manager.images_paths)

        self.lb_pageMax.setText(f" / {max_page}")
        self.le_page.setInputMask("0" * len(str(max_page)))

        font = qtg.QFontMetrics(self.le_page.font())
        width = font.horizontalAdvance("0" * (len(str(max_page)) + 2))
        self.le_page.setFixedWidth(width)
        
        self.set_page(0, True)

    def set_page(self, page:int, upadte_le:bool = False):
        if upadte_le: 
            self.le_page.setText(f"{page}")
        if page < 0:
            page = 0
            self.le_page.setText(f"{page}")
        if page > (max_page := len(self.proj_manager.images_paths)):
            page = max_page
            self.le_page.setText(f"{page}")
        
        self.proj_manager.index = page
        self.scene.open_image_file(self.proj_manager.image_path, self.proj_manager.label_path)

    def segment(self):
        def confirm():
            msg = qtw.QMessageBox.question(self, "Download Model", "Model file not found, do you want to download it now?")
            return msg == qtw.QMessageBox.StandardButton.Yes
        
        # self.scene.update_image(image)

    def toggle_cheked(self):
        self.scene.show_processed = self.pb_processed.isChecked()
        self.scene.draw_bboxes()

    def update_list(self):
        self.bbox_list.clear()
        for i, label in enumerate(self.scene.labels):
            widget = qtw.QListWidgetItem("")
            widget.setData(1,i)
            widget.setText(self.proj_manager.classes[label.label_id].name)
            self.bbox_list.addItem(widget)
            pass

    def list_selected(self, current:qtw.QListWidgetItem, previous:qtw.QListWidgetItem):
        if current is None: return
        self.scene.current_label_index = current.data(1)
        self.scene.draw_bboxes()

    def keyPressEvent(self, event: qtg.QKeyEvent):
        self.scene.keyPress(event)