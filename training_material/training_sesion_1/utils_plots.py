import pandas as pd

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mc # For the legend
from matplotlib.colors import LinearSegmentedColormap

# Another utility for the legend
from matplotlib.cm import ScalarMappable
import os


# ---------------------------
# ------ GENERIC UTILS ------
# ---------------------------
def get_heatmap_custom_cmap():
    CB_color_cycle = [
                    '#00296b', "#047cd2",  "#19B7C2" , "#e1ff00", "#fdec00",  "#F9391CDA"                             
                    ]

    custom_cmap = LinearSegmentedColormap.from_list("my_cmap", CB_color_cycle)
    return custom_cmap


def check_folder_and_create(current_folder: str, folder_path: str):
    if not os.path.exists( os.path.join(current_folder, folder_path) ):
        os.makedirs( os.path.join(current_folder, folder_path) )


# ---------------------------
# ------ CAPACITY DONUT -----
# ---------------------------

def get_capacity_donut_color_map(
        sto_capacity_label_strings : list 
) -> dict:
    color_map = {'Thermal': '#5E1688', 
                'Solar PV': '#FFC903', 
                'Wind': '#00B6EF'}

    # Define a list of colors for storage technologies
    storage_colors = ['#FF4A88', '#FF4741', '#CC0079', '#FF7FBB', '#7F7FFF', "#FFCE89", '#47FFB3']

    # Add storage technologies to color_map dynamically
    for i, tech in enumerate(sto_capacity_label_strings):
        color_map[tech] = storage_colors[i % len(storage_colors)]
    
    return color_map

def get_capacity_filtered(data: pd.DataFrame):
    # Doughnut chart
    gen_capacity = pd.DataFrame(data.loc[data["Metric"] == "Capacity", "Optimal Value"][0:3]).reset_index(drop=True)
    gen_capacity_label = pd.DataFrame(data.loc[data["Metric"] == "Capacity", "Technology"][0:3]).reset_index(drop=True)
    sto_capacity = pd.DataFrame(data.loc[data["Metric"] == "Average power capacity", "Optimal Value"][0:4]).reset_index(drop=True)
    sto_capacity_label = pd.DataFrame(data.loc[data["Metric"] == "Average power capacity", "Technology"][0:4]).reset_index(drop=True)
    sto_capacity_label_strings = [str(label) for label in sto_capacity_label['Technology']]

    capacity = pd.concat([gen_capacity, sto_capacity])
    capacity_labels = pd.concat([gen_capacity_label, sto_capacity_label])
    capacity_n_labels = pd.concat([capacity_labels, capacity], axis=1)


    capacity_filtered = capacity_n_labels[capacity_n_labels['Optimal Value'] > 0]
    return capacity_filtered, sto_capacity_label_strings

def plot_capacity_donut(
    capacity_filtered: pd.DataFrame,
    #capacity_labels: pd.DataFrame,
    colors: list,
    total_capacity: float,
    case_name : str,
    folder_path : str = "results_plots",
):
    current_folder = os.getcwd()
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(capacity_filtered['Optimal Value'], 
        #labels=capacity_labels['Technology'], 
        startangle=90, colors = colors, autopct='%1.1f%%', pctdistance=0.8,  textprops={'fontsize': 20, 'fontweight':'bold','color':'black'})

    # Draw a circle at the center to create the donut effect
    centre_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    # Ensure the circle is a circle
    ax.axis('equal')

    # Display the chart
    plt.title('Capacity per technology (MW)', y = 0.95, fontsize = 28)
    legend = plt.legend(capacity_filtered['Technology'], bbox_to_anchor=(1.15, 0.9), loc="upper right", frameon=False, fontsize = 20, labelcolor='black')

    centre_text = f'{total_capacity}GW'
    centre_text_line_2 = f'Total Capacity'
    ax.text(0,0.1, centre_text, horizontalalignment='center', 
                verticalalignment='center', 
                fontsize=32, fontweight='bold',
                color='black')
    ax.text(0,-0.1, centre_text_line_2, horizontalalignment='center', 
                verticalalignment='center', 
                fontsize=30, fontweight='bold',
                color='black')
    plt.tight_layout() # Adjust layout to prevent labels from overlapping
    check_folder_and_create(current_folder, folder_path)
    plt.savefig(os.path.join(current_folder, folder_path, f'{case_name}_Capacity_per_tech.png'), dpi=1000)
    plt.show()
    return ax


# ---------------------------
# ------ HEAT MAP FUNCT -----
# ---------------------------

def get_vre_results( original_df : pd.DataFrame ) -> pd.DataFrame:
    df = pd.DataFrame()
    df[['Scenario', 'Hour']] = original_df[['Scenario', 'Hour']]
    df['VRE Generation (MW)'] = original_df['Solar PV Generation (MW)'] + original_df['Wind Generation (MW)']
    df['VRE Curtailment (MW)'] = original_df['Solar PV Curtailment (MW)'] + original_df['Wind Curtailment (MW)']
    processed_cols = ['Scenario', 'Hour', 'Solar PV Generation (MW)', 'Wind Generation (MW)', 'Solar PV Curtailment (MW)', 'Wind Curtailment (MW)']
    remaining_cols = [col for col in original_df.columns if col not in processed_cols]
    df[remaining_cols] = original_df[remaining_cols]

    return df


def plot_heatmap(
    results : pd.DataFrame,
    col_name : str,
    case_name : str,
    folder_path : str = "results_plots",
    color_map = "viridis",
    start_date = '2025-01-01 00:00:00'
):
    current_folder = os.getcwd()

    n_periods = len(results)
    hours = np.arange(1, n_periods+1)
    # Create the DataFrame with the hours
    df = pd.DataFrame(data=hours, columns=["Hour of the Year"])
    # Create a DatetimeIndex for a year (assuming the data starts at the beginning of the year)
    datetime_index = pd.date_range(start=start_date, periods=n_periods, freq='h')
    # Assign the DatetimeIndex to the DataFrame
    df['timestamp'] = datetime_index

    # Extract day of year and hour of day
    df['day_of_year'] = df['timestamp'].dt.dayofyear
    df['hour_of_day'] = df['timestamp'].dt.hour

    reshaped_data = results[col_name].values.reshape(24, len(df['day_of_year'].unique()), order="F")
    # # The first + 1 increases the length
    # # The outer + 1 ensures days start at 1, and not at 0.
    last_day_in_data = df['day_of_year'].max()
    xgrid = np.arange(last_day_in_data + 1) + 1
    # # Hours start at 0, length 2
    ygrid = np.arange(25)

    fig, ax = plt.subplots(figsize=(12,10))

    heatmap = ax.pcolormesh(xgrid, ygrid, reshaped_data, cmap = color_map)
    ax.set_xticklabels(ax.get_xmajorticklabels(), fontsize=16) 
    ax.set_yticklabels(ax.get_ymajorticklabels(), fontsize=16)
    ax.set_frame_on(False) # remove all spines
    
    plt.xlim(0, last_day_in_data)
    plt.ylim(0,24)

    cbar = plt.colorbar(heatmap)
    cbar.ax.tick_params(labelsize=16)

    plt.xlabel("Day of the year", fontsize = 20)
    plt.ylabel("Hour of the day", fontsize = 20)
    plt.title(col_name, y=1.05, fontsize = 20)
    case_name_file = case_name.replace("/","_")
    col_name_file = col_name.replace("/","_")
    check_folder_and_create(current_folder, folder_path)
    plt.savefig(os.path.join(current_folder, folder_path, f'{case_name_file}_{col_name_file}.png'), dpi=1000)
    plt.show()
    return ax