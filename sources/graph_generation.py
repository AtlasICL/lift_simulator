import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set a nice style for the plots
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

def plot_data(file_path, x_col, y_col, x_label, title, output_file):
    """
    Reads a CSV file and plots a scatter plot with a linear trend line.
    
    Parameters:
        file_path (str): Path to the CSV file.
        x_col (str): Name of the column for the x-axis (the varied parameter).
        y_col (str): Name of the column for the y-axis (e.g., Moves).
        x_label (str): Label for the x-axis.
        title (str): Title of the graph.
        output_file (str): File name to save the plot.
    """
    # Read CSV file
    df = pd.read_csv(file_path)
    
    # Create a new figure
    plt.figure(figsize=(10, 6))
    
    # Scatter plot of the data
    sns.scatterplot(x=x_col, y=y_col, data=df, s=100, color="blue", label="Data Points")
    
    # To create a smooth trend line, sort the DataFrame by the x_col
    sorted_df = df.sort_values(by=x_col)
    x = sorted_df[x_col]
    y = sorted_df[y_col]
    
    # Compute a linear regression (trend line) using numpy
    coefficients = np.polyfit(x, y, 1)  # degree 1 for linear fit
    poly_eqn = np.poly1d(coefficients)
    y_fit = poly_eqn(x)
    
    # Plot the trend line
    plt.plot(x, y_fit, color="red", linestyle="--", label="Trend line")
    
    # Set title and labels
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_col)
    plt.legend()
    plt.tight_layout()
    
    # Save and show the plot
    plt.savefig(output_file)
    plt.show()

def main():
    # Graph for the CSV file where the number of requests is varied
    plot_data(
        file_path="num_requests.csv",
        x_col="Num Requests",
        y_col="Moves",
        x_label="Number of Requests",
        title="Lift Simulation Performance vs. Number of Requests",
        output_file="num_requests_graph.png"
    )
    
    # Graph for the CSV file where the total floors is varied
    plot_data(
        file_path="floors.csv",
        x_col="Total Floors",
        y_col="Moves",
        x_label="Total Floors",
        title="Lift Simulation Performance vs. Total Floors",
        output_file="floors_graph.png"
    )
    
    # Graph for the CSV file where the capacity is varied
    plot_data(
        file_path="capacity.csv",
        x_col="Capacity",
        y_col="Moves",
        x_label="Capacity",
        title="Lift Simulation Performance vs. Capacity",
        output_file="capacity_graph.png"
    )

if __name__ == "__main__":
    main()
