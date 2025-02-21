import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean, publication-quality style for the plots
sns.set(style="whitegrid", palette="muted", font_scale=1.2)

def plot_exponential_trend(file_path, x_col, y_col, x_label, title, output_file):
    """
    Reads a CSV file and plots a scatter plot of y_col vs x_col, 
    fitting an exponential trendline (y = a * exp(b*x)).
    
    Parameters:
        file_path (str): Path to the CSV file.
        x_col (str): Column name for the x-axis (Capacity).
        y_col (str): Column name for the y-axis (TTSW).
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
    
    # Sort the DataFrame by the x_col for a smooth trendline curve
    sorted_df = df.sort_values(by=x_col)
    x = sorted_df[x_col]
    y = sorted_df[y_col]
    
    # Fit an exponential model: y = a * exp(b * x)
    # Taking logarithms: log(y) = log(a) + b * x, so we can use a linear fit on (x, log(y))
    coefficients = np.polyfit(x, np.log(y), 1)  # Returns [b, log(a)]
    b = coefficients[0]
    a = np.exp(coefficients[1])
    y_fit = a * np.exp(b * x)
    
    # Plot the exponential trendline
    plt.plot(x, y_fit, color="red", linestyle="--", label="Exponential Trendline")
    
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
    # Define file paths (adjust folder paths as needed)
    file_path = os.path.join("results", "data", "ttsw_data", "ttsw_vs_capacity.csv")
    output_file = os.path.join("results", "charts", "ttsw_vs_capacity_exponential.png")
    
    plot_exponential_trend(
        file_path=file_path,
        x_col="Capacity",
        y_col="TTSW",
        x_label="Capacity",
        title="Lift Simulation Performance (TTSW) vs Capacity\n(Exponential Trend)",
        output_file=output_file
    )
    print(f"Graph saved to {output_file}")

if __name__ == "__main__":
    main()
