###########################################
# Random CSV Dummy Data Generator
# By @Amit Barman
###########################################
import csv
import random
import json
import argparse

class DataGenerator(object):
    file_name = ''
    data_count = None
    outfile_name = ''

    def __init__(self, file_name, data_count):
        self.file_name = file_name
        self.data_count = data_count
        self.outfile_name = f'dummy_data_{data_count}_row.csv'

    # Read json file
    def read_source(self, file_name: str) -> dict:
        try:
            with open(file_name, 'r') as source:
                source_data = json.load(source)
            return source_data
        except Exception as e:
            pass

    # Function to generate random data
    def generate_random_data(self) -> dict:
        try:
            json_data = self.read_source(self.file_name)
            return_dict = {}
            for key, val in json_data.items():
                if type(val) == int or type(val) == str:
                    return_dict[key] = val
                elif type(val) == list and len(val) > 0:
                    if len(val) == 2 and type(val[0]) == int:
                        return_dict[key] = random.randint(val[0], val[1])
                    else:
                        return_dict[key] = random.choice(val)
                else:
                    pass
            return return_dict
        except Exception as e:
            pass

    # Create and write to CSV file
    def write_csv(self) -> None:
        try:
            with open(self.outfile_name, 'w', newline='') as csvfile:
                fieldnames = list(self.read_source(self.file_name).keys())
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()

                # Generate and write random records
                for _ in range(self.data_count):
                    data = self.generate_random_data()
                    writer.writerow(data)
            print(f'[+] {self.data_count} Row of Dummy data written to {self.outfile_name}')
        except Exception as e:
            pass

# Main Block
if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-s', '--source', type=str, required=True, dest='source', metavar=None, help='json source name')
    parser.add_argument('-c', '--count', type=int, metavar=None, dest='count', default=10, help='number of rows you want to generae')

    args = parser.parse_args()

    if (args.source).endswith('.json'):
        DataGenerator(args.source, args.count).write_csv()
    else:
        parser.error("invalid file type")