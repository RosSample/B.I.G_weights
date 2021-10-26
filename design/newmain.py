import sys
import serial
import datetime
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from design import Ui_Weights  # импорт нашего сгенерированного файла


def log_write(text):  # запись в лог
    log = open("log.txt", "a", encoding='utf8')  # открытие/создание лога
    log.write(text + "\n")
    log.close()
    return


def scan():  # сканирование штрих кода в течении 5 секунд
    time.sleep(1)
    ser.write("sc".encode())
    print("[" + greenwich_time + "] Сканирование штрих-кода")
    time.sleep(5)
    return


# def calib():  # калибровка  status: Калибровка...
#     calib_button_press = True  # плейсхолдер нажатия на кнопку в приложении
#     time.sleep(1)
#     ser.write("c".encode())
#     if calib_button_press:  # имитация нажатия кнопки
#         time.sleep(1)
#         ser.write("c1".encode())
#         for i in range(0, 4):
#             time.sleep(1)
#             if calib_button_press:  # нажатие кнопки еще раз
#                 time.sleep(1)
#                 ser.write("c2".encode())
#             else:  # выход из калибровки при нажатии другой кнопки
#                 ser.write("0".encode())
#                 return
#     else:  # выход из калибровки при нажатии другой кнопки
#         ser.write("0".encode())
#         return
#     a = ser.readline().strip().decode()  # получаем 4 строки данных для записи в лог: calibration_coefficient_sample,
#     b = ser.readline().strip().decode()  # calibration_coefficient_calib, w_calib[0] и w_sample[0]
#     c = ser.readline().strip().decode()
#     d = ser.readline().strip().decode()
#     print("[" + greenwich_time + "] Калибровка прошла успешно")
#     calib_settings = open("calib.txt", "w", encoding='utf8')  # открытие/создание настроек калибровки
#     calib_settings.write(a + " " + b + " " + c + " " + d)  # сохранение настроек калибровки в файл
#     calib_settings.close()
#     log_write("[" + greenwich_time + "]" + " " + a + " " + b + " " + c + " " + d)  # запись настроек в лог
#     time.sleep(1)
#     return


