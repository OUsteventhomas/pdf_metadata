from PyQt4 import QtGui, QtCore

import sys
from engine_core.qt_main import Main

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)

    main_window = Main()
    main_window.show()

    sys.exit(app.exec_())