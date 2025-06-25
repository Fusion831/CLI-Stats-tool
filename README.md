
# CSV Statistical Analysis CLI Tool

A Python command-line tool designed to perform statistical analysis on CSV files. It offers descriptive statistics, optional histogram generation, pairwise correlation matrices for numerical data, and value counts for categorical data.

## Features

* **CSV Parsing:** Reads and processes data from specified CSV files.
* **Descriptive Statistics:** Calculates mean, median, standard deviation, minimum, maximum, and count for:
  * User-specified numerical columns.
  * All numerical columns by default if none are specified.
* **Customizable Statistics:** Users can specify which statistics to display (e.g., only mean and count).
* **Missing Data Handling:** Gracefully handles missing values (NaNs) by dropping them before calculations for the respective column.
* **Histogram Generation:** Optionally generates and saves histograms as PNG files for each numerically analyzed column to a user-specified directory.
* **Correlation Matrix:** Computes and displays a pairwise correlation matrix if multiple numerical columns are analyzed.
* **Categorical Data Analysis:** Identifies categorical columns (typically 'object' dtype) and prints their unique value counts.
* **Robust Error Handling:** Includes error management for issues like file not found, empty or malformed CSVs, and invalid column names.
* **Command-Line Interface:** Easy-to-use CLI built with Python's `argparse` module.

## Tech Stack

* Python (3.8+)
* Pandas
* NumPy (installed as a dependency of Pandas)
* Matplotlib
* argparse (Python Standard Library)

## Prerequisites

Before running the tool, ensure you have the following installed:

* Python 3.8 or higher.
* The Python package manager `pip`.

## Installation

1. **Clone the repository (or download the `analyzer.py` script):**

    ```bash
    git clone <your-repository-url>
    cd <repository-name>
    ```

    *(Replace `<your-repository-url>` and `<repository-name>` with your actual repository details if you are cloning. If you downloaded the script, navigate to its directory.)*

2. **Install dependencies:**

    **Option 1: Using `requirements.txt` (Recommended)**

    If a `requirements.txt` file is provided in the repository (you may need to create this):

    ```bash
    pip install -r requirements.txt
    ```

    *To create a `requirements.txt` file from your current environment, you can run:*

    ```bash
    pip freeze > requirements.txt
    ```

    *(Ensure your environment only contains the necessary packages for this project before running `pip freeze`.)*

    **Option 2: Manual Installation**

    If you prefer to install packages manually, or if `requirements.txt` is not available:

    ```bash
    pip install pandas matplotlib numpy
    ```

    *(Note: NumPy is usually installed automatically as a dependency of Pandas.)*

## Usage

The script `analyzer.py` is executed from the command line.

**Core Syntax:**

```bash
python analyzer.py --filepath <path_to_your_csv_file> [options]
```

**Available Options:**

* `--filepath FILEPATH` (Required): Path to the input CSV file.
* `-c COLUMNS [COLUMNS ...], --columns COLUMNS [COLUMNS ...]`: List of specific column names to analyze. If not provided, all numerical columns (and categorical columns for value counts if processing all) will be analyzed.
* `-op OUTPUT_PLOT_DIR, --output_plot_dir OUTPUT_PLOT_DIR`: Directory path to save generated histograms. Histograms are created for numerically analyzed columns if this option is provided.
* `--stats {mean,median,std,min,max,count} [{mean,median,std,min,max,count} ...]`: List of specific descriptive statistics to display. Default is all statistics (mean, median, std, min, max, count).

**Examples:**

1. **Analyze all numerical and categorical columns in `data.csv` and display all standard statistics:**

    ```bash
    python analyzer.py --filepath data.csv
    ```

2. **Analyze specific columns (`Age`, `Salary`, `Department`) from `employees.csv`, display all statistics, and save histograms to a folder named `plots`:**

    ```bash
    python analyzer.py --filepath employees.csv --columns Age Salary Department --output_plot_dir ./plots
    ```

3. **Analyze the `Score` column from `results.csv` and display only the mean and count:**

    ```bash
    python analyzer.py --filepath results.csv --columns Score --stats mean count
    ```

4. **Analyze all numerical columns in `sensor_data.csv` and save histograms to `output_histograms`, displaying all statistics:**

    ```bash
    python analyzer.py --filepath sensor_data.csv --output_plot_dir output_histograms
    ```

## Error Handling

The tool includes error handling for:

* File not found at the specified path.
* Empty CSV files.
* Malformed CSV files (parsing errors).
* Specified column names not existing in the CSV.
* Attempts to perform numerical statistics on non-numerical columns (these are skipped for stats, or value counts are shown if categorical).

In case of critical errors like file issues, the script will print an error message and exit.

## Future Enhancements / To-Do

* Implement comprehensive unit tests using the `unittest` module to ensure code reliability and facilitate easier refactoring.
* Allow more advanced configuration for histogram bins and appearance.
* Option to output statistical results to a file (e.g., CSV, JSON, TXT) in addition to console display.
