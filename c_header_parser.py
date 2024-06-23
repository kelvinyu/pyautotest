# c_header_parser.py
import re

def parse_header(file_path):
    parameters = {}
    with open(file_path, 'r') as file:
        content = file.read()
        struct_matches = re.findall(r'struct\s+(\w+)\s*{([^}]*)}', content)
        
        for struct in struct_matches:
            struct_name = struct[0]
            struct_body = struct[1]
            members = re.findall(r'\s*(\w+)\s+(\w+);', struct_body)
            parameters[struct_name] = members
            
    return parameters

def get_member_size(member_type):
    # 你可以根据具体情况扩展此字典，例如根据不同平台的实际情况
    size_map = {
        'int': 4,
        'float': 4,
        'double': 8,
        'char': 1
        # 添加更多类型及其大小
    }
    return size_map.get(member_type, 0)
