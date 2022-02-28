/*
 *ЛАБОРАТОРНЫЕ ВЕСЫ ДЛЯ ПРОВЕДЕНИЯ ИЗМЕРЕНИЙ В УСЛОВИЯХ МОРСКОЙ КАЧКИ
 *Версия 1.5_alpha
 *Авторы проекта: Белов Андрей, Грищенко Анна, Ибрагимов Далгат
 *Руководитель: Борисов Дмитрий Геннадьевич
 *ГБОУ Школа №2065
 *Институт океанологии им. П.П. Ширшова РАН
 *2021-03
*/
//Подключение библиотек
#include <Wire.h>                                         // библиотека для работы через интерфейс I2C
#include <SPI.h>                                          // библиотека для работы через интерфейс SPI
#include <AltSoftSerial.h>                                // библиотека через программный серийный/последовательны порт (UART) на пинах 8 и 9
#include <EEPROM.h>                                       // библиотека для записи и чтения из энергонезависимой памяти arduino
#include <LiquidCrystal_I2C.h>                            // библиотека для работы с ЖК-дисплеем через I2C
#include <SD.h>                                           // библиотека для работы с модулем для чтения/записи SD-карт
#include <HX711.h>                                        // библиотека для работы с АЦП HX711
#include <TroykaRTC.h>                                    // библиотека для работы с модулем реального времени


//Макроопределения


#define LED_GREEN_PIN 9                                   // пин для подключения зеленого светодиода
#define HX1_DT_PIN A1                                     // пин Arduino, с которым соединен пин DT/DO на первом модуле весов
#define HX1_SCK_PIN A0                                    // пин Arduino, с которым соединен пин SCK/CK на первом модуле весов
#define HX2_DT_PIN A3                                     // пин Arduino, с которым соединен пин DT на втором модуле весов
#define HX2_SCK_PIN A2                                    // пин Arduino, с которым соединен пин SCK на втором модуле весов
#define SD_CS_PIN 10                                      // Номер пина к которому подключен пин CS модуля чтения/записи SD-карт

//Создание объектов
LiquidCrystal_I2C lcd(0x27, 20, 4);                       // объект для управления ЖК-экраном с адресом 0x38, 16 колонками и 2 строками
RTC clock;                                                // объект для управления работой модуля реального времени
HX711 scale1;                                             // объект для управления первым модулем весов
HX711 scale2;                                             // объект для управления вторым модулем весов
AltSoftSerial altSerial;                                  // объект для работы с программным серийным портом на пинах Arduino 9(TX) и 8 (RX)

//Переменные
char time_arr[12];                                        // массив для хранения текущего времени
char date[12];                                            // массив для хранения текущей даты
char weekDay[12];
String sample_index = "000";

unsigned int counter = 0;

float weight_calib = 0.00;                                // переменная для хранения окончательного результата взвешивания калибровочного груза
float weight_sample = 0.00;                               // переменная для хранения окончательной массы образца
float fin_weight_sample = 00.00;                   


float temp_w_calib = 0.00;                                // переменная для временного хранения результата взвешивания с калибровочного датчика
float sum_calib[20];                                      // массив для хранения всех результатов взвешивания с основного датчика при сортирвоке
float temp_w_sample = 0.00;                               // переменная для временного хранения результата с калибровочного датчика при сортирвоке
float sum_sample[20];                                     // массив для хранения всех результатов взвешивания с основного датчика при сортирвоке
float temp;                                               // переменная для временного хранения при сортировке
float w_calib[3];                                         // массив для хранения медианных значений каждого веса калибровочного груза
float w_sample[3];                                        // массив для хранения медианных значений каждого веса для 
byte gramm = 0;                                           // переменная для вывода значения в граммах при калибровке

float calibration_coefficient_calib = 0;
float calibration_coefficient_sample = 0 ;

String command;

