import os

def compile_files(extension, directory):
    valid_directory = False
    files = []
    for file in os.listdir(directory):
        if file.endswith(extension):
            valid_directory = True
            bill_path = os.path.join(directory, file)
            files.append(bill_path)

    if valid_directory:
        return True, files
    return False, None