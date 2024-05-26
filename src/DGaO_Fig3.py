import os
import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

def sort_by_laser_dia(name):
    match = re.search(r'laserDia_(\d+)mm.csv', name)
    if match:
        return int(match.group(1))
    else:
        return 0

def main():
    
    '''Directory containing data'''
    directory = "../data/csv_error_data/"
    
    '''Directory to save figures'''
    output_dir = "../plots/DGaO_revised_plots/"
    
    '''Create directory if it does not exist and do not raise errors otherwise'''
    os.makedirs(output_dir, exist_ok=True)

    filenames = []
    legend_labels = []
    dist_x_all = []
    dist_y_all = []

    '''Save filenames'''
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filenames.append(filename)
    
    '''Sort filenames in ascending order'''
    filenames = sorted(filenames, key=sort_by_laser_dia)
    
    for filename in filenames:
        params = filename.split("_")
        laser_dia = params[1][:-6] # Get laser diameter for legend labels
        csv_file = os.path.join(directory, filename)
        data = pd.read_csv(csv_file) # Read the data

        dist_x_all.append(data["Dist. X (mm)"])
        dist_y_all.append(data["Dist. Y (mm)"])
        legend_labels.append(laser_dia)

    plt.figure(figsize=(8,6))
    for dist_x, dist_y, label in zip(dist_x_all, dist_y_all, legend_labels):
        plt.plot(dist_x, dist_y, marker="o", linestyle=":", label=f"{label} mm")
    
    hexapod_x_y = 0.3
    plt.scatter(hexapod_x_y, hexapod_x_y, color="black", marker="*", s=200, zorder=10)
    plt.text(hexapod_x_y, 0.55, "Hexapod Coordinate", fontsize=14)
    plt.title("Laser speckle template position tracking", fontsize=15)
    plt.annotate('', xy=(hexapod_x_y, hexapod_x_y), xytext=(hexapod_x_y + 0.1, 0.5),arrowprops=dict(facecolor='black', width=0.9, headwidth=5, headlength=10))
    plt.xlabel("Position X-Axis (mm)", fontsize=15)
    plt.ylabel("Position Y-Axis (mm)", fontsize=15)
    plt.grid(True, linestyle="--", linewidth=0.5, color="gray")
    plt.legend(fontsize=15)
    plt.xlim(-1.3, 1.3)
    plt.ylim(-1.3, 1.3)
    plt.axvline(x=0, color="k", linewidth=1.5)
    plt.axhline(y=0, color="k", linewidth=1.5)
    plt.xticks(fontsize=15)
    plt.yticks(fontsize=15)

    '''Save the plot image file'''
    plot_filename = os.path.join(output_dir, "Fig_3.png")
    plt.savefig(plot_filename, dpi=700)
    # plt.show()
    plt.close()

if __name__ == "__main__":
    main()
