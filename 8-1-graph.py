import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
import math

with open("./settings.txt", "r") as settings_file:
    settings_data = [float(num) for num in settings_file.read().split("\n")]

data_arr = np.loadtxt("./data.txt", dtype=int)

volt_step = settings_data[1]
time_step = settings_data[0]

volt_arr = data_arr * volt_step
time_arr = np.arange(0, len(data_arr)) * time_step

volt_max     = np.max(volt_arr)
volt_max_ind = np.argmax(volt_arr)
time_max     = np.max(time_arr)
time_max_ind = np.argmax(time_arr)

charge_data    = [time_arr[0:volt_max_ind:], volt_arr[0:volt_max_ind:]]
discharge_data = [time_arr[volt_max_ind::] , volt_arr[volt_max_ind::]]

figure, axes = plt.subplots(figsize = (16, 10), dpi = 400)

axes.set_xlabel("Time, sec", fontsize = 16)
axes.set_ylabel("Volt, mV", fontsize = 16)
axes.set_title("Capacitor carge and discarge graph", fontsize = 20)

charge_plot_line   , = axes.plot(charge_data[0], charge_data[1], color = 'red')
discharge_plot_line, = axes.plot(discharge_data[0], discharge_data[1], color = 'blue')

charge_plot_line.set_label("Charge line")
discharge_plot_line.set_label("Discharge line")
axes.legend(prop={"size":16})

x_limits = (0.0, math.ceil(time_max))
y_limits = (0.0, 3.5)
axes.set(xlim = x_limits, ylim = y_limits)

axes.xaxis.set_minor_locator(MultipleLocator(0.5))
axes.xaxis.set_major_locator(MultipleLocator(1.0))
axes.yaxis.set_minor_locator(MultipleLocator(0.25))
axes.yaxis.set_major_locator(MultipleLocator(0.5))

axes.grid(color = "gray", which = "both", linestyle = ':', linewidth = 0.5)

charge_time = time_arr[volt_max_ind] - time_arr[0]
discharge_time = time_arr[-1] - time_arr[volt_max_ind]

axes.axvline(x = charge_time, ymin = y_limits[0], ymax = volt_max/y_limits[1], color='green', linestyle='dashed')
axes.axhline(y = volt_max, xmin = x_limits[0], xmax = charge_time/x_limits[1], color='green', linestyle='dashed')

axes.scatter(time_arr[volt_max_ind], volt_max, color='brown')

axes.scatter(x = charge_time, y = 0.0, color = 'green')
axes.text(x = charge_time + 0.1, y = 0.05, s = str(round(charge_time, 2)), fontsize = 14)

axes.scatter(x = 0.0, y = volt_max, color = 'green')
axes.text(x = 0.1, y = volt_max + 0.05, s = str(round(charge_time, 2)), fontsize = 14)

axes.text(x = (charge_time / 2 - 0.8), y = volt_max / 2, s = ("charge time: " + str(round(charge_time, 2)) + "sec"), color = 'blue', fontsize = 14)
axes.text(x = (charge_time + discharge_time / 2 - 0.8), y = volt_max / 2, s = ("discharge time: " + str(round(discharge_time, 2)) + "sec"), color = 'yellow', fontsize = 14)

figure.savefig("graph.svg")