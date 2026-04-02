from parse.parse import parse_bill
from pathlib import Path
from bdd.bdd import save_bill, bill_in_table, set_paid_bill, get_month_comision
from utils.utils import *

EXTENSION_DB = "db"
DB_DIR = Path("./bills_per_month")

def submit_bill(bill):
    company_name, bill_number, net_amount, comision, month_year = parse_bill(bill)
    save_bill(company_name, bill_number, net_amount, comision, month_year)

def pay_bill(bill_number):
    bill_number = f"0010-0000{bill_number}"
    for db in compile_files(EXTENSION_DB, DB_DIR):
        if bill_in_table(bill_number, db):
            set_paid_bill(bill_number, db)
            break

def get_total_comision(db_files):
    monto_total, facturas_totales = 0, {}
    for db_file in db_files:
        monto_actual, facturas_totales = get_month_comision(db_file, facturas_totales)
        monto_total += monto_actual
    
    return monto_actual, facturas_totales
