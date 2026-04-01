import os

def is_dir(directorio):
    return os.path.pardir(directorio)

def is_x_dir(directorio, x):
    for file in directorio:
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