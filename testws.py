import socketio

# Ganti URL sesuai alamat server websocket Anda
sio = socketio.Client()

@sio.event
def connect():
    print("Terhubung ke server websocket")

@sio.event
def disconnect():
    print("Terputus dari server websocket")

@sio.on('message')
def on_message(data):
    print("Pesan dari server:", data)

@sio.on('serial_data')
def on_serial_data(data):
    print("Serial data:", data)

if __name__ == '__main__':
    sio.connect('http://localhost:5000')  # Ganti jika server di IP lain
    sio.wait()