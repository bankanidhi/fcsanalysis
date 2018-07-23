from .correlate import analyse_data, find_files
from .args import arguments


def run():
    # Stores the parsed arguments
    options = arguments()
    # Get a list of files that match the keyword as given with the -k arg
    file_list = find_files(options.k)

    # If the user wants to perform a dry run.
    if options.list:
        print("----------------------")
        for f in file_list:
            print(f)
        print("----------------------")
        print("Total files found:", len(file_list))
        print("----------------------")
        exit()

    # The actually analysis happens after this.
    else:
        for file in file_list:
            analyse_data(file, int(options.numcol))
