"""
This file will contain methods which will be used for the PDF meta data functionality.
from: http://svn.certrec.com:81/svn/Python/FileManagement/trunk/core/engines/file_cabinet/file_meta_engine.py
"""

import os

#from flask import jsonify, request
from pyPdf import PdfFileReader, PdfFileWriter
from pyPdf.generic import NameObject, createStringObject

# from core.engines.core_engine.engine_base import EngineBase
# from core.engines.file_cabinet.file_engine import FileEngine
# from core.engines.file_cabinet.file_group_engine import FileGroupEngine
# from core.common.file_helper import clean_file_path
# from core.init_app import current_app


class FileMetaEngine(EngineBase):
    allowed_characters = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ %();?,.:!@$-/&_|<>=\"'"

    def __init__(self, db_source=None):
        """
        This __init__ function will call the super() function in EngineBase
        The EngineBase will create the default engine, or the testing engine
        depending on how this class is invoked.
        """

        # As of right now, there is no base db source for this engine. However,
        # I am using the EngineBase just in case for later
        super(FileMetaEngine, self).__init__(None, db_source)

        self.file_engine = FileEngine()
        self.file_group_engine = FileGroupEngine()

    def get_meta_data_for_file(self, file_id, status_id):
        if status_id == 1:
            source = clean_file_path(current_app.config['UPLOADED_FILES_DEST'])
        else:
            source = clean_file_path(current_app.config['UPLOADED_PENDING_DEST'])

        file_record = self.file_engine.get_file(file_id, status_id)
        pdf_info = {'title': "", 'subject': "", 'author': "", 'keywords': "", 'error': None, 'hide_meta': False}
        if file_record is not None:
            source_file = '%s/%s/%s' % (source, file_record['file_path'], file_record['file_name'])
            from pyPdf import PdfFileReader
            if os.path.isfile(source_file):
                try:
                    with open(source_file, "rb") as pdf_to_read:
                        reader = PdfFileReader(pdf_to_read)
                        meta = reader.getDocumentInfo()
                        if meta is not None:
                            pdf_info["title"] = meta["/Title"] if "/Title" in meta else ""
                            pdf_info["subject"] = meta["/Subject"] if "/Subject" in meta else ""
                            pdf_info["author"] = meta["/Author"] if "/Author" in meta else ""
                            pdf_info["keywords"] = meta["/Keywords"] if "/Keywords" in meta else ""
                            pdf_info["error"] = None
                            pdf_info['hide_meta'] = len(reader.outlines) > 0
                        pdf_to_read.close()
                except Exception, ex:
                    pdf_info["error"] = str(ex)
            else:
                pdf_info["error"] = 'No File For Meta Data'
        else:
            pdf_info["error"] = 'No File For Meta Data'

        return jsonify({'results': pdf_info})

    def save_meta_data_for_file(self, file_id, status_id):
        if status_id == 1:
            source = clean_file_path(current_app.config['UPLOADED_FILES_DEST'])
        else:
            source = clean_file_path(current_app.config['UPLOADED_PENDING_DEST'])

        file_record = self.file_engine.get_file(file_id, status_id)

        source_file = '%s/%s/%s' % (source, file_record['file_path'], file_record['file_name'])

        title = request.form.get('title')
        author = request.form.get('author')
        subject = request.form.get('subject')
        keywords = request.form.get('keywords')

        title = str(self.__filter_valid_characters(title)).strip().upper()
        author = str(self.__filter_valid_characters(author)).strip().upper()
        subject = str(self.__filter_valid_characters(subject)).strip().upper()
        keywords = str(self.__filter_valid_characters(keywords)).strip().upper()

        temp_file_path = source_file.upper().replace('.PDF', '') + "-temp.pdf"

        with file(source_file, "rb") as input_file:
            input = PdfFileReader(input_file)
            output = PdfFileWriter()

            meta_data = output._info.getObject()
            meta_data.update({
                NameObject("/Title"): createStringObject(title),
                NameObject("/Author"): createStringObject(author),
                NameObject("/Subject"): createStringObject(subject),
                NameObject("/Keywords"): createStringObject(keywords)
            })

            for page in range(input.getNumPages()):
                output.addPage(input.getPage(page))

            with file(temp_file_path, "wb") as output_stream:
                output.write(output_stream)
                output_stream.close()

            input_file.close()

        os.remove(source_file)
        os.rename(temp_file_path, source_file)

    def __filter_valid_characters(self, value):
        return filter(lambda x: x in self.allowed_characters, value)