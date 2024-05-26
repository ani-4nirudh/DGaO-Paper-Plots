import os
import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import t

def sort_by_laser_dia(name):
    match = re.search(r'laserDia_(\d+)mm.csv', name)
    if match:
        return int(match.group(1))
    else:
        return 0

def main():
    
    ''' Directory containing the error data files'''
    directory = "../data/csv_error_data/"    
    
    '''Directory to save plort figures'''
    output_dir = "../plots/DGaO_revised_plots/"

    '''Create directory if it does not exist'''
    os.makedirs(output_dir, exist_ok=True)

    filenames = []
    
    '''Store data for plotting'''
    all_frame_numbers = []
    all_errors = []
    legend_labels = []
    all_upper_confidence_bands = []
    all_lower_confidence_bands = []

    '''Saving filenames inside this directory'''
    for filename in os.listdir(directory):
        if filename.endswith(".csv"):
            filenames.append(filename)

    '''Sorting filenames'''
    filenames = sorted(filenames, key=sort_by_laser_dia)
    
    for filename in filenames:
        params = filename.split("_")
        laser_dia = params[1][:-6]

        csv_file = os.path.join(directory, filename)

        '''Read the csv file'''
        data = pd.read_csv(csv_file)
        
        '''Actual error values with =ve and -ve values'''
        data_error_x = data["Error X (mm)"]
        data_error_y = data["Error Y (mm)"]
        frame_number = list(range(0, data_error_x.size, 1))

        ''' Calculate error for each file'''
        data["Absolute Error (mm)"] = np.sqrt(data_error_x**2 + data_error_y**2)
        
        ''' Calculate mean and standard deviation for confidence bands'''
        mean_error = data["Absolute Error (mm)"].mean()
        std_error = data["Absolute Error (mm)"].std()
        sample_number = len(frame_number)

        '''Calculate t-value for 95% confidence interval'''
        t_value = t.ppf(0.975, df = sample_number-1)  # 95% confidence interval, two-tailed, df = degrees of freedom
        confidence_band = t_value * std_error / np.sqrt(sample_number)
        # upper_confidence_band = data["Absolute Error (mm)"] + confidence_band # Confidence bands around actual values       
        # lower_confidence_band = data["Absolute Error (mm)"] - confidence_band
        upper_confidence_band = mean_error + confidence_band # Confidence band around mean error
        lower_confidence_band = mean_error - confidence_band
        rmse_error = np.sqrt(np.mean(data["Absolute Error (mm)"]**2))
        
        '''Combine data from all csv files'''
        all_frame_numbers.append(frame_number)
        all_errors.append(data["Absolute Error (mm)"])
        legend_labels.append(f"{laser_dia} mm") 
        all_upper_confidence_bands.append(upper_confidence_band)
        all_lower_confidence_bands.append(lower_confidence_band)
        
        print(f"For {laser_dia} mm - Mean: {mean_error}, CI: ({lower_confidence_band}, {upper_confidence_band}), RMSE: {rmse_error}")

    # Plot the data
    plt.figure(figsize=(10,6))
    for frame_number, error, labels, upper_band, lower_band in zip(all_frame_numbers, all_errors, legend_labels, all_upper_confidence_bands, all_lower_confidence_bands):
        plt.plot(frame_number, error, marker="o", linestyle=":", label=labels)
        plt.fill_between(frame_number, lower_band, upper_band, alpha=0.3)
    
    plt.title("Error in XY plane for different laser spot diameters", fontsize=15)
    plt.xlabel("Frame Number", fontsize=15)
    plt.ylabel("Error (mm)", fontsize=15)
    plt.grid(True, linestyle="--", linewidth=0.5, color="gray")
    plt.legend(fontsize=14)
    plt.yticks(fontsize=14)
    plt.xticks(fontsize=14)

    # Saving the plot image
    plot_filename = os.path.join(output_dir, "Fig_2.png")
    plt.savefig(plot_filename, dpi=700)
    # plt.show()
    plt.close()

if __name__ == "__main__":
    main()
