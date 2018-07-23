import glob
import numpy as np
import scipy
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
from lmfit import Model
matplotlib.style.use("seaborn-colorblind")


def return_corr_function_data(filename):
    """This function opens ascii files and reads the correlation function raw
    data.

    Parameters
    ----------
    filename : str
        The ascii file that has fcs data.

    Returns
    -------
    reshaped : ndarray
        An array with the first dimension as time and the other dimensions
        have the y-data.
    """
    # open the file as ascii as ascii_file
    with open(filename, "r") as ascii_file:
        # read the opened ascii_file to an array ascii_file_data
        ascii_file_data = ascii_file.read()
        # slicing the useful text from the raw data as useful_data
        useful_data = ascii_file_data[244:18963]

        # Find the number of columns in the data
        numcol = find_numcol(useful_data)

        # conversion of the ascii data to numpy array
        array_data = np.fromstring(useful_data, sep="\t")

        reshaped = array_data.reshape(
            int(len(array_data)/numcol), numcol)  # reshaped as 2D array

        # Returning transposed matrix for easy iteration
        return reshaped.T


def find_numcol(raw_text):
    first_line = raw_text.split("\n")[0]
    cols = first_line.split("\t")
    return len(cols)


def correlation(t, g0, tauD, bl):
    return g0/((1+t/tauD)*(1+0.01*t/tauD)**(0.5))+bl


def fit_model(t, y):
    gmodel = Model(correlation)
    return gmodel.fit(y, t=t, g0=0.5, tauD=0.0001, bl=1.0000001)


def generate_report(result):
    print(result.fit_report())


def plot_corrcurve(t, y, result):
    plt.semilogx(t, y, 'o')
    #plt.semilogx(t, result.init_fit, 'k--')
    plt.semilogx(t, result.best_fit, '-')
    plt.title('Rhodamine B', fontsize=12)
    #plt.text(0.002,1.035, 'RB', fontsize=12)
    plt.xlabel('Delay time (s)', fontsize=12)
    plt.ylabel('Autocorrelation, $G(\\tau)$', fontsize=12)
    plt.show()
    plt.close("all")
    return


def plot_corrcurve1(t, y_list, result_list):
    for y, result in zip(y_list, result_list):
        plt.semilogx(t, y, 'o', markersize=1)
        #plt.semilogx(t, result.init_fit, 'k--')
        plt.semilogx(t, result.best_fit, '-')
    plt.title('Rhodamine B', fontsize=12)
    #plt.text(0.002,1.035, 'RB', fontsize=12)
    plt.xlabel('Delay time (s)', fontsize=12)
    plt.ylabel('Autocorrelation, $G(\\tau)$', fontsize=12)
    plt.show()
    plt.close("all")
    return


def analyse_data(filename, lowlimit=1e-5, highlimit=1):
    corr_data = return_corr_function_data(filename=filename)
    t = corr_data[0]

    mask = (t > lowlimit) * (t < highlimit)

    # Limit the time axis in the raw data
    useful_t = t[mask]

    # Apply the same mask on all the y data
    useful_y_list = [y[mask] for y in corr_data[1:]]

    fitted_y_list = [fit_model(useful_t, y) for y in useful_y_list]

    plot_corrcurve1(t=useful_t, y_list=useful_y_list,
                    result_list=fitted_y_list)

    for y, result in zip(useful_y_list, fitted_y_list):
        plot_corrcurve(useful_t, y, result)


def find_files(keyword="./*.sin"):
    return sorted(glob.glob(keyword))
