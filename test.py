import csv

def parse_cores_data(cores_data_str):
    cores_data = {}
    core_entries = cores_data_str.split(';')
    for entry in core_entries:
        if ':' in entry:
            core_id, data_str = entry.split(':')
            data = list(map(int, data_str.split(',')))
            cores_data[int(core_id)] = data
    return cores_data

def read_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            testname = row['testname']
            testid = row['testid']
            cores_data_str = row['cores_data'].strip('"')
            cores_data = parse_cores_data(cores_data_str)
            host_command = row['host_command'].strip('"')
            host_scripts = row['host_scripts'].strip('"')
            process_test_data(testname, testid, cores_data, host_command, host_scripts)

def process_test_data(testname, testid, cores_data, host_command, host_scripts):
    # Implement the logic to process test data for each core, host command, and host scripts
    print(f"Processing Test: {testname} (ID: {testid})")
    for core, data in cores_data.items():
        print(f"Core {core}: {data}")
    print(f"Host Command: {host_command}")
    print(f"Host Scripts: {host_scripts}")

# Example usage
read_csv('test.csv')
