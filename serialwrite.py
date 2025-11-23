import serial

port = 'COM4'  # Ganti dengan port serial yang sesuai
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=1)
def write_serial_data(data):
    if ser.is_open:
        ser.write(data.encode('utf-8'))
        print(f"Sent: {data}")
    else:
        print("Serial port is not open.")

if __name__ == '__main__':
    try:
        while True:
            user_input = input("Enter data to send (or 'exit' to quit): ")
            if user_input.lower() == 'exit':
                break
            write_serial_data(user_input)
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()