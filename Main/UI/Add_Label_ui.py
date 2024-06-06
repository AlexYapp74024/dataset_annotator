# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Add_Label.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QLabel, QSizePolicy, QTextEdit, QVBoxLayout,
    QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(414, 215)
        Dialog.setModal(True)
        self.actionA = QAction(Dialog)
        self.actionA.setObjectName(u"actionA")
        self.actionA.setMenuRole(QAction.MenuRole.NoRole)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")
        self.textEdit.setInputMethodHints(Qt.InputMethodHint.ImhLowercaseOnly|Qt.InputMethodHint.ImhMultiLine)

        self.verticalLayout.addWidget(self.textEdit)

        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.buttonBox.setCenterButtons(False)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Add Labels", None))
        self.actionA.setText(QCoreApplication.translate("Dialog", u"A", None))
#if QT_CONFIG(shortcut)
        self.actionA.setShortcut(QCoreApplication.translate("Dialog", u"Ctrl+Return", None))
#endif // QT_CONFIG(shortcut)
        self.label.setText(QCoreApplication.translate("Dialog", u"Class should be separated by commas or new lines", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"[Ctrl-Enter] Confirm, [Esc] Cancel", None))
    # retranslateUi

