import os
from pathlib import Path
from interfaz.interfaz import *
from parse.parse import parse_bill, parse_date
from bdd.bdd import set_paid_bill, get_month_comision
from utils.utils import *

DB_DIR = Path("./bills_per_month")
EXTENSION_DB = "db"
EXTENSION_PDF = ".PDF"
OPCION_CARGAR = "1"
OPCION_MARCAR = "2"
OPCION_TOTAL = "3"
OPCION_PAGAR = "4"
OPCION_SALIR = "X"
OPCION_CONTINUAR = "Y"

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
            while not is_dir(directory) or not is_x_dir(directory, EXTENSION_PDF):
                directory = input("La ruta que ingreso no existe o no tiene facturas en formato PDF, ingrese otra nuevamente: ")

            for file in compile_files(EXTENSION_PDF, directory):
                submit_bill(file)
                
        elif operation == OPCION_MARCAR:
            exit = False
            while not exit:
                paid_bill_number = input("Ingrese el número de la factura pagada (ingresa los últimos 4 números): ")
                while not valid_bill_number(paid_bill_number):
                    paid_bill_number = input("El número de factura no es válido: ")

                pay_bill(paid_bill_number)
                ingreso = input("Ingresa Y para cargar otra factura, X para continuar: ")
                if ingreso.upper() != OPCION_CONTINUAR:
                    break

        elif operation == OPCION_TOTAL:
            db_files = compile_files(EXTENSION_DB, DB_DIR)
            if len(db_files) == 0:
                input("No hay facturas cargadas en el sistema! Pulsa cualquier tecla para volver al menu principal")
                continue

            monto, facturas_totales = get_total_comision(db_files)

            monto_transformado = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            print(f"El monto a pagar es: $ {monto_transformado}")
            print("Las siguientes facturas tienen comision impaga: ")
            for razon_social in facturas_totales.keys():
                for factura in facturas_totales[razon_social]:
                    print(f"{factura} - {razon_social}")
        
        # elif operation == OPCION_PAGAR:
        #     monto_a_pagar = float(input("Ingrese el monto a pagar: "))
        #     db_directory, files = compile_files(EXTENSION_DB, DB_DIR)

        #     if not db_directory:
        #         input("No hay facturas cargadas en el sistema! Pulsa cualquier tecla para volver al menu principal")
        #         continue

        elif operation.upper() == OPCION_SALIR:
            break
        
        else:
            print("Ingrese una operacion válida")

        input("Pulse cualquier tecla para volver al menu principal ")
        os.system("clear")

if __name__ == "__main__":
    main()
