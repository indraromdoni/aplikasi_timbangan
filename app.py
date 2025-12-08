from flask import Flask, jsonify, render_template, request, session
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from serial.tools import list_ports
import serial
import threading
import json
import psycopg2
import eventlet
import datetime
import uuid
import re

_exit = False
_config = {}

app = Flask(__name__)
sock = SocketIO(app, async_mode='eventlet')
app.secret_key = 'timbangan_secret_key'
_serial_thread = None
_thread_lock = threading.Lock()
data_serial = None

def db_connect():
    global _config
    dbname = _config['db_connection']['database']
    user = _config['db_connection']['user']
    password = _config['db_connection']['password']
    host = _config['db_connection']['host']
    port = _config['db_connection']['port']
    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

def db_query(cmd, values=None):
    conn = db_connect()
    if conn is None:
        print("Database connection failed")
        return
    cur = conn.cursor()
    try:
        if values:
            cur.execute(cmd, values)
        else:
            cur.execute(cmd)
        results = cur.fetchall()
        return results
    except Exception as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        cur.close()
        conn.close()

def load_serial():
    global _config
    port = _config['serial_port']['port']
    baudrate = _config['serial_port']['baudrate']
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        return ser
    except Exception as e:
        print(f'Error com port :', e)
        return None

def list_serial_ports():
    ports = list_ports.comports()
    return [port.device for port in ports]

def parse_weight(text):
    # Regex menangkap: +00123.4, -00012.7, 155.5, -5.0, dll.
    match = re.search(r'([+-]?\d+\.\d+)\s*Kg', text)
    if match:
        return float(match.group(1))
    return None

def read_serial_data(ser):
    if ser.is_open:
        line = ser.readline().decode('utf-8').rstrip()
        return line
    else:
        return None

def load_config():
    global _config
    with open('config.json', 'r') as f:
        _config = json.load(f)
    f.close()

def save_config(config):
    global _config
    _config = config
    with open('config.json', 'w') as f:
        json.dump(_config, f, indent=4)
    f.close()
    load_config()
    restart_serial_thread()

def restart_serial_thread():
    global _exit, _serial_thread, _thread_lock
    with _thread_lock:
        # Hentikan thread lama
        _exit = True
        if _serial_thread and _serial_thread.is_alive():
            _serial_thread.join(timeout=2)
        
        # Buat thread baru dengan config terbaru
        _exit = False
        _serial_thread = threading.Thread(target=thread_serialread, daemon=True)
        _serial_thread.start()
        print("Serial thread restarted with new config")

@app.route('/')
def home():
    user = session.get('username')
    role = session.get('role')
    return render_template('index.html', user=user, role=role)

@app.route('/report')
def report():
    user = session.get('username')
    role = session.get('role')
    return render_template('report.html', user=user, role=role)

@app.route('/data_pengguna')
def operator():
    user = session.get('username')
    role = session.get('role')
    return render_template('formPengguna.html', user=user, role=role)

@app.route('/data_wadah')
def wadah():
    user = session.get('username')
    role = session.get('role')
    return render_template('formWadah.html', user=user, role=role)

@app.route('/data_produk')
def produk():
    user = session.get('username')
    role = session.get('role')
    return render_template('formProduk.html', user=user, role=role)

@app.route('/data_supplier')
def supplier():
    user = session.get('username')
    role = session.get('role')
    return render_template('formSupplier.html', user=user, role=role)

@app.route('/print_data')
def print_data():
    return render_template('printout.html')

@app.route('/config')
def config():
    global _config
    user = session.get('username')
    role = session.get('role')
    return render_template('config.html', user=user, role=role)

@app.route('/api/config', methods=['GET'])
def api_get_config():
    global _config
    _config['list_serial_ports'] = list_serial_ports()
    return jsonify(_config)

@app.route('/api/config', methods=['POST'])
def api_save_config():
    global _config
    #print("before:", _config)
    new_config = request.json
    _config['serial_port']['port'] = new_config['port']
    _config['serial_port']['baudrate'] = new_config['baudrate']
    #print("after:", _config)
    save_config(_config)
    return jsonify({'status': 'success'})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    ret = db_query("SELECT * FROM tbluser WHERE \"user\"=%s AND \"password\"=md5(%s)", (username, password))
    print(data)
    print(ret)
    if ret and len(ret) > 0:
        session['username'] = username
        session['role'] = ret[0][2]
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'failure'}), 401

@app.route('/api/logout', methods=['GET'])
def api_logout():
    session.pop('username', None)
    session.pop('role', None)
    return jsonify({'status': 'success'})

