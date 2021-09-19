import serial
import datetime


def log_write(text):  # запись в лог
    log = open("log.txt", "a", encoding='utf8')  # открытие/создание лога
    log.write(text + "\n")
    log.close()
    return


def scan():  # сканирование штрихкода
    return


def calib():  # калибровка
    calib_button_press = True  # плейсхолдер нажатия на кнопку в приложении
    ser.write("calib".encode())
    if calib_button_press:  # нажатие кнопки
        ser.write("calib1".encode())
        if calib_button_press:  # нажатие кнопки еще раз
            ser.write("calib2".encode())
        else:  # выход из калибровки при нажатии другой кнопки
            ser.write("not calib2".encode())
            return
    else:  # выход из калибровки при нажатии другой кнопки
        ser.write("not calib1".encode())
        return
    a = ser.readline(10)  # получаем 4 строки данных для записи в лог: calibration_coefficient_sample,
    b = ser.readline(10)  # calibration_coefficient_calib, w_calib[0] и w_sample[0]
    c = ser.readline(10)
    d = ser.readline(10)
    log_write((a, b, c, d))  # запись в лог    note to self: сделать парсировку строк
    return "Калибровка прошла успешно"


def save():  # сохранение
    return


def measure():  # измерение
    measure_button_press = True  # плейсхолдер нажатия на кнопку в приложении
    ser.write("measure".encode())
    if measure_button_press:  # нажатие кнопки
        ser.write("measure1".encode())
    else:  # выход из измерения при нажатии другой кнопки
        ser.write("not measure1".encode())
        return
    weight = ser.readline(10)
    log_write(weight)
    return "Вес = " + weight


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
log_write("найди работу")
log_write("найди работу")
greenwich_time = str(datetime.datetime.utcnow())
print(greenwich_time[:19])
# print(ser.readline())
# print(ser.readline())
# input()
# print(measure())
# input()
# ser.close()  # закрытие порта
