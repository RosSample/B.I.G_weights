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


def log_write(text):  # запись в лог
    log.write(text + "\n")
    return


def scan():  # сканирование штрихкода
    return


def calib():  # калибровка
    ser.write("calib".encode())
    ser.write("calib1".encode())
    ser.write("calib1".encode())
    a = ser.readline()
    b = ser.readline()
    c = ser.readline()
    d = ser.readline()
    log_write(a + b + c + d)
    return


def save():  # сохранение
    return


def measure():  # измерение
    ser.write("measure".encode())
    ser.readline()
    ser.write("measure1".encode())
    log_write(ser.readline())
    return ser.readline()


def port_search():  # поиск портов
    ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


ser = serial.Serial(port_search()[0])  # открытие порта
log = open("log.txt", "a", encoding='utf8')  # открытие/создание лога
log_write("найди работу")
log_write("найди работу")
# print(ser.readline())
# print(ser.readline())
# input()
# print(measure())
# input()
# ser.close()  # закрытие порта
log.close()  # закрытие лога
