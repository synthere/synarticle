# -*- coding: utf-8 -*-
import sys, os

#pyside6-uic.exe  -o .\mainwin.py .\mainwin.ui
from mainwin import Ui_MainWindow

from PySide6.QtCore import QSize, Qt, QUrl, Signal, QTimer, QThread
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtWidgets import QApplication, QFileDialog, QMainWindow, QMessageBox, QWidget
from PySide6 import QtWidgets
import config
from typing import Iterator, Union
#pyinstaller artbing.spec

os.environ['QT_MEDIA_BACKEND'] = 'windows'

import subprocess
from functools import wraps

# save original function
__old_Popen = subprocess.Popen

# create wrapper to be called instead of original one
@wraps(__old_Popen)
def new_Popen(*args, startupinfo=None, **kwargs):
    if startupinfo is None:
        startupinfo = subprocess.STARTUPINFO()

    # way 1, as SO suggests:
    # create window
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    # and hide it immediately
    startupinfo.wShowWindow = subprocess.SW_HIDE

    # way 2
    #startupinfo.dwFlags = subprocess.CREATE_NO_WINDOW
    return __old_Popen(*args, startupinfo=startupinfo, **kwargs)
import v2art
# monkey-patch/replace Popen
subprocess.Popen = new_Popen

def get_base_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return base_path

class TranslatorThread(QThread):

    signal_progress_update = Signal(list)
    signal_timer = Signal(str)

    def __init__(self, input_file, source_lang, target_lang, api_key, output_path):
        super().__init__() #TranslatorThread, self
        self.inputfile = input_file
        self.source_lang = source_lang
        self.target_lang = target_lang
        self.api_key = api_key
        self.outputfilePath = output_path
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(1000)  # 1000ms

        self.v2art = v2art.Video2Art()
        self.art_stat = 0
    def run(self):
        #self.art_stat = 1

        self.v2art.trans(self.inputfile, self.source_lang, self.target_lang, self.api_key, self.outputfilePath)
        config.logger.info('audio mode finish')

        self.signal_timer.emit("finish")
        #self.art_stat = 0
    def update_progress(self):

        percent = self.v2art.translate_percent
        #print("to emiit:", percent)
        self.signal_progress_update.emit([percent, 100])

    def finish(self):
        self.signal_progress_update.emit([100, 100])
        self.timer.stop()

