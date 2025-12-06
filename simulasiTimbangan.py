import serial
import random
import time

port = 'COM2'  # Ganti dengan port serial yang sesuai
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=1)
def write_serial_data(data):
    if ser.is_open:
        data_str = f"{data}\n"  # convert to string and add newline
        ser.write(data_str.encode('utf-8'))
        print(f"Sent: {data_str.strip()}")
    else:
        print("Serial port is not open.")

if __name__ == '__main__':
    try:
        while True:
            random_weight = round(random.uniform(0.0, 100.0), 2)
            write_serial_data(random_weight)
            print(f"Simulated weight sent: {random_weight} kg")
            time.sleep(1)  # prevent flooding the serial port
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()