# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'Main.ui'
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
from PySide6.QtWidgets import (QApplication, QGraphicsView, QGridLayout, QGroupBox,
    QHBoxLayout, QMainWindow, QMenu, QMenuBar,
    QPushButton, QScrollArea, QSizePolicy, QSpacerItem,
    QTabWidget, QVBoxLayout, QWidget)
import Icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(886, 584)
        self.actionNew_Project = QAction(MainWindow)
        self.actionNew_Project.setObjectName(u"actionNew_Project")
        self.actionOpen_Projects = QAction(MainWindow)
        self.actionOpen_Projects.setObjectName(u"actionOpen_Projects")
        self.actionAdd_Images = QAction(MainWindow)
        self.actionAdd_Images.setObjectName(u"actionAdd_Images")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(6, 0, 6, 6)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.annotate_tab = QWidget()
        self.annotate_tab.setObjectName(u"annotate_tab")
        self.verticalLayout = QVBoxLayout(self.annotate_tab)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(3, 3, 3, 3)
        self.groupBox = QGroupBox(self.annotate_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.horizontalLayout = QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(3, 3, 3, 3)
        self.btn_prev = QPushButton(self.groupBox)
        self.btn_prev.setObjectName(u"btn_prev")
        icon = QIcon()
        icon.addFile(u":/buttons/Prev.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_prev.setIcon(icon)

        self.horizontalLayout.addWidget(self.btn_prev)

        self.btn_next = QPushButton(self.groupBox)
        self.btn_next.setObjectName(u"btn_next")
        icon1 = QIcon()
        icon1.addFile(u":/buttons/Next.png", QSize(), QIcon.Normal, QIcon.Off)
        self.btn_next.setIcon(icon1)

        self.horizontalLayout.addWidget(self.btn_next)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setEnabled(True)
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setCheckable(True)

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.annotate_tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(3, 3, 3, 3)
        self.graphicsView = QGraphicsView(self.groupBox_2)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy)

        self.horizontalLayout_2.addWidget(self.graphicsView)

        self.gb_label_group = QGroupBox(self.groupBox_2)
        self.gb_label_group.setObjectName(u"gb_label_group")
        self.gb_label_group.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_3 = QVBoxLayout(self.gb_label_group)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.gb_label_group)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(100, 0))
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 98, 436))
        self.label_group = QVBoxLayout(self.scrollAreaWidgetContents)
        self.label_group.setSpacing(2)
        self.label_group.setObjectName(u"label_group")
        self.label_group.setContentsMargins(2, 2, 2, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.pb_add_class = QPushButton(self.gb_label_group)
        self.pb_add_class.setObjectName(u"pb_add_class")

        self.verticalLayout_3.addWidget(self.pb_add_class)


        self.horizontalLayout_2.addWidget(self.gb_label_group)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.annotate_tab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 886, 33))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName(u"menuFile")
        self.menuImages = QMenu(self.menubar)
        self.menuImages.setObjectName(u"menuImages")
        MainWindow.setMenuBar(self.menubar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuImages.menuAction())
        self.menuFile.addAction(self.actionNew_Project)
        self.menuFile.addAction(self.actionOpen_Projects)
        self.menuImages.addAction(self.actionAdd_Images)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionNew_Project.setText(QCoreApplication.translate("MainWindow", u"New Project", None))
        self.actionOpen_Projects.setText(QCoreApplication.translate("MainWindow", u"Open Projects", None))
        self.actionAdd_Images.setText(QCoreApplication.translate("MainWindow", u"Add Images", None))
        self.groupBox.setTitle("")
        self.btn_prev.setText("")
        self.btn_next.setText("")
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"Segment", None))
        self.groupBox_2.setTitle("")
        self.gb_label_group.setTitle("")
        self.pb_add_class.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.annotate_tab), QCoreApplication.translate("MainWindow", u"Annotate", None))
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", u"Projects", None))
        self.menuImages.setTitle(QCoreApplication.translate("MainWindow", u"Images", None))
    # retranslateUi

