import os

MONTHS = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]

def is_dir(directorio):
    return os.path.isdir(directorio)

def is_x_dir(directorio, x):
    for file in os.listdir(directorio):
        if file.endswith(x):
            return True
    return False

def compile_files(extension, directory):
    files = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            bill_path = os.path.join(directory, file)
            files.append(bill_path)

    return files

def valid_bill_number(bill_number):
    return len(bill_number) < 5