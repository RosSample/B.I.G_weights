import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from design import Ui_Weights  # импорт нашего сгенерированного файла


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_Weights()
        self.ui.setupUi(self)
        self.setWindowTitle('Весы')     # название программы
        self.setWindowIcon(QIcon('./images/icon.png'))      # иконка программы

        self.show()
        self.ui.saveButton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        print('button clicked!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = mywindow()
    application.show()

    sys.exit(app.exec())
