from .correlate import analyse_data
from .args import arguments


def run():
    options = arguments()
    file_list = find_files(options.key)

    if options.list:
        print(file_list)
    else:
        for file in file_list:
            analyse_data(file, numcol=5)