byte sdChar[8] = 
{0b01111,
 0b11111,
 0b11001,
 0b10001,
 0b10001,
 0b10001,
 0b11111,
 0b00000};
byte serialChar[8] = 
{0b00100,
 0b01110,
 0b11111,
 0b00100,
 0b00100,
 0b11111,
 0b01110,
 0b00100};

void setup() {

  counter = EEPROM.read(0);
  
  calibration_coefficient_calib =  EEPROM.read((sizeof(unsigned int)));
  calibration_coefficient_sample = EEPROM.read((sizeof(unsigned int) + sizeof(float)));
  w_calib[0] = EEPROM.read((sizeof(unsigned int) + sizeof(float) + sizeof(float)));
  w_sample[0] = EEPROM.read((sizeof(unsigned int) + sizeof(float) + sizeof(float) + sizeof(float)));
  
  Serial.begin(9600);                                     // создаем соединение с ПК через серийный порт на скорости 9600 бод
  altSerial.begin(9600);                                  // создаем соединение со сканером штрих-кода через серийный порт на скорости 9600 бод
  if (Serial){
   Serial.println(F("Serial port is ready"));
  } 
  clock.begin();                                          // начинаем работу с объектом модуля реального времени
  //clock.set(11,38,18,15,3,2021,MONDAY);                                //устанавливаем на часах дату и время в соответствии с данными ПК на момент компиляции
  lcd.init();                                             // начинаем работу с ЖК-дисплеем
  lcd.backlight();                                        // включаем подсветку ЖК-дисплея
  lcd.setCursor(0, 0);                                    // устанавливаем на ЖК-дисплее курсор в колонку 0, строку 0
  lcd.createChar(0, sdChar);
  lcd.createChar(1, serialChar);
  scale1.begin(HX1_DT_PIN, HX1_SCK_PIN);
  scale2.begin(HX2_DT_PIN, HX2_SCK_PIN);
  scale1.set_scale();                                     // запуск первого модуля весов
  scale2.set_scale();                                     // запуск второго модуля весов
  SD.begin(SD_CS_PIN);
  if (SD.begin(SD_CS_PIN)) {
    Serial.println(F("Card initialized."));               // если всё в порядке выводим сообщение, что карта инициализирована
  }
  else {
    Serial.println(F("Card failed, or not present"));     // если нет, то выводим сообщение об ошибке             
  }
 
  pinMode(4, INPUT_PULLUP);
  pinMode(3, INPUT_PULLUP);
  pinMode(2, INPUT_PULLUP);
  pinMode(LED_GREEN_PIN, OUTPUT);
  displayview();
}

