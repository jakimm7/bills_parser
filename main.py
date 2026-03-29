from datetime import datetime
from pathlib import Path
import os
from parse.parse import parse_bills, update_csv

def main():
    date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    csv_directory = Path("csv")
    directory = input("Ingrese la ruta absoluta del directorio con las facturas: ")

    for file in os.listdir(directory):
        if file.endswith("PDF"):
            path = os.path.join(directory, file)
            bill_number, company_name, net_amount = parse_bills(path)
            final_csv_path = os.path.join(csv_directory, f"csv{date}.csv")
            update_csv(final_csv_path, company_name, bill_number, net_amount)
    
    print(f"Archivo creado a las {date}")

if __name__ == "__main__":
    main()
