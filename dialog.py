from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog
import sys

class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()

        # Load the ui file
        uic.loadUi("Dialog.ui", self)

        # Define our widgets
        self.button = self.findChild(QPushButton, "fileButton")
        self.label = self.findChild(QLabel, "openFileLabel")

        # Clicks the button
        self.button.clicked.connect(self.clicker)

        # Shows the app
        self.show()

    def clicker(self):
        #self.label.setText("You Clicked the Button!")
        # Open File Dialog and choose which file type you want
        fileName = QFileDialog.getOpenFileName(self, "Open Da Magic File", "", "All Files (*);;Python Files(*.py);;PNG Files(*.png)")

        # Output file name to screen
        if fileName:
            self.openFileLabel.setText(fileName[0])


app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