void loop() {
  if (Serial.available()>0) {
   command = String(Serial.readString());
  }
   if (command == "m"){
    measure();
   }
   if (command == "c"){
    calib();
   }
   if (command == "s"){
    save();
   }
   if (command == "sc"){
    altSerial.write(static_cast<byte>(0x7E));
    altSerial.write(static_cast<byte>(0x00));
    altSerial.write(static_cast<byte>(0x08));
    altSerial.write(static_cast<byte>(0x01));
    altSerial.write(static_cast<byte>(0x00));
    altSerial.write(static_cast<byte>(0x02));
    altSerial.write(static_cast<byte>(0x01));
    altSerial.write(static_cast<byte>(0xAB));
    altSerial.write(static_cast<byte>(0xCD));
    command = "0"; 
    while (altSerial.available() == 0){
      }
    byte buffer[7];
    altSerial.readBytes(buffer, 7);   
  }
  if (digitalRead(2) == 0){
    calib();
  }
  if (digitalRead(3) == 0){
    measure();
  }
  if (digitalRead(4) == 0){
    save();
  }
  if (altSerial.available()>0) {
      sample_index = altSerial.readString();
      // Serial.println(sample_index);
      displayview();
   }
}
void save(){
  lcd.setCursor(0, 2); 
  lcd.print(F("Save?"));
  lcd.setCursor(0, 3);   
  lcd.print(F("Press again"));
  delay(500);
  while (digitalRead(4) != 0){
    if (Serial.available()>0){
      command = String(Serial.readString());
      if (command == "s1") {
        break;
      } else {
        lcd.clear();
        displayview();
        lcd.setCursor(0, 2);
        return;
      }
    }
    if ((digitalRead(2) == 0)||(digitalRead(3) == 0)){
      return;
    }
  }
  if (SD.begin(SD_CS_PIN)) {
    String info;
    counter = EEPROM.read(0);                            // считываем данные из ячейку EEPROM с адресом, записанным в переменной addr, и записываем результат в counter
    counter += 1;
    EEPROM.put(0, counter);                            // записываем значение счетчика кол-ва сохраненных измерений в ячейку EEPROM с адресом addr
    clock.read();                                           // запрашиваем данные с часов
    clock.getTimeStamp(time_arr, date, weekDay);            // сохраняем текущее время, дату и день недели в массивы объявленные выше 
    Serial.println(F("Card initialized."));               // если всё в порядке выводим сообщение, что карта инициализирована
    info = String(time_arr) + " " + String(date) + " " + sample_index + " " + String(fin_weight_sample);
    File savefile = SD.open("savefile.txt", FILE_WRITE);
    if (savefile) {
      savefile.println(info);
      savefile.close();
      Serial.println(F("Data Saved"));                         // выводим сообщение об удачной записи
    } else {
        Serial.println(F("Error opening savefile.txt"));          // если файл не доступен, выводим сообщение об ошибке
    }
  } else {
      Serial.println(F("Card failed, or not present"));     // если нет, то выводим сообщение об ошибке
  }
  lcd.clear();
  displayview();
  delay(500);
}
void measure(){
  delay(500);
  for(int i = 0; i < 20; i++){                            //Цикл по итогу которого мы получаем два массива заполненных результатами, полученными с тензодатчиков
    temp_w_calib = scale1.read();
    temp_w_sample = scale2.read();
    sum_calib[i] = temp_w_calib;
    sum_sample[i] = temp_w_sample;
  }
  for (int j = 0; j + 1 < 20; ++j) {                      //Цикл в котором собствено и просиходит пузырьковая сортировка
    for (int i = 0; i + 1 < 20 - j; ++i) {
      if ( sum_calib[i] > sum_calib[i + 1]) {
        temp = sum_calib[i];
        sum_calib[i] = sum_calib[i + 1];
        sum_calib[i + 1] = temp;
      }
      if ( sum_sample[i] > sum_sample[i + 1]) {
        temp = sum_sample[i];
        sum_sample[i] = sum_sample[i + 1];
        sum_sample[i + 1] = temp;
      }
    }
  }

  weight_sample = sum_sample[10];
  weight_calib = sum_calib[10];
  weight_sample = (weight_sample * (20 * calibration_coefficient_calib + w_calib[0]))/weight_calib;
  fin_weight_sample = (weight_sample - w_sample[0])/calibration_coefficient_sample;
  Serial.println(counter);
  Serial.println(sample_index);
  Serial.println(fin_weight_sample);
  lcd.clear();
  displayview();
}
void calib(){                                             //Функция для калибровки модуля весов 
  lcd.setCursor(0, 2); 
  lcd.print(F("Start CALIB.?"));
  lcd.setCursor(0, 3); 
  lcd.print(F("Yes(C) No(S)"));
  delay(500);
  while (digitalRead(2) != 0){
    if (Serial.available()>0){
      command = String(Serial.readString());
      if (command == "c1") {
        break;
      } else {
        lcd.clear();
        displayview();
        lcd.setCursor(0, 2);
        return;
      }
     }
    if ((digitalRead(3) == 0 ) || (digitalRead(4) == 0)){
      lcd.clear();
      displayview();
      lcd.setCursor(0, 2);
      return;
    }
  }
  lcd.clear();
  displayview();
  gramm = 0;
  for (int k = 0; k < 3; k++){
    lcd.setCursor(0, 2); 
    lcd.print("Calib: " + String(gramm));
    lcd.setCursor(0, 3);   
    lcd.print(F("Press again"));
    delay(500);
    while (digitalRead(2) != 0){
      if (Serial.available()>0){
        command = String(Serial.readString());
        if (command == "c2") {
          break;
        } else {
          lcd.clear();
          displayview();
          lcd.setCursor(0, 2);
          return;
        }
      }
      if ((digitalRead(3) == 0 ) || (digitalRead(4) == 0)){
        lcd.clear();
        displayview();
        lcd.setCursor(0, 2);
        return;
      }
    }
    for(int i = 0; i < 9; i++){                            //Цикл по итогу которого мы получаем два массива заполненных результатами, полученными с тензодатчиков
      temp_w_calib = scale1.read();
      temp_w_sample = scale2.read();
      sum_calib[i] = temp_w_calib;
      sum_sample[i] = temp_w_sample;
    }
    for (int j = 0; j + 1 < 9; ++j) {                      //Цикл в котором собствено и просиходит пузырьковая сортировка
      for (int i = 0; i + 1 < 9 - j; ++i) {
        if ( sum_calib[i] > sum_calib[i + 1]) {
          temp = sum_calib[i];
          sum_calib[i] = sum_calib[i + 1];
          sum_calib[i + 1] = temp;
        }
        if ( sum_sample[i] > sum_sample[i + 1]) {
          temp = sum_sample[i];
          sum_sample[i] = sum_sample[i + 1];
          sum_sample[i + 1] = temp;
        }
      }
    }
    w_sample[k] = sum_sample[5];
    w_calib[k] = sum_calib[5];
    gramm+=20;
  }
  lcd.clear();
  displayview();
  calibration_coefficient_sample = ((w_sample[1] - w_sample[0] ) / 20 + ( w_sample[2] - w_sample[0])/40) / 2;
  calibration_coefficient_calib = (( w_calib[1] - w_calib[0]) /20 + (w_calib[2] - w_calib[0] )/40) / 2;
  lcd.setCursor(0, 2); 
  lcd.print(F("Calib"));
  lcd.setCursor(0, 3);   
  lcd.print(F("Succesful"));
  Serial.println(calibration_coefficient_sample);
  Serial.println(calibration_coefficient_calib);
  Serial.println(w_calib[0]);
  Serial.println(w_sample[0]);
  EEPROM.put((sizeof(unsigned int)), calibration_coefficient_calib);
  EEPROM.put((sizeof(unsigned int) + sizeof(float)), calibration_coefficient_sample);
  EEPROM.put((sizeof(unsigned int) + sizeof(float) + sizeof(float)), w_calib[0]);
  EEPROM.put((sizeof(unsigned int) + sizeof(float) + sizeof(float) + sizeof(float)), w_sample[0]);
  delay(500);
  gramm = 0;
  lcd.clear();
  displayview();
}
 void displayview(){
  lcd.setCursor(0,0);
  lcd.print(counter);
  lcd.setCursor(8,0);
  lcd.print("READY");
  lcd.setCursor(18,0); 
  if(Serial){
    lcd.write((uint8_t)1);
  }
  lcd.setCursor(19,0); 
  if(SD.begin(SD_CS_PIN)){
   lcd.write((uint8_t)0);
  }
  lcd.setCursor(0,1);
  lcd.print("S");
  lcd.print(sample_index);
  lcd.setCursor(8,1);
  lcd.print(F("W="));
  lcd.setCursor(10,1);
  lcd.print(String(fin_weight_sample));
  lcd.setCursor(15,1);
  lcd.print(F("g"));
  lcd.setCursor(0,3);
 }
