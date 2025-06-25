import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os


#A CLI tool to give descriptive statistics of a given CSV file.


def analyze_csv(file_path,columns=None,output_plot_dir=None,requested_stats=None):
    """Analyze a CSV file and print descriptive statistics for specified columns.
    args:
     file_path (str): Path to the CSV file to be analyzed.
     columns (list, optional): List of column names to analyze. If None, all numeric columns will be analyzed.
     output_plot_dir (str, optional): Directory to save histograms. If None, histograms will not be saved.
     requested_stats (list, optional): List of statistics to compute. Default is ['mean', 'median', 'std', 'min', 'max', 'count'].
     
     Functions of  the script:
     - Reads a CSV file into a pandas DataFrame.
     - Analyzes specified columns or all numeric columns if none are specified.
     - Computes and prints descriptive statistics for each column.
     - Generates and saves histograms for each analyzed column if an output directory is provided.
     - Computes and prints a correlation matrix for the analyzed columns.
     - Handles various exceptions related to file reading and data processing."""
    try:
        df=pd.read_csv(file_path)
        analyzed_columns=[]
        if output_plot_dir:
            try:
                os.makedirs(output_plot_dir, exist_ok=True)
                print(f"Histograms will be saved to: {output_plot_dir}")
            except OSError as e:
                print(f"Error: Could not create output directory '{output_plot_dir}': {e}. Histograms will not be saved.")
                output_plot_dir = None
        print(f"Analyzing {file_path}...")
        if columns:
            for col in columns:
                if col in df.columns:
                    series= df[col]
                    if pd.api.types.is_numeric_dtype(series):
                        cleaned_series = series.dropna()
                        if cleaned_series.empty:
                            print(f"Column '{col}' is empty after dropping NaN values. No statistics to display.")
                        else:
                            
                            print_stats(cleaned_series,col,requested_stats)
                            analyzed_columns.append(col) 
                            if output_plot_dir:
                                generate_histogram(cleaned_series, col, output_plot_dir,)
                                
                        
                    else:
                        print(f"Column '{col}' is not numeric. Skipping statistics.")
                        handling_categorical(series)
                        print("-" * 40)
                else:
                    print(f"Column '{col}' not found in the DataFrame.")
        else:
            print("No specific columns provided. Analyzing all numeric columns.")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                series = df[col]
                cleaned_series = series.dropna()
                if cleaned_series.empty:
                    print(f"Column '{col}' is empty after dropping NaN values. No statistics to display.")
                else: 
                    print_stats(cleaned_series,col,requested_stats)
                    analyzed_columns.append(col) 
        if len(analyzed_columns)>1:
            print("\n Correlation matrix for analyzed columns:")
            print('-' * 40)
            correlation_matrix = df[analyzed_columns].corr()
            print(correlation_matrix)
            print('-' * 40)
        elif len(analyzed_columns) == 1:
            print(f"\nOnly one column '{analyzed_columns[0]}' was analyzed. No correlation matrix to display.")
        else:
            print("No numeric columns were analyzed. No correlation matrix to display.")
        
        return True
    
    
    except FileNotFoundError:
        print(f"File {file_path} not found. Please check the path and try again.")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"File {file_path} is empty. Please provide a valid CSV file.")
        sys.exit(1)
    except pd.errors.ParserError:
        print(f"Error parsing the file {file_path}. Please ensure it is a valid CSV file.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        sys.exit(1)
    




def print_stats(series,column_name,stats_to_compute):
    """Print descriptive statistics for a given pandas Series.
    args:
        series (pd.Series): The pandas Series containing numeric data.
        column_name (str): The name of the column for labeling the statistics.
        stats_to_compute (list): List of statistics to compute. Default is ['mean', 'median', 'std', 'min', 'max', 'count'].
    """
    if series.empty:
        print("Series is empty. No statistics to display.")
        return
    print(f"Descriptive statistics for column '{column_name}':")
    available_calculations = {
        'mean': lambda s: f"  Mean: {s.mean():.2f}",
        'median': lambda s: f"  Median: {s.median():.2f}",
        'std': lambda s: f"  Standard Deviation: {s.std():.2f}",
        'min': lambda s: f"  Minimum: {s.min():.2f}",
        'max': lambda s: f"  Maximum: {s.max():.2f}",
        'count': lambda s: f"  Count: {s.count()}"
    }
    for stat in stats_to_compute:
        if stat in available_calculations:
            try:
                print(available_calculations[stat](series))
            except Exception as e:
                print(f"Error calculating {stat} for column '{column_name}': {e}")
        else:
            print(f"Statistic '{stat}' is not recognized. Available options are: {', '.join(available_calculations.keys())}")
    print("-" * 40)







def generate_histogram(series, col, output_dir):
    """Generate and save a histogram for the given series.
    args:
        series (pd.Series): The pandas Series containing numeric data.
        col (str): The name of the column for labeling the histogram.
        output_dir (str): The directory where the histogram will be saved.
    """
    plot_name=os.path.join(output_dir, f"{col}_histogram.png")
    plt.figure(figsize=(10, 6))
    plt.hist(series, bins=30, color='blue', alpha=0.7)
    plt.title(f"Histogram of {col}")
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.grid(axis='y', alpha=0.75)
    try:
        plt.savefig(plot_name)
        print(f"Histogram for column '{col}' saved as {plot_name}.")
    except Exception as e:
        print(f"Error saving histogram for column '{col}': {e}")
    finally:
        plt.close()


def handling_categorical(series):
    """Handle categorical data by displaying value counts.
    args:
        series (pd.Series): The pandas Series containing categorical data.
    """
    if series.empty:
        print("Series is empty. No value counts to display.")
        return
    cleaned_series = series.dropna()
    if cleaned_series.empty:
        print("Series is empty after dropping NaN values. No value counts to display.")
        return
    value_counts = cleaned_series.value_counts()
    if value_counts.empty:
        print("Series is empty. No value counts to display.")
    else:
        print(f"Value counts for categorical data:")
        print(value_counts)
        print("-" * 40)


def parser_setup():
    """Set up the command line argument parser.
    """
    parser = argparse.ArgumentParser(description="Analyze a CSV file and provide descriptive statistics."
                                     )
    parser.add_argument("--filepath", type=str, required=True,
                        help="Path to the CSV file to analyze.")
    parser.add_argument("-c", "--columns", nargs='+',
                        help="List of specific columns to analyze. (example=['column1', 'column2']), If not provided, all numeric columns will be analyzed.")
    parser.add_argument("-op","--output_plot_dir",type=str,default=None,
                        help="Directory path to save generated histograms. If provided, histograms will be created for numerically analyzed columns.")
    parser.add_argument("--stats",nargs='+', choices=['mean', 'median', 'std', 'min', 'max', 'count'],default=['mean', 'median', 'std', 'min', 'max', 'count'],
                        help="List of descriptive statistics to display. Default is all statistics (mean, median, std, min, max, count).")
    return parser.parse_args()



if __name__ == "__main__":
    args = parser_setup()
    if analyze_csv(args.filepath,args.columns,args.output_plot_dir,args.choices): 
        print("Analysis completed successfully.")
    
        