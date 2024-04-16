import sys
from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import QFileDialog
from GUI import Ui_MainWindow
from model import model
import time
class MainWindow(qtw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.Browse.clicked.connect(self.browsefiles)
        self.ui.start.clicked.connect(self.start)
    def browsefiles(self):
        fname, _ = QFileDialog.getOpenFileName(self, "Open File", filter="gcode (*.gcode)")
        if fname:
            with open(fname, "r") as f:
                content = f.read()
                self.ui.textEdit.setText(content)
        self.ui.lineEdit.setText(fname)
    def start(self):
        start = time.time()
        model(self.ui.lineEdit.text())
        end = time.time()
        print(end - start)
def app():
    app = qtw.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
app()