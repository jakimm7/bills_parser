import os
from pathlib import Path
from interfaz.interfaz import save_bill
from parse.parse import parse_bill, parse_date
from bdd.bdd import set_paid_bill, get_month_comision
from utils.utils import *

DB_DIR = Path("./bills_per_month")
EXTENSION_DB = "db"
EXTENSION_PDF = "PDF"
OPCION_CARGAR = "1"
OPCION_MARCAR = "2"
OPCION_TOTAL = "3"
OPCION_PAGAR = "4"
OPCION_SALIR = "X"

MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

def main():
    print("Bienvenido a Bill Parser")
    exit = False

    while not exit:
        print("Oprima el número correspondiente a la operacion que quiere realizar")
        print("1) Cargar facturas desde un directorio")
        print("2) Marcar facturas como pagas")
        print("3) Obtener el monto de comisiones que hay que abonar")
        print("4) Pagar comisiones")
        print("X) Salir")

        operation = str(input("Ingrese la opción deseada: "))

        if operation == OPCION_CARGAR:
            directory = input("Ingrese la ruta absoluta del directorio con las facturas: ")
            while not is_dir(directory) or not is_x_dir(EXTENSION_PDF, directory):
                directory = input("La ruta que ingreso no existe o no tiene facturas en formato PDF, ingrese otra nuevamente: ")

            for file in compile_files(directory):
                save_bill(file)
                
        elif operation == OPCION_MARCAR:
            paid_bill_number = input("Ingrese el número de la factura pagada (ingresa los últimos 4 números): ")
            bill_month = input("Ingrese el mes de la factura (Ejemplo: si la factura es de marzo, 03): ")
            while bill_month not in MONTHS:
                bill_month = input("Ingrese un mes válido: ")

            bill_year = input("Ingrese el año de la factura: ")
            set_paid_bill(f"0010-0000{paid_bill_number}", f"{bill_month}_{bill_year}")

        elif operation == OPCION_TOTAL:
            monto, facturas = 0, {}
            db_directory, files = compile_files(EXTENSION_DB, DB_DIR)

            if not db_directory:
                input("No hay facturas cargadas en el sistema! Pulsa cualquier tecla para volver al menu principal")
                continue

            for file in files:
                monto_actual, factura = get_month_comision(Path(file).name)
                monto += monto_actual
                facturas[factura] = monto

            monto_transformado = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            print(f"El monto a pagar es: $ {monto_transformado}")
        
        elif operation == OPCION_PAGAR:
            monto_a_pagar = float(input("Ingrese el monto a pagar: "))
            db_directory, files = compile_files(EXTENSION_DB, DB_DIR)

            if not db_directory:
                input("No hay facturas cargadas en el sistema! Pulsa cualquier tecla para volver al menu principal")
                continue

        elif operation.upper() == OPCION_SALIR:
            break
        
        else:
            print("Ingrese una operacion válida")

        input("Pulse cualquier tecla para volver al menu principal ")
        os.system("clear")

if __name__ == "__main__":
    main()
