from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QFileDialog, QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox, QCheckBox, QComboBox
import sys, openpyxl, csv, subprocess, os, pathlib, psutil, glob

class UI(QMainWindow):

    def __init__(self):
        super(UI, self).__init__()
        self.test_out=str()

        # Load the ui file
        uic.loadUi("MainMenu.ui", self)

        # Creates the layout of the box
        layout = QVBoxLayout()   

         # Adding the table widget to our window
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        # Shows the table widget (sorta idk it doesn't quite show)
        self.table_widget.show()

        # Define our widgets
        self.widgetDefiner()

        # Clicks the buttons
        self.analyzeResultsButton.clicked.connect(self.analyzeClicker)
        self.tableDisplayButton.clicked.connect(self.tableClicker)
        #self.advancedOptionsButton.clicked.connect(self.advancedOptionsClicker)

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

            # Checks what options are selected and applies those arguements to our command line
            rmlst = self.rmlstOptions()
            fasta = self.fastaOptions()
            baseCutoff = self.baseCutoffOptions()
            dataChoice = self.dataChoiceOptions()
            keepFiles = self.keepOptions()
            versionDisplay = self.versionOptions()
            crossDetails = self.crossDetailsOptions()
            verbosity = self.verbosityOptions()
            databases = self.databaseOptions()
            tmp = self.TMPOptions()
            baseFraction = self.baseFractionOptions()
            threads = self.threadsOptions()
            qualityCutoff = self.qualityOptions()
            cgmlst = self.CGMLISTOptions()
            forwardId = self.forwardOptions()
            reverseId = self.reverseOptions()
            MMH = self.MMHOptions()


            # Uses the folder name as an argument to run ConFindr and get the results. Mem represents total allocated memory that is being reserved for confindr
            self.test_out = os.path.join(folderName, "test_out")
            mem = int(0.85 * float(psutil.virtual_memory().total) / 1024)
            subprocess.run(f'confindr -i {folderName} -o {self.test_out}{databases}{rmlst}{threads}{tmp}{keepFiles}{qualityCutoff}{baseCutoff}{baseFraction}{forwardId}{reverseId}{versionDisplay}{dataChoice}{cgmlst}{fasta}{verbosity}{crossDetails}{MMH} -Xmx {mem}K', shell=True)
            print(f'confindr -i {folderName} -o {self.test_out}{databases}{rmlst}{threads}{tmp}{keepFiles}{qualityCutoff}{baseCutoff}{baseFraction}{forwardId}{reverseId}{versionDisplay}{dataChoice}{cgmlst}{fasta}{verbosity}{crossDetails}{MMH} -Xmx {mem}K')

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
        if str(fileName) != "('', '')":
            self.test_out = os.path.dirname(fileName[0])

            # Custom methods use to extract data into the GUI
            self.convert_csv_to_xlsx()
            self.load_data(fileName[0])

        else:
            self.errorLabel.setText("Please select a .csv or .xlsx file to continue")

    # Opens a new window with advanced options [NOW DISCOUTINUED AND NOT USED]
    #def advancedOptionsClicker(self):
        #self.window = QtWidgets.QMainWindow()
        #self.ui = Ui_AdvancedWindow()
        #self.ui.setupUi(self.window)
        #self.window.show()

#--------------------File Loader and Graph Displayer------------------------------------------

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

        #--------------------------Widget Definers-------------------------------------------------

    def widgetDefiner(self):
        # Defines all the widgets used [there is a lot of them]
        self.tableDisplayButton = self.findChild(QPushButton, "tableDisplayButton")
        self.analyzeResultsButton = self.findChild(QPushButton, "analyzeResultsButton")
        #self.advancedOptionsButton = self.findChild(QPushButton, "advancedOptionsButton")
        self.folderField = self.findChild(QLineEdit, "folderField")
        self.errorLabel = self.findChild(QLabel, "errorLabel")

        # Main arguments
        self.RMLSTcheckBox = self.findChild(QCheckBox, "RMLSTcheckBox")
        self.FASTAcheckBox = self.findChild(QCheckBox, "FASTAcheckBox")
        self.baseCutoffInput = self.findChild(QLineEdit, "baseCutoffInput")
        self.dataDropdownMenu = self.findChild(QComboBox, "dataDropdownMenu")

        # Advanced arguements
        self.keepCheckBox = self.findChild(QCheckBox, "keepCheckBox")
        self.versionCheckBox = self.findChild(QCheckBox, "versionCheckBox")
        self.crossDetailsCheckBox = self.findChild(QCheckBox, "crossDetailsCheckBox")
        self.verbosityDropdownMenu = self.findChild(QComboBox, "verbosityDropdownMenu")        
        self.databaseInput = self.findChild(QLineEdit, "databaseInput")
        self.TMPInput = self.findChild(QLineEdit, "TMPInput")
        self.baseFractionInput = self.findChild(QLineEdit, "baseFractionInput")
        self.threadsInput = self.findChild(QLineEdit, "threadsInput")
        self.qualityInput = self.findChild(QLineEdit, "qualityInput")
        self.cgmlstInput = self.findChild(QLineEdit, "cgmlstInput")
        self.forwardInput = self.findChild(QLineEdit, "forwardInput")
        self.reverseInput = self.findChild(QLineEdit, "reverseInput")
        self.MMHInput = self.findChild(QLineEdit, "MMHInput")

