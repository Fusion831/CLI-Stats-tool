import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import sys



#A CLI tool to give descriptive statistics of a given CSV file.


def analyze_csv(file_path,columns=None):
    try:
        df=pd.read_csv(file_path)
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
    
    
    return parser.parse_args()



if __name__ == "__main__":
    args = parser_setup()
    if analyze_csv(args.filepath,args.columns): 
        print("Analysis completed successfully.")
    
        