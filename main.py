import serial
import datetime
import time


def calib_import(a, b, c, d):  # импорт настроек калибрации в весы
    ser.write(a.encode())
    ser.write(b.encode())
    ser.write(c.encode())
    ser.write(d.encode())
    return


def log_write(text):  # запись в лог
    log = open("log.txt", "a", encoding='utf8')  # открытие/создание лога
    log.write(text + "\n")
    log.close()
    return


def scan():  # сканирование штрих кода
    return


def calib():  # калибровка   status: Калибровка в процессе...
    calib_button_press = True  # плейсхолдер нажатия на кнопку в приложении
    time.sleep(1)
    ser.write("c".encode())
    if calib_button_press:  # имитация нажатия кнопки
        time.sleep(1)
        ser.write("c1".encode())
        for i in range(0, 4):
            if calib_button_press:  # нажатие кнопки еще раз
                time.sleep(1)
                ser.write("c2".encode())
            else:  # выход из калибровки при нажатии другой кнопки
                ser.write("0".encode())
                return
    else:  # выход из калибровки при нажатии другой кнопки
        ser.write("0".encode())
        return
    a = ser.readline().strip().decode()  # получаем 4 строки данных для записи в лог: calibration_coefficient_sample,
    b = ser.readline().strip().decode()  # calibration_coefficient_calib, w_calib[0] и w_sample[0]
    c = ser.readline().strip().decode()
    d = ser.readline().strip().decode()
    print("Калибровка прошла успешно")
    log_write(greenwich_time + " " + a + " " + b + " " + c + " " + d)  # запись в лог
    return


def s():  # сохранение   status: Сохранение в процессе...
    if not card:
        print("Отсутствует карта")
        return
    save_button_press = True
    time.sleep(1)
    ser.write("s".encode())
    if save_button_press:  # имитация нажатия кнопки
        time.sleep(1)
        ser.write("s1".encode())
        print("Успешно сохранено")
    else:  # выход из сохранения при нажатии другой кнопки
        ser.write("0".encode())
        return
    return


def measure():  # измерение
    measure_button_press = True
    time.sleep(1)
    ser.write("m".encode())
    if measure_button_press:  # имитация нажатия кнопки
        time.sleep(1)
        ser.write("m1".encode())
    else:  # выход из измерения при нажатии другой кнопки
        ser.write("0".encode())
        return
    weight = ser.readline().strip().decode()
    log_write(greenwich_time + " " + weight)
    print("Вес = " + weight)
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


ser = serial.Serial(port_search()[0])  # открытие порта
greenwich_time = str(datetime.datetime.utcnow())[:19]  # время по гринвичу
print(ser.readline().strip().decode())
if print(ser.readline().strip().decode()) == "Card initialized.":  # проверка наличия sd карты
    card = True
else:
    card = False

measure()
measure()

ser.close()  # закрытие порта
