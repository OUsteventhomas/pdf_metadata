from PyQt4 import QtGui, QtCore
import os
import re
import subprocess


class FastWebView(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)
    clear_trigger = QtCore.pyqtSignal()

    output_list = []
    python_directory = os.getcwd()
    source_file = ''

    def __init__(self, parent=None, folder_entry=None, text_output=None):
        super(FastWebView, self).__init__(parent)
        self.folder_entry = folder_entry
        self.text_output = text_output

    def run(self):
        self.clear_trigger.emit()
        pdf_directory = self.folder_entry.text()

        if len(pdf_directory) > 0:
            if os.path.isdir(pdf_directory):
                for root, _, files in os.walk(str(pdf_directory)):
                    for f in files:
                        if os.path.splitext(f)[1].upper() == '.PDF':
                            self.source_file = os.path.join(root, f)
                            self.__fast_web_view()
                            self.trigger.emit('Finished Processing File: %s' % self.source_file)
                self.trigger.emit("\nAll PDF's have fast web view enabled.\n")
            else:
                self.trigger.emit("The folder path you entered does not exist.")
        else:
            self.trigger.emit("You must enter a folder to enable fast web viewing.")

    def __fast_web_view(self):
        # generate temp_file_path again
        self.__source_rename()
        # path to qpdf
        qpdf_path = self.python_directory + '\\qpdf\\bin\\qpdf.exe'
        # call qpdf install to enable fastwebview
        subprocess.call([qpdf_path, '--linearize', self.source_file, self.temp_file_path])
        # file replace
        self.__file_replacement()

    def __file_replacement(self):
        os.remove(self.source_file)
        os.rename(self.temp_file_path, self.source_file)

    def __source_rename(self):
        self.temp_file_path = re.sub('\.PDF', '-temp.pdf', self.source_file.upper())