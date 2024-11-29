import csv
import os

# CSV Import
# This reads in a CSV File containing two columns:
#  Date, Count
# Where Date is in YYYY-MM-DD format, and Count is an integer.
# The data is put into a dictionary.
# The dates must be in order, with the oldest date at the top.
# Between the first and last dates, if a date is missing from
# the range, it is added with a Count of 0. 
# This dictionary will be used for Monte Carlo simulations.
# The name of the CSV file is read from a configuration file.

data_dictionary = {}

def read_data_file(filename):
    data = {}
    """Reads the contents of the data file."""
    try:
        with open(filename, 'r') as file:
            csv_reader = csv.reader(file)

            for row in csv_reader:
                date, count = row
                data_dictionary[date] = int(count)
        return data_dictionary

    except FileNotFoundError:
        print(f"Error: The data file '{filename}' was not found.")
        return None
    except IOError as e:
        print(f"Error reading the data file '{filename}': {e}")
        return None

def main():

    data_filename = 'dates_and_counts.csv'
    print(f"Reading from {data_filename}")

    if data_filename:
        # Check if the data file exists before attempting to read
        if os.path.isfile(data_filename):
            # Read and print the contents of the data file
            data_content = read_data_file(data_filename)
            if data_content is not None:
                print("Contents of the data file:")
                print(data_content)
            else:
                print("Failed to read the data file.")
        else:
            print(f"Error: The data file '{data_filename}' does not exist.")
    else:
        print("Failed to read the configuration file.")


if __name__ == "__main__":
    main()

