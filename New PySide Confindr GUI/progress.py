import sys
import os
import platform
from PySide2 import *
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ui_progress import *

# Global values
global progressBarValue

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #QTIMER USED TO DELAY PROGRESS BAR
        self.timer - QtCore.QTimer()
        self.timer.timeout.connect(self.appProgress)

        # Time interval in miliseconds for the progress bar to change value
        self.timer.start(100)

        self.show()

    # Lets degine appProgress function
    def appProgress(self):
        # Access the global variable progressBarValue
        global progressBarValue

        # Apply progressBarValue to the progressBar
        self.ui.progressBar.setValue(progressBarValue)

        if progressBarValue > 100:
             self.timer.stop()
             self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())