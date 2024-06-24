import csv
import struct

HEADER_MAGIC = 0xDEADBEEF

def parse_cores_data(cores_data_str):
    cores_data = {}
    core_entries = cores_data_str.split(';')
    for entry in core_entries:
        if ':' in entry:
            core_id, data_str = entry.split(':')
            data = list(map(int, data_str.split(',')))
            cores_data[int(core_id)] = data
    return cores_data

def process_test_data(testid, cores_data):
    packed_data = []
    packed_data.append(HEADER_MAGIC)
    packed_data.append(testid)
    for core, data in cores_data.items():
        packed_data.append(core)
        for datum in data:
            packed_data.append(datum)
    return packed_data

def send_to_memory(data):
    # Example function - replace with your actual memory write function
    # Assuming data is a list of 32-bit integers
    for value in data:
        print(f"Writing 32-bit int to memory: {value}")
        # Write 'value' to memory or device here

def read_csv_and_send(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            testid = int(row['testid'])
            cores_data_str = row['cores_data'].strip('"')
            cores_data = parse_cores_data(cores_data_str)
            packed_data = process_test_data(testid, cores_data)
            send_to_memory(packed_data)

# Example usage
read_csv_and_send('test_data.csv')
