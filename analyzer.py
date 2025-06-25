import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse



#A CLI tool to give descriptive statistics of a given CSV file.


def analyze_csv(file_path,columns=None):
    try:
        df=pd.read_csv(file_path)
        print(f"Analyzing {file_path}..."
              )
        if columns:
            for col in columns:
                if col in df.columns:
                    print(f"Descriptive statistics for column '{col}':")
                    series= df[col]
                    if pd.api.types.is_numeric_dtype(series):
                        cleaned_series = series.dropna()
                        print(f"Mean: {cleaned_series.mean()}")
                        print(f"Median: {cleaned_series.median()}")
                        print(f"Standard Deviation: {cleaned_series.std()}")
                        print(f"Minimum: {cleaned_series.min()}")
                        print(f"Maximum: {cleaned_series.max()}")
                        print(f"Count: {cleaned_series.count()}")
                    else:
                        print(f"Column '{col}' is not numeric. Skipping statistics.")
                else:
                    print(f"Column '{col}' not found in the DataFrame.")
        else:
            print("No specific columns provided. Analyzing all numeric columns.")
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                print(f"Descriptive statistics for column '{col}':")
                series = df[col]
                cleaned_series = series.dropna()
                print(f"Mean: {cleaned_series.mean()}")
                print(f"Median: {cleaned_series.median()}")
                print(f"Standard Deviation: {cleaned_series.std()}")
                print(f"Minimum: {cleaned_series.min()}")
                print(f"Maximum: {cleaned_series.max()}")
                print(f"Count: {cleaned_series.count()}")
    
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    


def parser_setup():
    parser = argparse.ArgumentParser(description="Analyze a CSV file and provide descriptive statistics."
                                     )
    parser.add_argument("--filepath", type=str, required=True,
                        help="Path to the CSV file to analyze.")
    parser.add_argument("-c", "--columns", nargs='+',example=['column1', 'column2'],
                        help="List of specific columns to analyze. If not provided, all numeric columns will be analyzed.")
    
    
    return parser.parse_args()



if __name__ == "__main__":
    args = parser_setup()
    analyze_csv(args.filepath,args.columns)
    print("Analysis complete.")
        