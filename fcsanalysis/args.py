import argparse


def arguments():
    des = "FCS analysis"
    parser = argparse.ArgumentParser(description=des,
                                     prog="python -m fcsanalysis")

    parser.add_argument("-k",
                        help="Keyword",
                        default="*.sin")

    parser.add_argument("--list",
                        help="Show files that are to be opened,\
                        without opening them.",
                        action="store_true")

    args = parser.parse_args()
    return args