#---------------------------Argument Functions----------------------------------------------

    # Checks if the rmlst option is selected
    def rmlstOptions(self):
        if self.RMLSTcheckBox.isChecked() == True:
            option = ' --rmlst'
        else:
            option = ''
        return option

    # Checks if the fasta option is selected
    def fastaOptions(self):
        if self.FASTAcheckBox.isChecked() == True:
            option = ' --fasta'
        else:
            option = ''
        return option    

    # Checks if the keep-files option is selected
    def keepOptions(self):
        if self.keepCheckBox.isChecked() == True:
            option = ' -k'
        else:
            option = ''
        return option  

    # Checks if the version option is selected
    def versionOptions(self):
        if self.versionCheckBox.isChecked() == True:
            option = ' -v'
        else:
            option = ''
        return option  

    # Checks if the cross details option is selected
    def crossDetailsOptions(self):
        if self.crossDetailsCheckBox.isChecked() == True:
            option = ' -cross_details'
        else:
            option = ''
        return option  
        
    # Checks first if the input is a number or not. If not, it defaults to 2. If is, then it returns that number
    def baseCutoffOptions(self):
        if (self.baseCutoffInput.text()).isnumeric():
            option = ' -b ' + str(int(self.baseCutoffInput.text()))
        else:
            option = ' -b ' + str(2)
        return option

    # Checks if there is anything written for databaseOptions and if not, return nothing
    def databaseOptions(self):
        if len(self.databaseInput.text()) == 0:
            option = ''
        else:
            option = ' -d ' + self.databaseInput.text()
        return option

    # Checks if anything is written and then returns the TMP input back
    def TMPOptions(self):
        if len(self.TMPInput.text()) == 0:
            option = ''
        else:
            option = ' -tmp ' + self.TMPInput.text()
        return option

    # Checks first if the input is a number or not. If not, it defaults to 0.05
    def baseFractionOptions(self):
        try:
            float(self.baseFractionInput.text())
            option = ' -bf ' + str(float(self.baseFractionInput.text()))
            return option
        except ValueError:
            option = ' -bf ' + str(0.05)
            return option

    # Checks first if the input is a number or not. If not, it returns nothing
    def threadsOptions(self):
        if (self.threadsInput.text()).isnumeric():
            option = ' -t ' + str(int(self.threadsInput.text()))
        else:
            option = ''
        return option

    # Checks first if the input is a number or not. If not, it defaults to 20. 
    def qualityOptions(self):
        if (self.qualityInput.text()).isnumeric():
            option = ' -q ' + str(int(self.qualityInput.text()))
        else:
            option = ' -q ' + str(20)
        return option
    
    # Checks first if there is any input. If not it adds whatever is typed
    def CGMLISTOptions(self):
        if len(self.cgmlstInput.text()) == 0:
            option = ''
        else:
            option = ' -cgmlst ' + self.cgmlstInput.text()
        return option
    
    # Checks first if there is any input. If not it adds whatever is typed
    def forwardOptions(self):
        if len(self.forwardInput.text()) == 0:
            option = ''
        else:
            option = ' -fid ' + self.forwardInput.text()
        return option
    
    # Checks first if there is any input. If not it adds whatever is typed
    def reverseOptions(self):
        if len(self.reverseInput.text()) == 0:
            option = ''
        else:
            option = ' -rid ' + self.reverseInput.text()
        return option

    # Checks first if the input is a number or not. If not, it defaults to 150. 
    def MMHOptions(self):
        if (self.MMHInput.text()).isnumeric():
            option = ' -m ' + str(int(self.MMHInput.text()))
        else:
            option = ' -m ' + str(150)
        return option
    
    # Checks if you chose Illumina or Nanopore as your data type
    def dataChoiceOptions(self):
        if self.dataDropdownMenu.currentText() == 'ILLUMINA':
            option = ' -dt Illumina'
        else:
            option = ' -dt Nanopore'
        return option    

    # Checks if you chose Debug, Info or Warning as the amount of output on your screen
    def verbosityOptions(self):
        if self.verbosityDropdownMenu.currentText() == 'DEBUG':
            option = ' -verbosity debug'
        elif self.verbosityDropdownMenu.currentText() == 'INFO':
            option = ' -verbosity info'
        else:
            option = ' -verbosity warning'
        return option  

app = QApplication(sys.argv)
UIWindow = UI()
app.exec_()