@app.route('/api/wadah', methods=['GET'])
def api_get_wadah():
    results = db_query("SELECT * FROM tblwadah ORDER BY id ASC")
    wadah_list = []
    if results:
        for row in results:
            wadah = {
                'id': row[0],
                'nama_wadah': row[1],
                'berat_kosong': float(row[2])
            }
            wadah_list.append(wadah)
    return jsonify(wadah_list)

@app.route('/api/wadah', methods=['POST'])
def api_add_wadah():
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "INSERT INTO tblwadah (nama, berat) VALUES (%s, %s)"
    values = (data['nama_wadah'], data['berat_kosong'])
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error inserting wadah: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/wadah/<int:wadah_id>', methods=['GET'])
def api_get_wadah_by_id(wadah_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "SELECT * FROM tblwadah WHERE id=%s"
    values = (wadah_id,)
    try:
        cur.execute(cmd, values)
        row = cur.fetchone()
        if row:
            wadah = {
                'id': row[0],
                'nama_wadah': row[1],
                'berat_kosong': float(row[2])
            }
            return jsonify(wadah)
        else:
            return jsonify({'status': 'not found'}), 404
    except Exception as e:
        print(f"Error fetching wadah: {e}")
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/wadah/<int:wadah_id>', methods=['PUT'])
def api_update_wadah(wadah_id):
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "UPDATE tblwadah SET nama=%s, berat=%s WHERE id=%s"
    values = (data['nama_wadah'], data['berat_kosong'], wadah_id)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error updating wadah: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/wadah/<int:wadah_id>', methods=['DELETE'])
def api_delete_wadah(wadah_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "DELETE FROM tblwadah WHERE id=%s"
    values = (wadah_id,)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error deleting wadah: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/produk', methods=['GET'])
def api_get_produk():
    results = db_query("SELECT * FROM tblproduk ORDER BY id ASC")
    produk_list = []
    if results:
        for row in results:
            produk = {
                'id': row[0],
                'nama_produk': row[1]
            }
            produk_list.append(produk)
    return jsonify(produk_list)

@app.route('/api/produk', methods=['POST'])
def api_add_produk():
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "INSERT INTO tblproduk (nama) VALUES (%s) RETURNING id"
    values = (data['nama_produk'],)
    try:
        cur.execute(cmd, values)
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({'status': 'success', 'id': new_id, 'nama_produk': data['nama_produk']})
    except Exception as e:
        print(f"Error inserting produk: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/produk/<int:produk_id>', methods=['DELETE'])
def api_delete_produk(produk_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "DELETE FROM tblproduk WHERE id=%s"
    values = (produk_id,)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error deleting produk: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/produk/<int:produk_id>', methods=['GET'])
def api_get_produk_by_id(produk_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "SELECT * FROM tblproduk WHERE id=%s"
    values = (produk_id,)
    try:
        cur.execute(cmd, values)
        row = cur.fetchone()
        if row:
            produk = {
                'id': row[0],
                'nama_produk': row[1]
            }
            return jsonify(produk)
        else:
            return jsonify({'status': 'not found'}), 404
    except Exception as e:
        print(f"Error fetching produk: {e}")
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/produk/<int:produk_id>', methods=['PUT'])
def api_update_produk(produk_id):
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "UPDATE tblproduk SET nama=%s WHERE id=%s"
    values = (data['nama_produk'], produk_id)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error updating produk: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/pengguna', methods=['GET'])
def api_get_pengguna():
    results = db_query("SELECT * FROM tbluser ORDER BY id ASC")
    pengguna_list = []
    if results:
        for row in results:
            pengguna = {
                'id': row[0],
                'user': row[1],
                'role': row[2]
            }
            pengguna_list.append(pengguna)
    return jsonify(pengguna_list)

@app.route('/api/pengguna', methods=['POST'])
def api_add_pengguna():
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "INSERT INTO tbluser (\"user\", role, \"password\") VALUES (%s, %s, md5(%s))"
    values = (data['user'], data['role'], data['password'])
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error inserting pengguna: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/pengguna/<int:pengguna_id>', methods=['DELETE'])
def api_delete_pengguna(pengguna_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "DELETE FROM tbluser WHERE id=%s"
    values = (pengguna_id,)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error deleting pengguna: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/pengguna/<int:pengguna_id>', methods=['PUT'])
def api_update_pengguna(pengguna_id):
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "UPDATE tbluser SET \"user\"=%s, role=%s, \"password\"=md5(%s) WHERE id=%s"
    values = (data['user'], data['role'], data['password'], pengguna_id)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error updating pengguna: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/pengguna/<int:pengguna_id>', methods=['GET'])
def api_get_pengguna_by_id(pengguna_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "SELECT * FROM tbluser WHERE id=%s"
    values = (pengguna_id,)
    try:
        cur.execute(cmd, values)
        row = cur.fetchone()
        if row:
            pengguna = {
                'id': row[0],
                'user': row[1],
                'role': row[2]
            }
            return jsonify(pengguna)
        else:
            return jsonify({'status': 'not found'}), 404
    except Exception as e:
        print(f"Error fetching pengguna: {e}")
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/supplier', methods=['GET'])
def api_get_supplier():
    results = db_query("SELECT * FROM tblsupplier ORDER BY id ASC")
    supplier_list = []
    if results:
        for row in results:
            supplier = {
                'id': row[0],
                'nama': row[1],
                'email': row[2],
                'alamat': row[3],
                'nama_pic': row[4],
                'no_kontak': row[5]
            }
            supplier_list.append(supplier)
    return jsonify(supplier_list)

@app.route('/api/supplier', methods=['POST'])
def api_add_supplier():
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "INSERT INTO tblsupplier (nama, email, alamat, pic, kontak) VALUES (%s, %s, %s, %s, %s)"
    values = (data['nama'], data['email'], data['alamat'], data['nama_pic'], data['no_kontak'])
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error inserting supplier: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/supplier/<int:supplier_id>', methods=['GET'])
def api_get_supplier_by_id(supplier_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "SELECT * FROM tblsupplier WHERE id=%s"
    values = (supplier_id,)
    try:
        cur.execute(cmd, values)
        row = cur.fetchone()
        if row:
            supplier = {
                'id': row[0],
                'nama': row[1],
                'email': row[2],
                'alamat': row[3],
                'nama_pic': row[4],
                'no_kontak': row[5]
            }
            return jsonify(supplier)
        else:
            return jsonify({'status': 'not found'}), 404
    except Exception as e:
        print(f"Error fetching supplier: {e}")
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/supplier/<int:supplier_id>', methods=['PUT'])
def api_update_supplier(supplier_id):
    data = request.json
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "UPDATE tblsupplier SET nama=%s, email=%s, alamat=%s, pic=%s, kontak=%s WHERE id=%s"
    values = (data['nama'], data['email'], data['alamat'], data['nama_pic'], data['no_kontak'], supplier_id)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error updating supplier: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/supplier/<int:supplier_id>', methods=['DELETE'])
def api_delete_supplier(supplier_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "DELETE FROM tblsupplier WHERE id=%s"
    values = (supplier_id,)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error deleting supplier: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/master_data', methods=['GET'])
def api_get_master_data():
    wadah = api_get_wadah().get_json()
    produk = api_get_produk().get_json()
    supplier = api_get_supplier().get_json()
    return jsonify({
        'wadah': wadah,
        'produk': produk,
        'supplier': supplier
    })

@app.route('/api/transaksi', methods=['POST'])
def api_create_transaksi():
    data = request.json or {}
    # simple id: date + short uuid
    id_transaksi = f"{datetime.datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    supplier = data.get('supplier')
    nopol = data.get('nopol')
    driver = data.get('driver')
    # Insert into table transaksi (create table DDL below)
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    try:
        cmd = """INSERT INTO transaksi (id_transaksi, supplier, nopol, driver, status, created_at)
                 VALUES (%s, %s, %s, %s, %s, NOW())"""
        cur.execute(cmd, (id_transaksi, supplier, nopol, driver, 'active'))
        conn.commit()
        return jsonify({'status': 'success', 'id_transaksi': id_transaksi, 'supplier': supplier, 'nopol': nopol, 'driver': driver})
    except Exception as e:
        print("Error creating transaksi:", e)
        conn.rollback()
        return jsonify({'status': 'failure', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/transaksi', methods=['GET'])
def api_list_transaksi():
    conn = db_connect()
    if conn is None:
        return jsonify([]), 200
    cur = conn.cursor()
    try:
        cmd = "SELECT id_transaksi, supplier, nopol, driver, status, created_at FROM transaksi WHERE status = 'active' ORDER BY created_at DESC"
        cur.execute(cmd)
        rows = cur.fetchall()
        out = []
        for r in rows:
            out.append({
                'id_transaksi': r[0],
                'supplier': r[1],
                'nopol': r[2],
                'driver': r[3],
                'status': r[4],
                'created_at': r[5].isoformat() if r[5] else None
            })
        return jsonify(out)
    except Exception as e:
        print("Error listing transaksi:", e)
        return jsonify([]), 200
    finally:
        cur.close()
        conn.close()

@app.route('/api/transaksi/all', methods=['GET'])
def api_all_transaksi():
    conn = db_connect()
    if conn is None:
        return jsonify([]), 200
    cur = conn.cursor()
    try:
        cmd = "SELECT id_transaksi, supplier, nopol, driver, status, created_at FROM transaksi ORDER BY created_at DESC"
        cur.execute(cmd)
        rows = cur.fetchall()
        out = []
        for r in rows:
            out.append({
                'id_transaksi': r[0],
                'supplier': r[1],
                'nopol': r[2],
                'driver': r[3],
                'status': r[4],
                'created_at': r[5].isoformat() if r[5] else None
            })
        return jsonify(out)
    except Exception as e:
        print("Error listing transaksi:", e)
        return jsonify([]), 200
    finally:
        cur.close()
        conn.close()

# Delete transaksi by id

@app.route('/api/transaksi/<id_transaksi>', methods=['DELETE'])
def api_delete_transaksi(id_transaksi):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    try:
        cmd = "DELETE FROM transaksi WHERE id_transaksi = %s"
        cur.execute(cmd, (id_transaksi,))
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error deleting transaksi: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

# Get transaksi by id
@app.route('/api/transaksi/<id_transaksi>', methods=['GET'])
def api_get_transaksi(id_transaksi):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    try:
        cmd = "SELECT id_transaksi, supplier, nopol, driver, status, created_at FROM transaksi WHERE id_transaksi=%s"
        cur.execute(cmd, (id_transaksi,))
        row = cur.fetchone()
        if not row:
            return jsonify({'status': 'not found'}), 404
        t = {
            'id_transaksi': row[0],
            'supplier': row[1],
            'nopol': row[2],
            'driver': row[3],
            'status': row[4],
            'created_at': row[5].isoformat() if row[5] else None
        }
        return jsonify(t)
    except Exception as e:
        print("Error get transaksi:", e)
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

# Add riwayat timbang to a specific transaksi
@app.route('/api/transaksi/<id_transaksi>/timbang', methods=['POST'])
def api_add_timbang_to_transaksi(id_transaksi):
    data = request.json or {}
    # Expect keys: wadah, produk, berat_kotor, berat_tare, berat_nett, operator, keterangan (optional)
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    try:
        # ensure transaksi exists
        cur.execute("SELECT 1 FROM transaksi WHERE id_transaksi=%s", (id_transaksi,))
        if cur.fetchone() is None:
            return jsonify({'status': 'transaksi_not_found'}), 404

        cmd = """INSERT INTO tbltimbangan 
                 (id_transaksi, nama_wadah, nama_produk, berat_kotor, berat_tare, berat_nett, operator, supplier, driver, nopol, remarks)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                 RETURNING id"""
        values = (
            id_transaksi,
            data.get('wadah'),
            data.get('produk'),
            data.get('berat_kotor'),
            data.get('berat_tare'),
            data.get('berat_nett'),
            data.get('operator'),
            data.get('supplier'),
            data.get('driver'),
            data.get('nopol'),
            data.get('keterangan')
        )
        cur.execute(cmd, values)
        new_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({'status': 'success', 'id': new_id})
    except Exception as e:
        print("Error inserting riwayat for transaksi:", e)
        conn.rollback()
        return jsonify({'status': 'failure', 'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Get riwayat timbang per transaksi (for DataTables)
@app.route('/api/transaksi/<id_transaksi>/timbang', methods=['GET'])
def api_get_timbang_by_transaksi(id_transaksi):
    conn = db_connect()
    if conn is None:
        return jsonify([]), 200
    cur = conn.cursor()
    try:
        cmd = """SELECT id, tanggal, waktu, nama_wadah, nama_produk, berat_kotor, berat_tare, berat_nett, operator, supplier, driver, nopol, id_transaksi, remarks
                 FROM tbltimbangan
                 WHERE id_transaksi=%s
                 ORDER BY id ASC"""
        cur.execute(cmd, (id_transaksi,))
        rows = cur.fetchall()
        out = []
        for r in rows:
            out.append({
                'id': r[0],
                'tgl': r[1].strftime("%Y-%m-%d") if r[1] else None,
                'waktu': r[2].strftime("%H:%M:%S") if r[2] else None,
                'wadah': r[3],
                'produk': r[4],
                'berat_kotor': float(r[5]) if r[5] is not None else None,
                'berat_tare': float(r[6]) if r[6] is not None else None,
                'berat_nett': float(r[7]) if r[7] is not None else None,
                'operator': r[8],
                'supplier': r[9],
                'driver': r[10],
                'nopol': r[11],
                'id_transaksi': r[12],
                'remarks': r[13]
            })
        return jsonify(out)
    except Exception as e:
        print("Error fetching riwayat by transaksi:", e)
        return jsonify([]), 200
    finally:
        cur.close()
        conn.close()

# Close transaksi (set status closed)
@app.route('/api/transaksi/<id_transaksi>/close', methods=['POST'])
def api_close_transaksi(id_transaksi):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    try:
        cur.execute("UPDATE transaksi SET status='closed' WHERE id_transaksi=%s", (id_transaksi,))
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print("Error closing transaksi:", e)
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.put("/api/timbang/<int:id_timbang>/remarks")
def update_remarks(id_timbang):
    data = request.get_json()
    remarks = data['remarks']

    conn = db_connect()
    cur = conn.cursor()

    cur.execute("UPDATE tbltimbangan SET remarks = %s WHERE id = %s", (remarks, id_timbang))

    conn.commit()
    cur.close()

    return jsonify({"status": "ok", "id_timbang": id_timbang, "remarks": remarks})

@app.route('/api/riwayat_timbang/<int:id>', methods=['GET'])
def api_get_data_timbang(id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "SELECT * FROM tbltimbangan WHERE id=%s ORDER BY id ASC"
    values = (id,)
    try:
        cur.execute(cmd, values)
        r = cur.fetchall()[0]
        res = {
            "id": r[0],
            "tanggal": r[1].isoformat() if r[1] else None,
            "waktu": r[2].isoformat() if r[2] else None,
            "wadah": r[3],
            "produk": r[4],
            "berat_kotor": float(r[5]),
            "berat_tare": float(r[6]),
            "berat_nett": float(r[7]),
            "operator": r[8],
            "supplier": r[9],
            "driver": r[10],
            "nopol": r[11],
            "id_transaksi": r[12],
            "remarks": r[13]
        }
        return jsonify(res)
    except Exception as e:
        print(f"Error fetching riwayat timbang: {e}")
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/riwayat_timbang/<id>', methods=['PUT'])
def api_update_riwayat_timbang(id):
    data = request.get_json()
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "UPDATE tbltimbangan SET nama_wadah=%s, nama_produk=%s, berat_kotor=%s, berat_tare=%s, berat_nett=%s WHERE id=%s"
    values = (data['wadah'], data['produk'], data['berat_kotor'], data['berat_tare'], data['berat_nett'], id)
    try:
        cur.execute(cmd, values)
        conn.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error fetching riwayat timbang: {e}")
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@app.route('/api/riwayat_timbang/<int:riwayat_id>', methods=['DELETE'])
def api_delete_riwayat_timbang(riwayat_id):
    conn = db_connect()
    if conn is None:
        return jsonify({'status': 'failure'}), 500
    cur = conn.cursor()
    cmd = "DELETE FROM tbltimbangan WHERE id=%s"
    values = (riwayat_id,)
    try:
        cur.execute(cmd, values)
        conn.commit()
        print("Deleted riwayat timbang with id:", riwayat_id)
        return jsonify({'status': 'success'})
    except Exception as e:
        print(f"Error deleting riwayat timbang: {e}")
        conn.rollback()
        return jsonify({'status': 'failure'}), 500
    finally:
        cur.close()
        conn.close()

@sock.on('connect')
def handle_connect():
    print('Client connected')

@sock.on('test')
def handle_message(msg):
    print('Message received: ' + msg)
    send(msg, broadcast=True)

def thread_serialread():
    global _exit, data_serial
    ser = load_serial()
    try:
        while True:
            if ser == None:
                print("Silahkan pilih com port")
                return None
            data = read_serial_data(ser)
            if data:
                with _thread_lock:
                    data_serial = parse_weight(data)
                print(f"data: {data}")
            else:
                print("No data received")
            if _exit:
                break
    except Exception as e:
        print("Exiting...")
        print(e)
    finally:
        if ser is not None:
            ser.close()
        print("Serial thread stopped")

def thread_sendwebsocket():
    global _exit, data_serial
    try:
        while True:
            with _thread_lock:
                if data_serial:
                    sock.emit('serial_data', data_serial)
            if _exit:
                break
            eventlet.sleep(0.1)
    except Exception as e:
        print("WebSocket thread exiting...")
        print(e)
    finally:
        print("WebSocket thread stopped")

if __name__ == '__main__':
    load_config()
    _serial_thread = threading.Thread(target=thread_serialread, daemon=True)
    _serial_thread.start()
    websocket_thread = eventlet.spawn(thread_sendwebsocket)
    sock.run(app, debug=False, host='0.0.0.0', port=5000)
    _exit = True
    if _serial_thread and _serial_thread.is_alive():
        _serial_thread.join(timeout=2)