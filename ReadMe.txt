This small script was designed to handle adding and changing the metadata presented in a PDF file (found by pressing Ctrl+D in Acrobat). It also uses qpdf to enable fast web viewing (linear optimization).

Requirements:
Python 2.7
PyQt4
pyPdf
Windows OS

Thanks to qpdf for allowing usage of their software. I have not modified the qpdf software so it may be included here per their licensing agreement. The qpdf website is located here: http://qpdf.sourceforge.net/

To use the program, simply run the file "main.py"

Paste the folder location of the PDF file(s) you would like to process into the top line.
All metadata is extracted to the csv file located in ./meta_spreadsheet
This information can be updated in the spreadsheet and reapplied to all of the files.
By default, when the metadata is updated on the PDF file linear optimization (fast web view) is also enabled.
