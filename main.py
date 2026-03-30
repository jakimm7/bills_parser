import os
from parse.parse import parse_bills
from bdd.bdd import set_paid_bill, get_month_comision
from datetime import datetime

EXTENSION_PDF = "PDF"
OPCION_CARGAR = "1"
OPCION_MARCAR = "2"
OPCION_TOTAL = "3"
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
        print("X) Salir")

        operation = str(input("Ingrese la opción deseada: "))
        if operation == OPCION_CARGAR:
            directory = input("Ingrese la ruta absoluta del directorio con las facturas: ")
            while not os.path.isdir(directory):
                directory = input("La ruta que ingreso no existe, ingrese otra nuevamente: ")

            pdf_directory = False
            for file in os.listdir(directory):
                if file.endswith(EXTENSION_PDF):
                    pdf_directory = True
                    bill_path = os.path.join(directory, file)
                    parse_bills(bill_path)

            if not pdf_directory:
                print("El directorio especificado no tiene facturas en formato pdf")
                
        elif operation == OPCION_MARCAR:
            paid_bill_number = input("Ingrese el número de la factura pagada: ")
            bill_month = input("Ingrese el mes de la factura (Ejemplo: Marzo - 03): ")
            while bill_month not in MONTHS:
                bill_month = input("Ingrese un mes válido: ")

            bill_year = input("Ingrese el año de la factura: ")
            set_paid_bill(paid_bill_number, f"{bill_month}_{bill_year}")

        # elif operation == OPCION_TOTAL:
        #     monto = get_month_comision(month_year)
        #     monto_transformado = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        #     print(f"El monto a pagar es: $ {monto_transformado}")

        elif operation.upper() == OPCION_SALIR:
            break
        
        else:
            print("Ingrese una operacion válida")

        input("Pulse cualquier tecla para volver al menu principal ")
        os.system("clear")

if __name__ == "__main__":
    main()
