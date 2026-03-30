import re
import csv
from pypdf import PdfReader
from bdd.bdd import save_bill

REGEX_FACTURA = r"Nº\s*(\d{4}-\d{8})"
REGEX_MONTO = r"[0-9,]+\.[0-9]{2}"
REGEX_FECHA = r"Fecha:?\s+(\d{2})/(\d{2})/(\d{4})"
MODO_APPEND = "a"
LINEA_PREVIA_MONTO = "SUBTOTAL"
INDICIO_LINEA_REGIMEN_FISCAL = ["RESPONSABLE INSCRIPTO", "RESPONSABLE MONOTRIBUTO"]
COMA = ","
COMILLA = '"'
PORCENTAJE_COMISION = 0.07
MONTH = 2
YEAR = 3

def parse_bills(bill_path):
    pdf_reader = PdfReader(bill_path)
    bill_number, company_name, net_amount, comision, month_year = None, None, None, None, None

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
            
            if not month_year:
                match_month_year = re.search(REGEX_FECHA, line)
                if match_month_year:
                    month = match_month_year.group(MONTH)
                    year = match_month_year.group(YEAR)
                    month_year = f"{month}_{year}"
            
            if not net_amount:
                if line == LINEA_PREVIA_MONTO:
                    match_net_amount = re.search(REGEX_MONTO, pdf_lines[i+1])
                    if match_net_amount:
                        monto_limpio = match_net_amount.group(0).replace(COMA, "")
                        net_amount = float(monto_limpio)
                        comision = net_amount * PORCENTAJE_COMISION
                        break

    save_bill(company_name, bill_number, net_amount, comision, month_year)