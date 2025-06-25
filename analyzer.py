import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys
import os


#A CLI tool to give descriptive statistics of a given CSV file.


def analyze_csv(file_path,columns=None,output_plot_dir=None):
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
                            
                            print_stats(cleaned_series,col)
                            analyzed_columns.append(col) 
                            if args.output_plot_dir:
                                os.makedirs(args.output_plot_dir, exist_ok=True)
                                plot_name=os.path.join(args.output_plot_dir, f"{col}_histogram.png")
                                plt.figure(figsize=(10, 6))
                                plt.hist(cleaned_series, bins=30, color='blue', alpha=0.7)
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
                                
                        
                    else:
                        print(f"Column '{col}' is not numeric. Skipping statistics.")
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
                    print_stats(cleaned_series,col)
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
    
def print_stats(series,column_name):
    if series.empty:
        print("Series is empty. No statistics to display.")
        return
    print(f"Descriptive statistics for column '{column_name}':")
    print(f"Mean: {series.mean():.2f}")
    print(f"Median: {series.median():.2f}")
    print(f"Standard Deviation: {series.std():.2f}")
    print(f"Minimum: {series.min():.2f}")
    print(f"Maximum: {series.max():.2f}")
    print(f"Count: {series.count()}")
    print("-" * 40)
    

def parser_setup():
    parser = argparse.ArgumentParser(description="Analyze a CSV file and provide descriptive statistics."
                                     )
    parser.add_argument("--filepath", type=str, required=True,
                        help="Path to the CSV file to analyze.")
    parser.add_argument("-c", "--columns", nargs='+',
                        help="List of specific columns to analyze. (example=['column1', 'column2']), If not provided, all numeric columns will be analyzed.")
    parser.add_argument("-op","--output_plot_dir",type=str,default=None,
                        help="Directory path to save generated histograms. If provided, histograms will be created for numerically analyzed columns.")
    
    return parser.parse_args()



if __name__ == "__main__":
    args = parser_setup()
    if analyze_csv(args.filepath,args.columns,args.output_plot_dir): 
        print("Analysis completed successfully.")
    
        