from parse.parse import parse_bill
from bdd.bdd import save_bill

def submit_bill(bill):
    company_name, bill_number, net_amount, comision, month_year = parse_bill(bill)
    save_bill(company_name, bill_number, net_amount, comision, month_year)
