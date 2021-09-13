import serial
import sys
from PyQt5 import uic  # Импортируем uic
from PyQt5.QtWidgets import QApplication, QMainWindow


"""
class MyWidget(QMainWindow):  # загрузка дизайна
    def __init__(self):
        super().__init__()
        uic.loadUi('main1.ui', self)  # Загружаем дизайн
        self.pushButton.clicked.connect(self.run)  # Обратите внимание: имя элемента такое же как в QTDesigner

    def run(self):
        self.label.setText("OK")
        # Имя элемента совпадает с objectName в QTDesigner


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
"""


def scan():
    return


def calib():
    return


def save():
    return


def measure():
    ser.write("measure".encode())
    ser.readline()
    ser.readline()
    ser.write("measure1".encode())
    return ser.readline()


ports = ['COM%s' % (i + 1) for i in range(256)]

result = []
for port in ports:
    try:
        s = serial.Serial(port)
        s.close()
        result.append(port)
    except (OSError, serial.SerialException):
        pass
ser = serial.Serial(result[0])  # open serial port
print(ser.readline())
print(ser.readline())
input()
print(measure())
input()
ser.close()             # close port