from regwin import Ui_RegisterWin
class RegWindows(QWidget, Ui_RegisterWin):
    reg_closed = Signal(str)
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.show()
        self.sel_lic_file.pressed.connect(self.sel_lic)
        self.activat_but.pressed.connect(self.activate_lic)
        self.lic_file = ''
        self.reg_stat = False
    def sel_lic(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, 'Select audio file', '', 'Licence File(*.bin);;All Files (*)',
                                              options=options)
        self.sel_lic_file = file

    def closeEvent(self, event):
        print("widget is closing")
        self.reg_closed.emit("closed")
    def activate_lic(self):
        from register import LicRegister

        lic_num = self.lic_code_txt.toPlainText()
        if lic_num != "":
            lic = lic_num
            print("lic:", lic)
        elif self.sel_lic_file != "":
            with open(self.sel_lic_file, 'r') as fp:
                lic = fp.read()
                # validate
        else:
            return
        lr = LicRegister()
        reg_file = 'reg.txt'

        res = lr.register(lic, reg_file)
        if res:
            self.reg_stat = True
            QMessageBox.warning(None, "Sucess", "Registered sucessfully!")
        else:
            QMessageBox.warning(None, "Fail", "Register failed!")


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.inputfile = ''
        self.outputfilePath = ''

        self.startbut.pressed.connect(self.startart)
        self.select_inputpath.pressed.connect(self.select_input_file)
        self.select_savepath.pressed.connect(self.save_out_file)

        menu_bar = self.menuBar()
        help_menu = menu_bar.addMenu("Help")

        reg_action = help_menu.addAction("Register")
        about_action = help_menu.addAction("About")

        reg_action.triggered.connect(self.show_reg_window)
        about_action.triggered.connect(self.show_about_dialog)

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()

        self.translate_process_bar.hide()
        self.unlimit_use = False # limit file length
        self.check_reg_stat()
        self.reg_win = RegWindows()
        self.reg_win.reg_closed.connect(self.reg_reset)
        self.show()
    def reg_reset(self):
        print("reg windows closed, reg res:", self.reg_win.reg_stat)
        if self.reg_win.reg_stat:
            self.unlimit_use = True
    def check_reg_stat(self):
        from register import LicRegister
        lr = LicRegister()
        reg_file = 'reg.txt'
        auth = lr.checkAuthored(reg_file)
        if auth:
            print("unlimit use")
            self.unlimit_use = True
    def show_reg_window(self):

        self.reg_win.show()
        self.reg_win .setWindowTitle("Register")

    def get_current_translator(self):
        return self.translator.currentText()

    def show_about_dialog(self):
        about_text = "<h3>Synthere Art 1.0</h3>" \
                     "<p style='font-size: 12px;'>Copyright © 2024 <a href='https://www.synthere.com'>Synthere</a></p>"
                     #"<ul style='font-size: 14px;'>" \
                     #"<li>More info <a href='https://www.example.com'>Synthere</a></li>" \
                     #"</ul>"
        if self.unlimit_use:
            about_text +="<p style='font-size: 12px;'>Registerd Version. </p>"
        else:
            about_text += "<p style='font-size: 12px;'>Preview Version. Support file less than 30s.</p>"

        about_box = QMessageBox()
        about_box.setWindowTitle("About")
        about_box.setTextFormat(Qt.AutoText)
        about_box.setText(about_text)

        about_box.exec()
    def save_out_file(self):
        options = QFileDialog.Options()
        #file, _ = QFileDialog.getSaveFileName(self, 'Save file', '', 'Video File(*.mp4 *.avi *.mov *.mpg *.mkv);;All Files (*)', options=options)
        file = QFileDialog.getExistingDirectory(self, "Select path")
        print("set output file:", file)
        if "" == file.strip():
            return
        self.outputfilePath = file
        self.savepath.setText(': ' + file) #os.path.basename(file)
    def select_input_file(self):
        options = QFileDialog.Options()
        file, _ = QFileDialog.getOpenFileName(self, 'Select audio file', '', 'Video File(*.mp4);;All Files (*)',
                                              options=options)
        self.inputfile = file
        self.input_file_line.setText(file)
        #self.inputpath_2.setText(file)#os.path.basename(file)

    def get_file_duration(self, video_file):
        from moviepy.editor import VideoFileClip
        vc = VideoFileClip(video_file)
        dur = vc.duration
        print("file dur:", dur)
        vc.close()
        return dur
    def get_current_api_key(self):
        return self.api_key.toPlainText()

    def get_current_input_file(self):
        return self.input_file_line.text()

    def startart(self):
        self.input_file = self.get_current_input_file()
        print("input file:", self.input_file)
        if '' == self.outputfilePath or '' == self.inputfile:
            print("invalid set")
            QMessageBox.warning(None, "Error", "Input file or output path not set!")
            return

        #if self.get_file_duration(self.inputfile) > 30 and False == self.unlimit_use:
        #    QMessageBox.warning(None, "Error", "File duration > 30s, unsupported in preview version. You can register to have unlimit usage.")
        #    return

        self.startbut.setEnabled(False)
        source_lang = 'english' #self.get_current_source_lang
        target_lang = 'cn'#self.get_current_target_lang()
        api_key = self.get_current_api_key()
        print("apikey:", api_key)

        self.translate_process_bar.setValue(0)
        self.translate_process_bar.show()
        self.transthread = TranslatorThread(self.inputfile, source_lang, target_lang, api_key, self.outputfilePath)
        self.transthread.signal_progress_update.connect(self.update_progress)
        self.transthread.signal_timer.connect(self.update_progress_timer)
        self.transthread.start()
        #
    def update_progress(self, values):
        print("to update val:", values)
        self.translate_process_bar.setValue(values[0])
    def update_progress_timer(self):
        self.transthread.finish()
        self.startbut.setEnabled(True)


