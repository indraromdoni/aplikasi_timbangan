import serial
import socketio

port = 'COM3'  # Replace with your serial port
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=1)
def read_serial_data():
    if ser.is_open:
        line = ser.readline().decode('utf-8').rstrip()
        return line
    else:
        return None
    
if __name__ == '__main__':
    try:
        while True:
            data = read_serial_data()
            if data:
                print(f"Received: {data}")
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()