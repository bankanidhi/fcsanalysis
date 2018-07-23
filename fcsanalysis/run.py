from .correlate import analyse_data, find_files
from .args import arguments


def run():
    options = arguments()
    file_list = find_files(options.k)

    if options.list:
        print("----------------------")
        for f in file_list:
            print(f)
        print("----------------------")
        print("Total files found:", len(file_list))
        print("----------------------")
        exit()
    else:
        for file in file_list:
            analyse_data(file, int(options.numcol))
