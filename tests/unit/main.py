import argparse
import csv
import json
import logging
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments():
    """
    Parses command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Data parser for CSV and JSON files.")
    parser.add_argument("input_file", help="Path to the input file (CSV or JSON).")
    parser.add_argument("output_file", help="Path to the output file (JSON).")
    parser.add_argument("--log_level", default="INFO", choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Set the logging level.")
    return parser.parse_args()


def read_csv_file(input_file):
    """
    Reads a CSV file and returns a list of dictionaries.
    """
    data = []
    try:
        with open(input_file, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
        logging.info(f"Successfully read CSV file: {input_file}")
    except FileNotFoundError:
        logging.error(f"File not found: {input_file}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading CSV file: {input_file} - {e}")
        sys.exit(1)
    return data


def read_json_file(input_file):
    """
    Reads a JSON file and returns a list of dictionaries.
    """
    try:
        with open(input_file, 'r') as jsonfile:
            data = json.load(jsonfile)
        logging.info(f"Successfully read JSON file: {input_file}")
    except FileNotFoundError:
        logging.error(f"File not found: {input_file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON file: {input_file} - {e}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error reading JSON file: {input_file} - {e}")
        sys.exit(1)

    if not isinstance(data, list):
        logging.error(f"JSON file {input_file} does not contain a list.")
        sys.exit(1)

    return data


def write_json_file(data, output_file):
    """
    Writes data to a JSON file.
    """
    try:
        with open(output_file, 'w') as jsonfile:
            json.dump(data, jsonfile, indent=4)
        logging.info(f"Successfully wrote to JSON file: {output_file}")
    except Exception as e:
        logging.error(f"Error writing to JSON file: {output_file} - {e}")
        sys.exit(1)


def main():
    """
    Main function to parse data and write to a JSON file.
    """
    args = parse_arguments()

    # Set logging level
    logging.getLogger().setLevel(args.log_level.upper())

    input_file = args.input_file
    output_file = args.output_file

    _, file_extension = os.path.splitext(input_file)

    if file_extension.lower() == ".csv":
        data = read_csv_file(input_file)
    elif file_extension.lower() == ".json":
        data = read_json_file(input_file)
    else:
        logging.error("Unsupported file format. Only CSV and JSON files are supported.")
        sys.exit(1)

    write_json_file(data, output_file)


if __name__ == "__main__":
    main()