# def save():  # сохранение  status: Сохранение...
#     if not card:
#         print("Отсутствует карта")
#         return
#     save_button_press = True
#     time.sleep(1)
#     ser.write("s".encode())
#     if save_button_press:  # имитация нажатия кнопки
#         time.sleep(1)
#         ser.write("s1".encode())
#         print("Успешно сохранено")
#     else:  # выход из сохранения при нажатии другой кнопки
#         ser.write("0".encode())
#         return
#     time.sleep(1)
#     return


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


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()

        self.weighButtonClickedCount = 0
        self.saveButtonClickedCount = 0
        self.calibButtonClickedCount = 0
        self.scanButtonClickedCount = 0

        self.ui = Ui_Weights()
        self.ui.setupUi(self)
        self.setWindowTitle('Весы')  # название программы
        self.setWindowIcon(QIcon('./images/icon.png'))  # иконка программы

        self.show()
        self.ui.weighButton.clicked.connect(self.measure)
        self.ui.saveButton.clicked.connect(self.save)
        self.ui.scanButton.clicked.connect(scan)
        self.ui.calibButton.clicked.connect(self.calib)
        self.ui.connectButton.clicked.connect(self.port_add)
        self.ui.disconnectButton.clicked.connect(self.port_disconnect)

        self.ui.selectionWindow.activated.connect(self.port_connect)

    def addText(self, text):
        self.ui.textShow.setText(self.ui.textShow.text() + text + "\n")

    def measure(self):
        if self.weighButtonClickedCount == 0:
            time.sleep(1)
            ser.write("m".encode())
            greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
            self.addText("[" + greenwich_time + "] Измерение...")
            self.ui.label.setText("Измерение")
            self.addText("[" + greenwich_time + "] Поставьте груз и нажмите еще раз.")
            self.weighButtonClickedCount += 1
            return
        self.weighButtonClickedCount = 0

        time.sleep(1)
        ser.write("m1".encode())
        counter = ser.readline().strip().decode()
        sample_index = ser.readline().strip().decode()
        weight = ser.readline().strip().decode()  # вид строки: счетчик, индекс образца, дата, время, вес
        greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
        log_write(
            "[" + counter + " " + sample_index + " " + greenwich_time + "] " + weight)
        self.addText(
            "[" + counter + " " + sample_index + " " + greenwich_time + "] Вес = " + weight + ".")
        self.ui.label.setText("работает")
        time.sleep(1)
        return

    def save(self):  # сохранение  status: Сохранение...
        if not card:
            greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
            self.addText("[" + greenwich_time + "] Отсустствует карта памяти.")
            return

        if self.saveButtonClickedCount == 0:
            time.sleep(1)
            # ser.write("s".encode())
            greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
            self.addText("[" + greenwich_time + "] Сохранение...")
            self.ui.label.setText("сохранение")
            self.addText("[" + greenwich_time + "] Нажмите взвесить чтобы продолжить.")
            self.saveButtonClickedCount += 1
            return
        self.saveButtonClickedCount = 0

        time.sleep(1)
        ser.write("s1".encode())
        greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
        self.addText("[" + greenwich_time + "] Успешно сохранено.")
        self.ui.label.setText("работает")
        time.sleep(1)
        return

    def calib(self):  # калибровка  status: Калибровка...
        if self.weighButtonClickedCount == 0:
            time.sleep(1)
            ser.write("c".encode())
            greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
            self.addText("[" + greenwich_time + "] Начать калибровку?")
            self.ui.label.setText("Измерение")
            self.addText("[" + greenwich_time + "]" + " Чтобы продолжить нажмите калибровать")
            self.addText("[" + greenwich_time + "]" + " Чтобы продолжить нажмите сохранить")
            self.weighButtonClickedCount += 1
            return

        time.sleep(1)
        ser.write("c".encode())
        if calib_button_press:  # имитация нажатия кнопки
            time.sleep(1)
            ser.write("c1".encode())
            for i in range(0, 4):
                time.sleep(1)
                if calib_button_press:  # нажатие кнопки еще раз
                    time.sleep(1)
                    ser.write("c2".encode())
                else:  # выход из калибровки при нажатии другой кнопки
                    ser.write("0".encode())
                    return
        else:  # выход из калибровки при нажатии другой кнопки
            ser.write("0".encode())
            return
        a = ser.readline().strip().decode()  # получаем 4 строки данных для записи в лог: calibration_coefficient_sample
        b = ser.readline().strip().decode()  # calibration_coefficient_calib, w_calib[0] и w_sample[0]
        c = ser.readline().strip().decode()
        d = ser.readline().strip().decode()
        greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
        self.addText("[" + greenwich_time + "] Калибровка прошла успешно")
        calib_settings = open("calib.txt", "w", encoding='utf8')  # открытие/создание настроек калибровки
        calib_settings.write(a + " " + b + " " + c + " " + d)  # сохранение настроек калибровки в файл
        calib_settings.close()
        log_write("[" + greenwich_time + "]" + " " + a + " " + b + " " + c + " " + d)  # запись настроек в лог
        time.sleep(1)
        return

    def port_connect(self):
        port = self.sender().currentText()
        self.addText(port)
        global ser
        ser = serial.Serial(port)

        global card
        self.addText(ser.readline().strip().decode())  # чтение первой строки из serial порта
        cardln = ser.readline().strip().decode()  # чтение второй строки из serial порта
        self.addText(cardln)
        if cardln == "Card initialized.":  # проверка наличия sd карты
            card = True
        else:
            card = False

    def port_disconnect(self):
        ser.close()

    def port_add(self):
        self.ui.selectionWindow.clear()
        ports = port_search()
        self.ui.selectionWindow.addItems(ports)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    application = mywindow()
    application.show()

    sys.exit(app.exec())
