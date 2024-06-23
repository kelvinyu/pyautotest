# csv_parser.py
import csv

def read_csv(file_path):
    tests = []
    with open(file_path, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            row['timeout'] = int(row['timeout'])  # 确保超时时间是整数
            tests.append(row)
    return tests
