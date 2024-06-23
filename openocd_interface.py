# openocd_interface.py
import subprocess

def run_openocd(script_path):
    result = subprocess.run(['openocd', '-f', script_path], capture_output=True, text=True)
    return result.stdout, result.stderr

def write_memory(address, value, size):
    gdb_command = f"set *(uint{size * 8}_t*){address} = {value}"
    result = subprocess.run(['gdb', '-ex', gdb_command, '-ex', 'quit'], capture_output=True, text=True)
    return result.stdout, result.stderr

def read_memory(address, size):
    gdb_command = f"x/{size}bx {address}"
    result = subprocess.run(['gdb', '-ex', gdb_command, '-ex', 'quit'], capture_output=True, text=True)
    return result.stdout, result.stderr

def call_host_tool(command):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout, result.stderr
