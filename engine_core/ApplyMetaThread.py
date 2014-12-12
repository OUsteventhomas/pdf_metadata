from PyQt4 import QtGui, QtCore
import os
import csv
from pyPdf import PdfFileReader, PdfFileWriter
from pyPdf.generic import NameObject, createStringObject
import re
from subprocess import call


class ApplyMetaThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)
    clear_trigger = QtCore.pyqtSignal()
    python_directory = os.getcwd()
    source_file = ''
    title = ''
    keywords = ''
    author = ''
    subject = ''
    temp_file_path = ''

    def __init__(self, parent=None, folder_entry=None, text_output=None):
        super(ApplyMetaThread, self).__init__(parent)
        self.folder_entry = folder_entry
        self.text_output = text_output

    def run(self):
        self.clear_trigger.emit()
        csv_file = self.python_directory + '\\meta_spreadsheet\\metadata_manipulation.csv'
        with open(csv_file, 'rb') as csvfile:
            csvreader = csv.reader(csvfile, delimiter=',')
            for row in csvreader:
                if row[0] != "File":
                    self.source_file = row[0]
                    self.title = row[1]
                    self.keywords = row[2]
                    self.author = row[3]
                    self.subject = row[4]
                    self.__source_rename()
                    self.trigger.emit('Processing %s' % self.source_file)
                    self.__pdf_meta_writer()

        self.trigger.emit('\nAll items in CSV have been processed.\n')

    def __source_rename(self):
        self.temp_file_path = re.sub('\.PDF', '-temp.pdf', self.source_file.upper())

    def __pdf_meta_writer(self):
        if os.path.isfile(self.source_file):
            with open(self.source_file, "rb") as input_file:
                fileinput = PdfFileReader(input_file)
                output = PdfFileWriter()

                meta_data = output._info.getObject()
                meta_data.update({
                    NameObject("/Title"): createStringObject(self.title),
                    NameObject("/Author"): createStringObject(self.author),
                    NameObject("/Subject"): createStringObject(self.subject),
                    NameObject("/Keywords"): createStringObject(self.keywords)
                })

                for page in range(fileinput.getNumPages()):
                    output.addPage(fileinput.getPage(page))

                with file(self.temp_file_path, "wb") as output_stream:
                    output.write(output_stream)
                    output_stream.close()

                input_file.close()

            self.__file_replacement()
            self.__fast_web_view()
        else:
            broken_file_path = str("File: %s not found!!!" % self.source_file)
            self.trigger.emit(broken_file_path)

    def __file_replacement(self):
        os.remove(self.source_file)
        os.rename(self.temp_file_path, self.source_file)

    def __fast_web_view(self):
        # generate temp_file_path again
        self.__source_rename()
        # path to qpdf
        qpdf_path = self.python_directory + '\\qpdf\\bin\\qpdf.exe'
        # call qpdf install to enable fastwebview
        call([qpdf_path, '--linearize', self.source_file, self.temp_file_path])
        # file replace
        self.__file_replacement()