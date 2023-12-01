import numpy as np
import matplotlib.pyplot as plt

# take the log of x and y, fit the linear function to the curve
# input x, y: np.array
#       graph_title: string
#       x_label,y_label: string, label of each axis
def log_fit_plot(x,y,x_label,y_label,graph_title): 
    print(y)
    x_log = np.log10(x)
    y_log = np.log10(y) 
    print(y_log)
    plt.plot(x_log,y_log,linestyle ="",marker='o')
    plt.xlabel("Log({})".format(x_label))
    plt.ylabel("Log({})".format(y_label))

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
        "./data/"+graph_title+".png",bbox_inches="tight"
    )
    plt.show()

def half_width_analysis(L_prob_list):
    L_list = [L_prob_list[i][0] for i in range(len(L_prob_list))]
    prob_list = [L_prob_list[i][1] for i in range(len(L_prob_list))]
    half_width_list = []
    
    for j in range(len(L_list)):
        print(L_list[j])
        data = prob_list[j]
        peak_height = np.max(data[:,1])
        peak_center = np.argmax(data[:,1])

        # Find the indices where data is approximately half the peak height
        left_half_index = np.argmin(np.abs(data[:peak_center,1] - peak_height / 2))
        right_half_index = np.argmin(np.abs(data[peak_center:,1] - peak_height / 2)) + peak_center

        left_half = data[left_half_index,0]
        right_half = data[right_half_index,0]
        # Calculate the half-width
        half_width = right_half - left_half
        half_width_list.append(half_width)
    
    thing_to_save = np.zeros((len(L_list),2))
    thing_to_save[:,0] = np.array(L_list)
    thing_to_save[:,1] = np.array(half_width_list)
    np.savetxt(
            "./data/half_width.csv",
            thing_to_save,
            delimiter=",",
        )
    log_fit_plot(L_list, half_width_list, x_label=r"width of lattice $L$",y_label=r"half width",graph_title="half_width_plot")
    
    return half_width_list