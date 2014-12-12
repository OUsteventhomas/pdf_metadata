from PyQt4 import uic
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from engine_core.GetMetaThread import GetMetaThread
from engine_core.ApplyMetaThread import ApplyMetaThread
from engine_core.FastWebView import FastWebView

(Ui_MainWindow, QMainWindow) = uic.loadUiType('mainwindow.ui')


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.__setup_ui()

    def __del__(self):
        self.ui = None

    def __setup_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Required to start and call a file
        self._thread = GetMetaThread(self, folder_entry=self.ui.folderEntry)
        self._thread.trigger.connect(self.__update_text)

        self._thread.clear_trigger.connect(self.__clear_text)

        # Required to start and call a file
        self._meta = ApplyMetaThread(self)
        self._meta.trigger.connect(self.__update_text)

        # Required to start and call a file
        self._fastweb = FastWebView(self, folder_entry=self.ui.folderEntry)
        self._fastweb.trigger.connect(self.__update_text)


        # Button commands to call functions
        self.ui.exportButton.clicked.connect(self._thread.start)
        self.ui.folderEntry.returnPressed.connect(self._thread.start)
        self.ui.applyButton.clicked.connect(self._meta.start)
        self.ui.fastWebViewButton.clicked.connect(self._fastweb.start)

    def __update_text(self, value):
        self.ui.textOutput.append(value)

    def __clear_text(self):
        self.ui.textOutput.setText('')