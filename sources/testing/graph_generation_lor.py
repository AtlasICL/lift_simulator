import os
import ast
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns


DATA_FOLDER_PATH = os.path.join("results", "data", "lor_data")
DATA_FILENAME = "lor_with_constants.csv"


# Set a clean, publication-quality style for the plots
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

def plot_avg_lor(file_path, output_file):
    """
    Reads a CSV file that contains simulation data with string-encoded lists
    for the 'lor' and 'visited_floors' columns. It computes the average LOR per
    simulation and generates a scatter plot with a linear trend line.

    Parameters:
        file_path (str): Path to the CSV file.
        output_file (str): Filename to save the resulting plot.
    """
    # Read the CSV file and convert the 'lor' and 'visited_floors' columns into lists
    df = pd.read_csv(file_path, converters={
        "lor": ast.literal_eval,
        "visited_floors": ast.literal_eval
    })
    
    # Compute the average LOR for each simulation
    df['avg_lor'] = df['lor'].apply(np.mean)
    
    # Create a new figure for the plot
    plt.figure(figsize=(10, 6))
    
    # Plot a scatter plot of Simulation vs Average LOR
    sns.scatterplot(x='simulation', y='avg_lor', data=df, s=100, color="blue", label="Avg LOR")
    
    # Sort the DataFrame by simulation for a smooth trend line
    sorted_df = df.sort_values(by='simulation')
    x = sorted_df['simulation']
    y = sorted_df['avg_lor']
    
    # Compute a linear regression trend line using numpy.polyfit
    coefficients = np.polyfit(x, y, 1)  # linear fit
    poly_eqn = np.poly1d(coefficients)
    y_fit = poly_eqn(x)
    
    # Plot the trend line
    plt.plot(x, y_fit, color="red", linestyle="--", label="Trend line")
    
    # Set plot title and axis labels
    plt.title("Average LOR vs. Simulation")
    plt.xlabel("Simulation")
    plt.ylabel("Average LOR")
    plt.legend()
    plt.tight_layout()
    
    # Save the plot to a file and close the figure
    plt.savefig(output_file)
    plt.close()

def main():
    file_path = os.path.join(DATA_FOLDER_PATH, DATA_FILENAME)
    output_file = "avg_lor_graph.png"
    
    plot_avg_lor(file_path, output_file)
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    main()
