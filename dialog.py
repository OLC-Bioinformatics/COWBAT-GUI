from PyQt5 import QtWidgets, uic, QtGui, QtCore
from main import main
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
import sys, openpyxl, csv, subprocess, os, pathlib, psutil, glob
from pathlib import Path

class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        self.test_out=str()

        # Load the ui file
        uic.loadUi("Dialog.ui", self)

        # Creates the layout of the box
        layout = QVBoxLayout()   

         # Adding the table widget to our window
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Shows the table widget (sorta idk it doesn't quite show)
        self.table_widget.show()

        # Define our widgets
        self.tableDisplayButton = self.findChild(QPushButton, "tableDisplayButton")
        self.analyzeResultsButton = self.findChild(QPushButton, "analyzeResultsButton")
        self.folderField = self.findChild(QLineEdit, "folderField")
        self.errorLabel = self.findChild(QLabel, "errorLabel")

        # Clicks the buttons
        self.analyzeResultsButton.clicked.connect(self.analyzeClicker)
        self.tableDisplayButton.clicked.connect(self.tableClicker)

        # Shows the app
        self.show()

    def analyzeClicker(self):

        # Gets the name of the folder with the data
        folderName = str(QFileDialog.getExistingDirectory(self, "Select Folder of Sequences"))
        print("This is the folder directory: " + folderName)

        # Checks if the folder selected contains any fastq.gz or fasta files which is what confindr uses. If not, return that idiot back
        if glob.glob(f'{folderName}/*.fastq.gz') or glob.glob(f'{folderName}/*.fasta'):
            # Prints a success message to say the file is found
            msg = QMessageBox()
            msg.setWindowTitle("Success")
            msg.setText("Successfully found folder.")
            msg.setIcon(QMessageBox.Information)
            msg.setInformativeText("You will have to select the file: confindr_report.csv when prompted in a few minutes in order to view results.")
            x = msg.exec_()

            # Uses the folder name as an argument to run ConFindr and get the results. Mem represents total allocated memory that is being reserved for confindr
            self.test_out = os.path.join(folderName, "test_out")
            mem = int(0.85 * float(psutil.virtual_memory().total) / 1024)
            subprocess.run(f'confindr -i {folderName} -o {self.test_out} --rmlst -Xmx {mem}K', shell=True)

            # Then, opens the window to allow you to select the confindr_report.csv file to show the graph
            self.tableClicker()

        # Checks if there is a folder containing your sequence or if there is anything written
        elif len(folderName) == 0:
            self.errorLabel.setText("Please select a folder to continue")

        else:
            self.errorLabel.setText("The folder does not contain any fastq.gz or fasta files")
            

    def tableClicker(self):
        # Open File Dialog and choose which file type you want
        fileName = QFileDialog.getOpenFileName(self, "Open Da Magic File", "", "CSV Files(*.csv);;XLSX Files(*.xlsx)")

        # Output file name to screen
        if fileName:
            self.test_out = os.path.dirname(fileName[0])
            #print(fileName)

            # Custom methods use to extract data into the GUI
            self.convert_csv_to_xlsx()
            self.load_data(fileName[0])

#---------------------------------------------------------------------------------

    # Converts csv files to xlsx fiels
    def convert_csv_to_xlsx(self):
        wb = openpyxl.Workbook()
        ws = wb.active

        # Delimiter turns a single cell line into multiple columns by breaking the line into different columns seperated by ","
        with open(os.path.join(self.test_out,"confindr_report.csv")) as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                ws.append(row)

        wb.save(os.path.join(self.test_out,"confindr_report.xlsx")) 
        
    # Loads the data from the xlsx file to the table widget in PyQt5
    def load_data(self, fileName):
        # Gathers the path and locates the excel file. Takes the file path, removes the all files header, subtracts the csv portion and adds on the xlsx
        #print(str(fileName))
        path = str(fileName[:-3] + "xlsx")
        workbook = openpyxl.load_workbook(path)
        sheet = workbook.active

        # Sets the number of rows and columns to the max rows and columns of the excel sheet entered
        self.table_widget. setRowCount(sheet.max_row - 1)
        self.table_widget.setColumnCount(sheet.max_column)

        # Sets the headers of the widget table to the headers in the excel sheet entered
        list_values = list(sheet.values)
        self.table_widget.setHorizontalHeaderLabels(list_values[0])

        # Gives a success message
        msg = QMessageBox()
        msg.setWindowTitle("Success")
        msg.setText("Table successfully generated!")
        msg.setIcon(QMessageBox.Information)
        x = msg.exec_()

        # Adds all other elements (value_tuple) of the excel file, skipping the header (starting at column 1 -> # of columns left)
        row_index = 0
        for value_tuple in list_values[1:]:
            col_index = 0
            for value in value_tuple:
                self.table_widget.setColumnWidth(col_index, 200)                
                self.table_widget.setItem(row_index, col_index, QTableWidgetItem(str(value))) 

                # Sets a whole row to red if there is contamination
                if str(value) == "True":
                    self.table_widget.item(row_index, col_index).setBackground(QtGui.QColor(255,114,118))    

                col_index += 1                   
                                            
            row_index += 1
        

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
