import re
import csv
from pypdf import PdfReader

REGEX_FACTURA = r"Nº\s*(\d{4}-\d{8})"
REGEX_MONTO = r"[0-9,]+\.[0-9]{2}"
MODO_APPEND = "a"
LINEA_PREVIA_MONTO = "SUBTOTAL"
INDICIO_LINEA_REGIMEN_FISCAL = ["RESPONSABLE INSCRIPTO", "RESPONSABLE MONOTRIBUTO"]
COMA = ","
COMILLA = '"'

def update_csv(csv_path, company_name, bill_number, net_amount):
    with open(csv_path, MODO_APPEND, newline='', encoding='utf-8') as bills_csv:
        bills_writer = csv.writer(bills_csv, delimiter=";")
        bills_writer.writerow([company_name, bill_number, net_amount])

def parse_bills(bill_path, csv_path):
    pdf_reader = PdfReader(bill_path)
    bill_number, company_name, net_amount = None, None, None

    for page in pdf_reader.pages:
        text = page.extract_text()
        pdf_lines = text.splitlines()

        for i, line in enumerate(pdf_lines):
            if not bill_number:
                match_bill_number = re.search(REGEX_FACTURA, line)
                if match_bill_number:
                    bill_number = match_bill_number.group(1)
                    continue

            if not company_name:
                for indicio in INDICIO_LINEA_REGIMEN_FISCAL:
                    if indicio in line:
                        company_name = pdf_lines[i+1].replace(COMILLA, "").strip()
                        break
            
            if not net_amount:
                if line == LINEA_PREVIA_MONTO:
                    match_net_amount = re.search(REGEX_MONTO, pdf_lines[i+1])
                    if match_net_amount:
                        monto_limpio = match_net_amount.group(0).replace(COMA, "")
                        net_amount = float(monto_limpio)
                        break
                    
    update_csv(csv_path, company_name, bill_number, net_amount)