import serial

ser = serial.Serial('COM1', baudrate=9600, timeout=1)


while True:
    data = ser.readline()
    ser.write(b'dfvfdv\n')
    print(str(data), end='')