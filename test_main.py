import threading
import json
import csv
from datetime import datetime
import time
from csv_parser import read_csv
from c_header_parser import parse_header, get_member_size
from openocd_interface import run_openocd
from memory_interface import PCIBARMemory, HostMemory

def load_config(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
    return config

def record_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        result['execution_time'] = execution_time
        return result
    return wrapper

def run_test_case(test, memory, base_memory_address, sq_address, cq_address, host_tool_path):
    # Placeholder function for actual test execution logic
    # This example just simulates a test with a sleep
    time.sleep(1)  # Simulate test execution time

    # Generate mock test result
    success = True  # Replace with actual test logic
    test['success'] = success

    # Simulate host tool command
    test['host_command'] = f"{host_tool_path} {test['host_command']}"

    return test

def generate_report(test_results, report_filename):
    with open(report_filename, 'w', newline='') as csvfile:
        fieldnames = ['Test ID', 'Execution Time (s)', 'Result']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in test_results:
            writer.writerow({
                'Test ID': result['testid'],
                'Execution Time (s)': result['execution_time'],
                'Result': 'Pass' if result['success'] else 'Fail'
            })

def main():
    # Load configuration from JSON file
    config = load_config('config/config.json')

    # Parse header file
    header_data = parse_header('headers/example.h')

    # Initialize memory interface based on config
    if config['memory_type'] == 'pcie_bar':
        memory = PCIBARMemory(config['pci_device'], config['bar_size'])
    elif config['memory_type'] == 'host_memory':
        memory = HostMemory()
    else:
        raise ValueError("Unsupported memory type")

    # Define fixed memory addresses
    base_memory_address = config['base_memory_address']
    sq_address = config['sq_address']
    cq_address = config['cq_address']

    # Read all CSV files and prepare tests
    all_tests = []
    for csv_path in config['csv_paths']:
        tests = read_csv(csv_path)
        all_tests.extend(tests)

    # Execute tests and update report dynamically
    test_results = []
    for test in all_tests:
        test_result = run_test_case(test, memory, base_memory_address, sq_address, cq_address, config['host_tool_path'])
        test_results.append(test_result)
        generate_report(test_results, 'test_report.csv')

    # Call OpenOCD to download program
    stdout, stderr = run_openocd('path_to_openocd_script.cfg')
    if stderr:
        print(f"Error: {stderr}")
    else:
        print(f"Output: {stdout}")

    # Close memory mapping
    if isinstance(memory, PCIBARMemory):
        memory.close()

if __name__ == "__main__":
    main()
