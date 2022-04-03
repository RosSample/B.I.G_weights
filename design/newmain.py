import sys
import serial
import datetime
import time
import numpy as np
# from threading import Thread
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QIcon

from design import Ui_Weights  # импорт нашего сгенерированного файла
from adddesign import Ui_DialogAdditionally as Add


def gtime():
    return '[' + str(datetime.datetime.utcnow())[:19] + ']'


# def median_loop():
#     r = np.array([])
#     for i in range(20):
#         time.sleep(1)
#         ser.write("m".encode())
#         counter = ser.readline().strip().decode()
#         sample_index = ser.readline().strip().decode()
#         weight = ser.readline().strip().decode()  # вид строки: счетчик, индекс образца, дата, время, вес
#         r = np.append(r, float(weight))
#     return r


def log_write(text):  # запись в лог
    log = open("log.txt", "a", encoding='utf8')  # открытие/создание лога
    log.write(text + "\n")
    log.close()
    return


def port_search():  # поиск портов
    ports = ['COM%s' % (i + 1) for i in range(256)]

    result = []
    for port in ports:
        try:
            se = serial.Serial(port)
            se.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()

        self.saveButtonClickedCount = 0
        self.calibButtonClickedCount = 0
        self.scanButtonClickedCount = 0
        self.portConnected = False

        self.ui = Ui_Weights()
        self.ui.setupUi(self)
        self.setWindowTitle('Весы')  # название программы
        self.setWindowIcon(QIcon('./images/icon.png'))  # иконка программы

        self.show()
        self.ui.cleanButton.clicked.connect(self.text_clear)
        self.ui.weighButton.clicked.connect(self.measure)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.scanButton.clicked.connect(self.scan)
        self.ui.calibButton.clicked.connect(self.calib)
        self.ui.connectButton.clicked.connect(self.port_add)
        self.ui.disconnectButton.clicked.connect(self.port_disconnect)

        self.ui.selectionWindow.activated.connect(self.port_connect)
        self.ui.settingsButton.clicked.connect(self.settings_clicked)

    def settings_clicked(self):
        dialog = QtWidgets.QDialog()
        dialog.ui = Add()
        dialog.ui.setupUi(dialog)
        dialog.exec_()


    def text_clear(self):
        self.ui.textShow.setText("")
        return

    def add_text(self, text):
        self.ui.textShow.setText(self.ui.textShow.text() + text + "\n")
        self.ui.scrollArea.verticalScrollBar().setValue(self.ui.scrollArea.verticalScrollBar().maximum())
        return

    def measure(self):
        if not self.portConnected:
            self.add_text(gtime() + " Отсутствует подключение к порту.")
            return

        self.add_text(gtime() + " Измерение...")
        self.ui.label.setText("измерение")
        counter = ''
        sample_index = ''

        log_write(
            "[" + counter + " " + sample_index + " " + gtime()[1:] + " " + str(round(np.median(r)+0.2, 2)))
        self.add_text(
            "[" + counter + " " + sample_index + " " + gtime()[1:] + " Вес = " + str(round(np.median(r)+0.2, 2)))
        self.ui.label.setText("работает")
        time.sleep(1)
        return

    def save(self):  # сохранение  status: Сохранение...
        if not self.portConnected:
            self.add_text(gtime() + " Отсутствует подключение к порту.")
            return

        if self.calibButtonClickedCount == 1:  # Отмена калибровки
            self.calibButtonClickedCount = 0
            self.add_text(gtime() + " Калибровка отменена.")
            self.ui.label.setText("работает")
            return

        if self.saveButtonClickedCount == 0:
            time.sleep(1)
            ser.write("s".encode())
            self.add_text(gtime() + " Сохранение...")
            self.ui.label.setText("сохранение")
            self.add_text(gtime() + " Нажмите сохранить чтобы продолжить.")
            self.saveButtonClickedCount += 1
            return
        self.saveButtonClickedCount = 0

        time.sleep(1)
        ser.write("s1".encode())
        if ser.readline().strip().decode() == "Data Saved":
            self.add_text(gtime() + " Успешно сохранено.")
        else:
            self.add_text(gtime() + " Отсутствует SD карта или\n ошибка при чтении файла.")

        self.ui.label.setText("работает")
        time.sleep(1)
        return

    def calib(self):  # калибровка  status: Калибровка...
        if not self.portConnected:
            self.add_text(gtime() + " Отсутствует подключение к порту.")
            return

        if self.calibButtonClickedCount == 0:
            time.sleep(1)
            ser.write("c".encode())
            self.add_text(gtime() + " Начать калибровку?")
            self.add_text(gtime() + " Для продолжения нажмите калибровать.")
            self.add_text(gtime() + " Для отмены нажмите сохранить.")
            self.calibButtonClickedCount += 1
            self.ui.label.setText("калибровка")
            return

        if self.calibButtonClickedCount == 1:
            time.sleep(1)
            ser.write("c1".encode())
            self.add_text(gtime() + " Калибровка: 0.")
            self.add_text(gtime() + " Нажмите калибровать еще раз.")
            self.calibButtonClickedCount += 1
            return

        if self.calibButtonClickedCount == 2:
            time.sleep(1)
            ser.write("c2".encode())
            self.add_text(gtime() + " Калибровка: 20.")
            self.add_text(gtime() + " Нажмите калибровать еще раз.")
            self.calibButtonClickedCount += 1
            return

        if self.calibButtonClickedCount == 3:
            time.sleep(1)
            ser.write("c2".encode())
            self.add_text(gtime() + " Калибровка: 40.")
            self.add_text(gtime() + " Нажмите калибровать еще раз.")
            self.calibButtonClickedCount += 1
            return

        if self.calibButtonClickedCount == 4:
            time.sleep(1)
            ser.write("c2".encode())
            self.add_text(gtime() + " Калибровка прошла успешна")
            self.calibButtonClickedCount = 0

        a = ser.readline().strip().decode()  # получаем 4 строки данных для записи в лог: calibration_coefficient_sample
        b = ser.readline().strip().decode()  # calibration_coefficient_calib, w_calib[0] и w_sample[0]
        c = ser.readline().strip().decode()
        d = ser.readline().strip().decode()
        calib_settings = open("calib.txt", "w", encoding='utf8')  # открытие/создание настроек калибровки
        calib_settings.write(a + " " + b + " " + c + " " + d)  # сохранение настроек калибровки в файл
        calib_settings.close()
        log_write(gtime() + " " + a + " " + b + " " + c + " " + d)  # запись настроек в лог
        self.ui.label.setText("работает")
        time.sleep(1)
        return

    def scan(self):  # сканирование штрих кода в течении 5 секунд
        if not self.portConnected:
            self.add_text(gtime() + " Отсутствует подключение к порту.")
            return

        self.add_text(gtime() + " Сканирование прошло успешно.")
        ser.write("sc".encode())
        time.sleep(5)
        return

    def port_connect(self):
        self.portConnected = True
        port = self.sender().currentText()
        self.add_text(gtime() + " Подключение к: " + port)
        global ser
        ser = serial.Serial(port)
        self.add_text(gtime() + " " +
                      ser.readline().strip().decode())  # чтение первой строки из serial порта
        self.add_text(gtime() + " " +
                      ser.readline().strip().decode())  # чтение второй строки из serial порта
        return

    def port_disconnect(self):
        if not self.portConnected:
            self.add_text(gtime() + " Невозможно отключиться от порта,\nподключение отсутствует.")
            return

        self.portConnected = False
        ser.close()
        self.add_text(gtime() + " Порт успешно закрыт.")
        return

    def port_add(self):
        self.ui.selectionWindow.clear()
        ports = port_search()
        self.ui.selectionWindow.addItems(ports)
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = MyWindow()
    application.show()

    sys.exit(app.exec())
