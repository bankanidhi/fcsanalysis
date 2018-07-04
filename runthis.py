import numpy as np
import scipy
import matplotlib.pyplot as plt
from scipy.optimize import least_squares
from scipy.optimize import curve_fit
from lmfit import Model


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


def correlation(x, g0, tauD, bl):
    return g0/((1+x/tauD)*(1+0.01*x/tauD)**(0.5))+bl

# Read this http://www.scipy-lectures.org/intro/numpy/index.html


reshaped = return_corr_function(filename="rb.sin", numcol=5)


t = reshaped[:, 0]
x = reshaped[:, 1]
x1 = reshaped[:, 4]

mask = (t > 1e-5) * (t < 1)
# Read http://www.scipy-lectures.org/
# intro/numpy/array_object.html#indexing-and-slicing
useful_t = t[mask]
useful_x = x[mask]
useful_x1 = x1[mask]
# print("here")

gmodel = Model(correlation)
result = gmodel.fit(useful_x, x=useful_t, g0=0.5, tauD=0.0001, bl=1.0000001)

print(result.fit_report())


def plot_corrcurve():
    plt.semilogx(useful_t, useful_x, 'bo')
    #plt.semilogx(useful_t, result.init_fit, 'k--')
    plt.semilogx(useful_t, result.best_fit, 'r-')
    plt.title('Rhodamine B', fontsize=12)
    #plt.text(0.002,1.035, 'RB', fontsize=12)
    plt.xlabel('Delay time (s)', fontsize=12)
    plt.ylabel('Autocorrelation, $G(\\tau)$', fontsize=12)
    plt.show()
