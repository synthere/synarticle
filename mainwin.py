# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwin.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QLabel,
    QLineEdit, QMainWindow, QMenuBar, QPlainTextEdit,
    QProgressBar, QPushButton, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(887, 274)
        MainWindow.setIconSize(QSize(20, 20))
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.startbut = QPushButton(self.centralwidget)
        self.startbut.setObjectName(u"startbut")
        self.startbut.setGeometry(QRect(730, 170, 151, 41))
        font = QFont()
        font.setFamilies([u"Microsoft YaHei UI"])
        font.setPointSize(12)
        font.setBold(True)
        self.startbut.setFont(font)
        self.startbut.setStyleSheet(u"")
        self.startbut.setFlat(False)
        self.select_inputpath = QPushButton(self.centralwidget)
        self.select_inputpath.setObjectName(u"select_inputpath")
        self.select_inputpath.setGeometry(QRect(17, 13, 111, 31))
        font1 = QFont()
        font1.setBold(True)
        self.select_inputpath.setFont(font1)
        self.select_savepath = QPushButton(self.centralwidget)
        self.select_savepath.setObjectName(u"select_savepath")
        self.select_savepath.setGeometry(QRect(420, 15, 111, 31))
        self.select_savepath.setFont(font1)
        self.savepath = QLabel(self.centralwidget)
        self.savepath.setObjectName(u"savepath")
        self.savepath.setGeometry(QRect(550, 25, 311, 16))
        font2 = QFont()
        font2.setItalic(False)
        self.savepath.setFont(font2)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 90, 111, 16))
        font3 = QFont()
        font3.setUnderline(False)
        self.label.setFont(font3)
        self.origin_lang = QComboBox(self.centralwidget)
        self.origin_lang.addItem("")
        self.origin_lang.addItem("")
        self.origin_lang.setObjectName(u"origin_lang")
        self.origin_lang.setGeometry(QRect(130, 90, 69, 22))
        self.translate_process_bar = QProgressBar(self.centralwidget)
        self.translate_process_bar.setObjectName(u"translate_process_bar")
        self.translate_process_bar.setGeometry(QRect(10, 190, 691, 23))
        self.translate_process_bar.setCursor(QCursor(Qt.UpArrowCursor))
        self.translate_process_bar.setValue(9)
        self.label_4 = QLabel(self.centralwidget)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(216, 91, 71, 16))
        self.target_lang = QComboBox(self.centralwidget)
        self.target_lang.addItem("")
        self.target_lang.setObjectName(u"target_lang")
        self.target_lang.setGeometry(QRect(280, 90, 81, 22))
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(420, 70, 441, 61))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.llm_type = QComboBox(self.frame)
        self.llm_type.addItem("")
        self.llm_type.setObjectName(u"llm_type")
        self.llm_type.setGeometry(QRect(80, 20, 69, 22))
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(170, 20, 61, 16))
        self.api_key = QPlainTextEdit(self.frame)
        self.api_key.setObjectName(u"api_key")
        self.api_key.setGeometry(QRect(230, 10, 201, 41))
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 20, 31, 16))
        font4 = QFont()
        font4.setPointSize(9)
        self.label_2.setFont(font4)
        self.frame_2 = QFrame(self.centralwidget)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setGeometry(QRect(10, 70, 371, 61))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.input_file_line = QLineEdit(self.centralwidget)
        self.input_file_line.setObjectName(u"input_file_line")
        self.input_file_line.setGeometry(QRect(150, 20, 221, 21))
        MainWindow.setCentralWidget(self.centralwidget)
        self.frame.raise_()
        self.frame_2.raise_()
        self.startbut.raise_()
        self.select_inputpath.raise_()
        self.select_savepath.raise_()
        self.savepath.raise_()
        self.label.raise_()
        self.origin_lang.raise_()
        self.translate_process_bar.raise_()
        self.label_4.raise_()
        self.target_lang.raise_()
        self.input_file_line.raise_()
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 887, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.startbut.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"SynthereArticle", None))
        self.startbut.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.select_inputpath.setText(QCoreApplication.translate("MainWindow", u"Video Path/Url", None))
        self.select_savepath.setText(QCoreApplication.translate("MainWindow", u"Result Path", None))
        self.savepath.setText(QCoreApplication.translate("MainWindow", u"Save the translated video and txt to", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Original language", None))
        self.origin_lang.setItemText(0, QCoreApplication.translate("MainWindow", u"EN", None))
        self.origin_lang.setItemText(1, QCoreApplication.translate("MainWindow", u"AutoDetect", None))

        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Target", None))
        self.target_lang.setItemText(0, QCoreApplication.translate("MainWindow", u"CN", None))

        self.llm_type.setItemText(0, QCoreApplication.translate("MainWindow", u"GLM", None))

        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Api Key", None))
        self.api_key.setPlainText(QCoreApplication.translate("MainWindow", u"xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"LLM ", None))
        self.input_file_line.setText(QCoreApplication.translate("MainWindow", u"Your video path or url ", None))
    # retranslateUi

