import os
from parse.parse import parse_bills
from bdd.bdd import initialize_db, set_paid_bill, get_total_comisions

EXTENSION_PDF = "PDF"
OPCION_CARGAR = "1"
OPCION_MARCAR = "2"
OPCION_TOTAL = "3"
OPCION_SALIR = "X"

def main():
    initialize_db()
    exit = False
    print("Bienvenido a Bill Parser")

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
            set_paid_bill(paid_bill_number)

        elif operation == OPCION_TOTAL:
            monto = get_total_comisions()
            monto_transformado = f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
            print(f"El monto a pagar es: $ {monto_transformado}")

        elif operation.upper() == OPCION_SALIR:
            break
        
        else:
            print("Ingrese una operacion válida")

        input("Pulse cualquier tecla para volver al menu principal ")
        os.system("clear")

if __name__ == "__main__":
    main()
