import sys
import time
from PyQt5.QtWidgets import QApplication, QWidget, QProgressBar, QPushButton, QVBoxLayout


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(600)
        self.setWindowTitle('QProgress Bar Example')

        layout = QVBoxLayout()

        n = 50

        self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(n)
        layout.addWidget(self.progressBar)

        # self.progressBar.setRange(0, n)

        self.button = QPushButton('Go')
        self.button.setStyleSheet('font-size: 30px; height: 30px;')
        self.button.clicked.connect(lambda status, n_size=n: self.run(n_size))
    
        layout.addWidget(self.button)       
        self.setLayout(layout)

    def run(self, n):
        for i in range(n):
            time.sleep(0.05)
            self.progressBar.setValue(i+1)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    demo = AppDemo()
    demo.show()

    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Closing Window...')