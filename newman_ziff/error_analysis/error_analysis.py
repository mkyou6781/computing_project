import numpy as np
import matplotlib.pyplot as plt
from newman_ziff.newman_ziff import LatticeDev, lattice_development

def estimate_critical_prob(L_list, repeat_time):
    result_to_save = []
    for L in L_list:
        print(L)
        wrapping_prob_list = []
        for j in range(repeat_time):
            lattice_dev = LatticeDev(L)
            wrapping_prob = lattice_development(lattice_dev)
            wrapping_prob = wrapping_prob / lattice_dev.N
            wrapping_prob_list.append(wrapping_prob)
        average = np.average(wrapping_prob_list)
        stdev = np.std(wrapping_prob_list)
        result_to_save.append([L,average,stdev])
        print(result_to_save)
    result_to_save = np.array(result_to_save)
    np.savetxt(
            "./data/convergence_of_data.csv",
            result_to_save,
            delimiter=",",
        )
    plt.errorbar(L_list,result_to_save[:,1],yerr=result_to_save[:,2],fmt='o',capsize=5)
    plt.hlines(y=0.592,xmin=0,xmax=L_list[-1],linestyle="--")
    plt.xlabel("lattice width L")
    plt.ylabel(r"wrapping probability $R_L(p)$")
    plt.savefig(
        "./data/convergence_to_theoretical_graph",bbox_inches="tight"
    )
    plt.show()

L_list = [32,113,170,256,384,576,864]
repeat_time = 10
#estimate_critical_prob(L_list, repeat_time)

#check how standard deviaiton scale with N
import pandas as pd

crit_prob_stat = pd.read_csv("./data/convergence_of_data.csv")
crit_prob_stat = np.array(crit_prob_stat)

print(crit_prob_stat)
print("at 0,0",crit_prob_stat[0,0])

stdev = crit_prob_stat[:,2]
L_list = crit_prob_stat[:,0]

stdev = np.array(stdev)
L_list = np.array(L_list)
N_list = L_list ** 2

x_log = np.log10(N_list)
y_log = np.log10(stdev) 
plt.plot(x_log,y_log,linestyle ="",marker='o')
plt.xlabel("Log(lattice size N)")
plt.ylabel("Log(standard deviation)")

# Fit the data with a linear function (degree 1 polynomial)
coefficients = np.polyfit(x_log,y_log, 1)
grad = int(coefficients[0] * 10 ** 2) / (10**2)
intercept= int(coefficients[1] * 10 **2) / (10**2)
# Create a linear function using the fitted coefficients
linear_function = np.poly1d(coefficients)

# Generate the fitted line (y values) for the given x coordinates
fitted_y_log_values = linear_function(x_log)

# Plot the data points
plt.plot(x_log, fitted_y_log_values,linestyle = "-", label="Fitted data: log(y) = {gradient}log(x) + {intercept}".format(gradient = grad,intercept=intercept))
plt.legend()
plt.savefig(
    "./data/convergence_of_stdev.png",bbox_inches="tight"
)
plt.show()

        