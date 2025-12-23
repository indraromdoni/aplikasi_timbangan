import json
import psycopg2

_config = {}

def load_config():
    global _config
    with open('config.json', 'r') as f:
        _config = json.load(f)
    f.close()

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

def print_data(id_transaksi):
    conn = db_connect()
    if conn is None:
        #return jsonify({'status': 'failure'}), 500
        pass
    cur = conn.cursor()
    cmd_data_transaksi = "SELECT id_transaksi, supplier, nopol, driver FROM transaksi WHERE id_transaksi=%s;"
    cmd_list_produk = "SELECT nama_produk, COUNT(*) AS jumlah FROM tbltimbangan WHERE id_transaksi=%s GROUP BY nama_produk ORDER BY jumlah DESC;"
    data_out = {}
    try:
        cur.execute(cmd_data_transaksi, (id_transaksi,))
        data_transaksi = cur.fetchall()[0]
        print(data_transaksi)
        colnames = [desc[0] for desc in cur.description]
        data_out.update({col: val for col, val in zip(colnames, data_transaksi)})
        cur.execute(cmd_list_produk, (id_transaksi,))
        list_produk = cur.fetchall()
        for produks in list_produk:
            #print(produks[0])
            produk = produks[0]
            cmd_data = """
                SELECT id, nama_wadah, berat_kotor, berat_tare, berat_nett
                FROM tbltimbangan
                WHERE id_transaksi=%s AND nama_produk=%s
                ORDER BY id;"""
            cur.execute(cmd_data, (id_transaksi, produk))
            listdata = cur.fetchall()
            #print(listdata)
            data = {}
            for d in listdata:
                data['id'] = d[0]
                data['wadah'] = d[1]
                data['berat_kotor'] = float(d[2])
                data['berat_tare'] = float(d[3])
                data['berat_nett'] = float(d[4])
            data_out['produk'] = {produk: data}
        print(data_out)
    except Exception as e:
        print(f'Error fetch print data : {e}')
    finally:
        cur.close()
        conn.close()

if __name__=='__main__':
    load_config()
    print_data('20251208-93b551')