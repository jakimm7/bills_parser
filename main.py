from datetime import datetime
from pathlib import Path
import os
from parse.parse import parse_bills, update_csv

EXTENSION_PDF = ".PDF"

def main():
    directory = input("Ingrese la ruta absoluta del directorio con las facturas: ")
    while not os.path.isdir(directory):
        directory = input("La ruta que ingreso no existe, ingrese otra nuevamente: ")

    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_directory = Path("csv")
    final_csv_path = os.path.join(csv_directory, f"csv{date}.csv")
    pdf_directory = False

    for file in os.listdir(directory):
        if file.endswith(EXTENSION_PDF):
            pdf_directory = True
            bill_path = os.path.join(directory, file)
            parse_bills(bill_path, final_csv_path)

    if not pdf_directory:
        print("El directorio especificado no tiene facturas en formato pdf")
        return

    print(f"Archivo creado a las {date}")

if __name__ == "__main__":
    main()
