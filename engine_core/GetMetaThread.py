from PyQt4 import QtGui, QtCore
import os
import csv
import pyPdf


class GetMetaThread(QtCore.QThread):
    trigger = QtCore.pyqtSignal(str)
    clear_trigger = QtCore.pyqtSignal()

    output_list = []
    working_dir = os.getcwd()
    list_of_fields = ["File", "Title", "Keywords", "Author", "Subject"]

    def __init__(self, parent=None, folder_entry=None, text_output=None):
        super(GetMetaThread, self).__init__(parent)
        self.folder_entry = folder_entry
        self.text_output = text_output

        self.csv_file = self.working_dir + '\\meta_spreadsheet\\metadata_manipulation.csv'

    def run(self):
        self.clear_trigger.emit()

        pdf_directory = self.folder_entry.text()

        if len(pdf_directory) > 0:
            if os.path.isdir(pdf_directory):
                for root, _, files in os.walk(str(pdf_directory)):
                    for f in files:
                        # If the next check fails, might institute something like:
                        # if os.path.split('.')[-1].upper() == 'PDF'
                        if os.path.splitext(f)[1].upper() == '.PDF':
                            full_path = os.path.join(root, f)
                            self.__file_reader(full_path)

                            self.trigger.emit('Finished Processing File: %s' % full_path)
                self.__output_csv()
                self.trigger.emit("\nAll PDF metadata extracted successfully.\n")
            else:
                self.trigger.emit("The folder path you entered does not exist.")
        else:
            self.trigger.emit("You must enter a folder to build metadata from.")

    def __file_reader(self, my_file):
        with open(my_file, 'rb') as pdf_to_read:
            pdf_reader = pyPdf.PdfFileReader(pdf_to_read)
            self.pdf_info = pdf_reader.getDocumentInfo()

        self.__pdf_meta_parser(my_file)

    def __pdf_meta_parser(self, my_file):
        temp_list = []
        meta = self.pdf_info

        pdf_title = ''
        pdf_subject = ''
        pdf_author = ''
        pdf_keywords = ''

        if meta is not None:
            pdf_title = meta["/Title"] if "/Title" in meta else ""
            pdf_subject = meta["/Subject"] if "/Subject" in meta else ""
            pdf_author = meta["/Author"] if "/Author" in meta else ""
            pdf_keywords = meta["/Keywords"] if "/Keywords" in meta else ""

        temp_list.extend([my_file, pdf_title, pdf_keywords, pdf_author, pdf_subject])

        self.output_list.append(temp_list)


    def __clear_output(self):
        self.ui.textOutput.setText('')

    def __output_csv(self):
        os.chdir(self.working_dir)
        with open(self.csv_file, 'wb') as my_document:
            meta_writer = csv.writer(my_document, delimiter=',')
            meta_writer.writerow(self.list_of_fields)
            for o in self.output_list:
                meta_writer.writerow(o)
        self.output_list = []