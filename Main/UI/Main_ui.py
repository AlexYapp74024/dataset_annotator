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
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractScrollArea, QApplication, QComboBox, QFrame,
    QGraphicsView, QGridLayout, QGroupBox, QHBoxLayout,
    QLabel, QLineEdit, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QScrollArea, QSizePolicy,
    QSpacerItem, QSplitter, QStatusBar, QTabWidget,
    QVBoxLayout, QWidget)
import Icons_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(886, 584)
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
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
        self.pb_open_proj = QPushButton(self.groupBox)
        self.pb_open_proj.setObjectName(u"pb_open_proj")

        self.horizontalLayout.addWidget(self.pb_open_proj)

        self.page_frame = QFrame(self.groupBox)
        self.page_frame.setObjectName(u"page_frame")
        self.page_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.page_frame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.page_frame)
        self.horizontalLayout_3.setSpacing(1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.pb_prev = QPushButton(self.page_frame)
        self.pb_prev.setObjectName(u"pb_prev")
        icon = QIcon()
        icon.addFile(u":/buttons/Prev.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_prev.setIcon(icon)

        self.horizontalLayout_3.addWidget(self.pb_prev)

        self.le_page = QLineEdit(self.page_frame)
        self.le_page.setObjectName(u"le_page")
        self.le_page.setEnabled(False)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_page.sizePolicy().hasHeightForWidth())
        self.le_page.setSizePolicy(sizePolicy)
        self.le_page.setMaximumSize(QSize(16777215, 16777215))
        self.le_page.setMaxLength(10)
        self.le_page.setAlignment(Qt.AlignmentFlag.AlignJustify|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.le_page)

        self.lb_pageMax = QLabel(self.page_frame)
        self.lb_pageMax.setObjectName(u"lb_pageMax")

        self.horizontalLayout_3.addWidget(self.lb_pageMax)

        self.pb_next = QPushButton(self.page_frame)
        self.pb_next.setObjectName(u"pb_next")
        icon1 = QIcon()
        icon1.addFile(u":/buttons/Next.png", QSize(), QIcon.Normal, QIcon.Off)
        self.pb_next.setIcon(icon1)

        self.horizontalLayout_3.addWidget(self.pb_next)


        self.horizontalLayout.addWidget(self.page_frame)

        self.cb_mode = QComboBox(self.groupBox)
        self.cb_mode.setObjectName(u"cb_mode")

        self.horizontalLayout.addWidget(self.cb_mode)

        self.pb_processed = QPushButton(self.groupBox)
        self.pb_processed.setObjectName(u"pb_processed")
        self.pb_processed.setEnabled(True)
        self.pb_processed.setAutoFillBackground(False)
        self.pb_processed.setCheckable(True)

        self.horizontalLayout.addWidget(self.pb_processed)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(self.annotate_tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy1)
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.splitter = QSplitter(self.groupBox_2)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.graphicsView = QGraphicsView(self.splitter)
        self.graphicsView.setObjectName(u"graphicsView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(4)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.graphicsView.sizePolicy().hasHeightForWidth())
        self.graphicsView.setSizePolicy(sizePolicy2)
        self.splitter.addWidget(self.graphicsView)
        self.frame = QFrame(self.splitter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.frame)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.splitter_2 = QSplitter(self.frame)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Orientation.Vertical)
        self.gb_label_group = QGroupBox(self.splitter_2)
        self.gb_label_group.setObjectName(u"gb_label_group")
        self.gb_label_group.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.verticalLayout_3 = QVBoxLayout(self.gb_label_group)
        self.verticalLayout_3.setSpacing(3)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.gb_label_group)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(100, 0))
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollArea.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignTop)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 254, 116))
        self.label_group = QVBoxLayout(self.scrollAreaWidgetContents)
        self.label_group.setSpacing(2)
        self.label_group.setObjectName(u"label_group")
        self.label_group.setContentsMargins(2, 2, 2, 2)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_3.addWidget(self.scrollArea)

        self.pb_add_class = QPushButton(self.gb_label_group)
        self.pb_add_class.setObjectName(u"pb_add_class")

        self.verticalLayout_3.addWidget(self.pb_add_class)

        self.splitter_2.addWidget(self.gb_label_group)
        self.groupBox_3 = QGroupBox(self.splitter_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox_3)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.bbox_list = QListWidget(self.groupBox_3)
        self.bbox_list.setObjectName(u"bbox_list")

        self.verticalLayout_2.addWidget(self.bbox_list)

        self.splitter_2.addWidget(self.groupBox_3)

        self.verticalLayout_4.addWidget(self.splitter_2)

        self.splitter.addWidget(self.frame)

        self.horizontalLayout_2.addWidget(self.splitter)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.tabWidget.addTab(self.annotate_tab, "")

        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QStatusBar(MainWindow)
        self.statusBar.setObjectName(u"statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.groupBox.setTitle("")
        self.pb_open_proj.setText(QCoreApplication.translate("MainWindow", u"Open Project", None))
        self.pb_prev.setText("")
        self.le_page.setText(QCoreApplication.translate("MainWindow", u"0", None))
        self.lb_pageMax.setText("")
        self.pb_next.setText("")
        self.cb_mode.setCurrentText("")
        self.pb_processed.setText(QCoreApplication.translate("MainWindow", u"Processed", None))
        self.groupBox_2.setTitle("")
        self.gb_label_group.setTitle(QCoreApplication.translate("MainWindow", u"Classes", None))
        self.pb_add_class.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Bounding boxes", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.annotate_tab), QCoreApplication.translate("MainWindow", u"Annotate", None))
    # retranslateUi

