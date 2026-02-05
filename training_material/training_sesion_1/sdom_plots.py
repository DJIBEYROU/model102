import numpy as np
import pandas as pd
import os

from utils_plots import plot_capacity_donut, get_capacity_filtered, get_capacity_donut_color_map, get_vre_results, plot_heatmap
# ---------------------------
# ------ HEATMAPS PLOTS -----
# ---------------------------
current_folder = os.getcwd()
print("Current folder:", current_folder)

# Configuration----------------------------------
start_date = '2035-01-01 00:00:00' # Or any starting date
case_name = "Data"
prefix_folder_name = "sample_results"
# Configuration----------------------------------

output_folder_name = f"{prefix_folder_name}_{case_name}"
folder_csv_results = os.path.join(current_folder, output_folder_name)

results = pd.read_csv(os.path.join(folder_csv_results, f"OutputGeneration_{case_name}.csv"))
results_rearranged = get_vre_results(results)

skip_cols = ["Scenario", "Hour"]
for col_name in results_rearranged.columns:
    if col_name in skip_cols:
        continue
    plot_heatmap( results_rearranged, col_name, case_name, start_date=start_date )


# ---------------------------
# ------ CAPACITY PLOTS -----
# ---------------------------
# Open the csv file
data = pd.read_csv(os.path.join(folder_csv_results, f"OutputSummary_{case_name}.csv"))
capacity_filtered, sto_capacity_label_strings = get_capacity_filtered(data)
total_capacity = round(sum(capacity_filtered['Optimal Value'])/1000) #GW
color_map = get_capacity_donut_color_map(sto_capacity_label_strings)
colors = [color_map[label] for label in capacity_filtered['Technology']]  
plot_capacity_donut( capacity_filtered, colors, total_capacity, case_name )
a=1