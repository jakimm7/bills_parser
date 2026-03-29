import sqlite3
from pathlib import Path

DB_DIR = Path(".")
DB_PATH = DB_DIR / "bills.db"

def initialize_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bills (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_name TEXT,
            bill_number TEXT UNIQUE,
            net_amount REAL,
            comision REAL,
            paid TEXT,
            comision_to_pay REAL
        )
    ''')
    
    conexion.commit()
    conexion.close()

def get_comision(bill_number):
    try:
        conexion = sqlite3.connect(DB_PATH)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()

        cursor.execute('''
            SELECT * FROM bills
            WHERE bill_number = ?
        ''', (bill_number,))

        bill = cursor.fetchone()

        if bill:
            return bill['comision']
        else:
            print(f"La factura número {bill_number} no está en la base de datos.")

    except sqlite3.Error as e:
        print(f"Error al leer la base de datos: {e}")
    finally:
        conexion.close()

def get_total_comisions():
    try: 
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()

        cursor.execute('''
            SELECT SUM(comision_to_pay) from bills
            ''')
        
        total = cursor.fetchone()[0]
        return total
        
    except sqlite3.Error as e:
        print(f"Error al leer la base de datos: {e}")
    finally:
        conexion.close()

def save_bill(company_name, bill_number, net_amount, comision):
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        cursor.execute('''
            INSERT INTO bills (company_name, bill_number, net_amount, comision, paid)
            VALUES (?, ?, ?, ?, ?)
        ''', (company_name, bill_number, net_amount, comision, "NO"))
        
        conexion.commit()
        print(f"Factura {bill_number} guardada correctamente.")
        
    except sqlite3.IntegrityError:
        print(f"Aviso: La factura {bill_number} de {company_name} ya estaba ingresada en el sistema.")
    finally:
        conexion.close()

def set_paid_bill(bill_number):
    try:
        conexion = sqlite3.connect(DB_PATH)
        cursor = conexion.cursor()
        
        cursor.execute('''
            UPDATE bills 
            SET paid = ?, comision_to_pay = ?
            WHERE bill_number = ?
        ''', ("SI", get_comision(bill_number), bill_number))
        
        if cursor.rowcount > 0:
            conexion.commit()
            print(f"Éxito: La factura {bill_number} fue actualizada como paga")
        else:
            print(f"Aviso: No se encontró la factura {bill_number} en la base de datos.")
            
    except sqlite3.Error as e:
        print(f"Error en la base de datos al intentar actualizar: {e}")
    finally:
        conexion.close()