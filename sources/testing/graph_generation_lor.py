import os
import ast
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns


LOR_DATA_FILES = ["lor_with_constants.csv", "lor_vs_capacity.csv", "lor_vs_floors.csv", "lor_vs_requests.csv"]

WHICH_DATA: int = 3

DATA_FOLDER_PATH = os.path.join("results", "data", "lor_data")
DATA_FILENAME = LOR_DATA_FILES[WHICH_DATA]

OUTPUT_FILE = "results/charts/" + (LOR_DATA_FILES[WHICH_DATA]).removesuffix(".csv") + ".png"


# Set a clean, publication-quality style for the plots
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

def plot_avg_lor(file_path, output_file):
    # Read the CSV file and convert the 'lor' and 'visited_floors' columns into lists
    df = pd.read_csv(file_path, converters={
        "lor": ast.literal_eval,
        "visited_floors": ast.literal_eval
    })
    
    # Compute the average LOR for each simulation (THIS IS LOROT)
    df['avg_lor'] = df['lor'].apply(np.mean)
    
    plt.figure(figsize=(10, 6))
    
    sns.scatterplot(x='simulation', y='avg_lor', data=df, s=100, color="blue", label="Avg LOR")
    
 
    # UNCOMMENT IF YOU WANT TRENDLINE
    # sorted_df = df.sort_values(by='simulation')
    # x = sorted_df['simulation']
    # y = sorted_df['avg_lor']
    # coefficients = np.polyfit(x, y, 1)  # linear fit
    # poly_eqn = np.poly1d(coefficients)
    # y_fit = poly_eqn(x)
    # plt.plot(x, y_fit, color="red", linestyle="--", label="Trend line")
    
    plt.title("Average LOR vs. Simulation")
    plt.xlabel("Simulation")
    plt.ylabel("Average LOR")
    plt.legend()
    plt.tight_layout()
    
    plt.savefig(output_file)
    plt.close()

def main():
    file_path = os.path.join(DATA_FOLDER_PATH, DATA_FILENAME)
    
    plot_avg_lor(file_path, OUTPUT_FILE)
    print(f"Graph saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
