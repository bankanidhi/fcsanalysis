import numpy as np
import scipy
import matplotlib
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
from lmfit import Model
matplotlib.style.use("seaborn-colorblind")

def return_corr_function(filename, numcol):
    """This function opens ascii files and reads the correlation function raw
    data.

    Parameters
    ----------
    filename : str
        The ascii file that has fcs data.

        numcol : int
                Number of columns including x.

        Returns
        -------

    """  # opening the file as ascii as ascii_file
    with open(filename, "r") as ascii_file:
        # reading the opened ascii_file to an array ascii_file_data
        ascii_file_data = ascii_file.read()
        # slicing the data as useful_data
        useful_data = ascii_file_data[244:18963]
        # conversion to an 1D array
        array_data = np.fromstring(useful_data, sep="\t")
        reshaped = array_data.reshape(
            int(len(array_data)/numcol), numcol)  # reshaped as 2D array
        return reshaped


def correlation(t, g0, tauD, bl):
    return g0/((1+t/tauD)*(1+0.01*t/tauD)**(0.5))+bl

# Read this http://www.scipy-lectures.org/intro/numpy/index.html


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


def analyse_data(filename, numcol, lowlimit=1e-5, highlimit=1):
    reshaped = return_corr_function(filename=filename, numcol=numcol)
    t = reshaped[:, 0]

    y_list = []
    for i in range(numcol-1):
        y_list.append(reshaped[:, i+1])

    mask = (t > lowlimit) * (t < highlimit)

    useful_t = t[mask]

    useful_y_list = []
    for y in y_list:
        useful_y_list.append(y[mask])

    fitted_y_list = []
    for y in useful_y_list:
        fitted_y_list.append(fit_model(useful_t, y))

    plot_corrcurve1(t=useful_t, y_list=useful_y_list,
                    result_list=fitted_y_list)

    exit()

    for y, result in zip(useful_y_list, fitted_y_list):
        plot_corrcurve(useful_t, y, result)


analyse_data("exampledata/rb.sin", numcol=5)
