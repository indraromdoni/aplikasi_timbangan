import serial
import random
import time

port = 'COM2'  # Ganti dengan port serial yang sesuai
baudrate = 9600
ser = serial.Serial(port, baudrate, timeout=1)

def generate_weight_string():
    # Generate berat antara -50 sampai +150 (boleh disesuaikan)
    weight = random.uniform(-50, 150)
    
    # Format dengan tanda + atau -, dan 5 digit + 1 desimal
    formatted = f"{weight:+08.1f}"        # contoh: +00155.5 atau -00012.7

    # Status acak: NT (net) atau ST (stable)
    status = random.choice(["NT", "ST"])

    # Format final seperti timbangan
    return f"US,{status},{formatted}Kg\r\n"

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
            #random_weight = round(random.uniform(0.0, 100.0), 2)
            random_weight = generate_weight_string()
            write_serial_data(random_weight)
            print(f"Simulated weight sent: {random_weight} kg")
            time.sleep(1)  # prevent flooding the serial port
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()