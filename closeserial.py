import serial

ports = ['COM3', 'COM4']
baud = 9600
for port in ports:
    ser = serial.Serial(port, baud, timeout=1)
    ser.close()
    print(f"Closed serial port: {port}")