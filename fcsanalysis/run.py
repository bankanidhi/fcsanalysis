from .correlate import analyse_data
from .args import arguments


def run():
    options = arguments()
    file_list = find_files(options.key)

    if options.list:
        for f in file_list:
            print(f)
        print("======================")
        print("Total files found:", len(files))
        print("======================")
        exit()
    else:
        for file in file_list:
            analyse_data(file, numcol=5)
