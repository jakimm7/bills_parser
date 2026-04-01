import sqlite3
from pathlib import Path

DB_DIR = Path("./bills_per_month")
DB_PATH = DB_DIR / "bills.db"

def initialize_db(month_year):
    db_name = f"bills_{month_year}.db"
    conexion = sqlite3.connect(DB_DIR / db_name)
    cursor = conexion.cursor()

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS bills_{month_year} (
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

def get_bill_comision(bill_number, month_year):
    try:
        db_name = f"bills_{month_year}.db"
        conexion = sqlite3.connect(DB_DIR / db_name)
        conexion.row_factory = sqlite3.Row
        cursor = conexion.cursor()

        cursor.execute(f'''
            SELECT * FROM bills_{month_year}
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

def get_month_comision(db_name):
    try:
        table_name = db_name.replace(".db", "")
        conexion = sqlite3.connect(DB_DIR / db_name)
        cursor = conexion.cursor()

        cursor.execute(f'''
            SELECT SUM(comision_to_pay) from {table_name}
            ''')
        
        total = cursor.fetchone()[0]
        return total
        
    except sqlite3.Error as e:
        print(f"Error al leer la base de datos: {e}")
    finally:
        conexion.close()

def save_bill(company_name, bill_number, net_amount, comision, month_year):
    initialize_db(month_year)
    try:
        db_name = f"bills_{month_year}.db"
        conexion = sqlite3.connect(DB_DIR / db_name)
        cursor = conexion.cursor()
        
        cursor.execute(f'''
            INSERT INTO bills_{month_year} (company_name, bill_number, net_amount, comision, paid, comision_to_pay)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (company_name, bill_number, net_amount, comision, "NO", 0))
        
        conexion.commit()
        print(f"Factura {bill_number} guardada correctamente.")
        
    except sqlite3.IntegrityError:
        print(f"Aviso: La factura {bill_number} de {company_name} ya estaba ingresada en el sistema.")
    finally:
        conexion.close()

def set_paid_bill(bill_number, month_year):
    try:
        db_name = f"bills_{month_year}.db"
        conexion = sqlite3.connect(DB_DIR / db_name)
        cursor = conexion.cursor()
        
        cursor.execute(f'''
            UPDATE bills_{month_year} 
            SET paid = ?, comision_to_pay = ?
            WHERE bill_number = ?
        ''', ("SI", get_bill_comision(bill_number, month_year), bill_number))
        
        if cursor.rowcount > 0:
            conexion.commit()
            print(f"Éxito: La factura {bill_number} fue actualizada como paga")
        else:
            print(f"Aviso: No se encontró la factura {bill_number} en la base de datos.")
            
    except sqlite3.Error as e:
        print(f"Error en la base de datos al intentar actualizar: {e}")
    finally:
        conexion.close()