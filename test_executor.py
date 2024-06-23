# test_executor.py
import threading
import time
import queue
from openocd_interface import call_host_tool

EXPECTED_VALUE = 0  # 根据实际情况设置预期值

def write_to_sq(fifo, memory, base_address, stop_event):
    address_offset = 0
    while not stop_event.is_set():
        if not fifo.empty():
            data = fifo.get()
            address = base_address + address_offset
            memory.write_memory(address, data['value'], data['size'])
            print(f"Successfully wrote {data['value']} to SQ at address {hex(address)}")
            address_offset += data['size']
        time.sleep(0.1)  # 控制写入频率

def poll_cq(memory, address, size, stop_event):
    while not stop_event.is_set():
        result = memory.read_memory(address, size)
        print(f"Polled result from CQ: {result}")
        if result == EXPECTED_VALUE:
            stop_event.set()
        time.sleep(1)  # 每秒轮询一次

def execute_test(test, memory, base_memory_address, sq_address, cq_address):
    struct_name = test['parameter']
    struct_members = test['struct_members']
    
    # 初始化FIFO队列
    fifo = queue.Queue()

    for member in struct_members:
        member_type, member_name = member
        member_size = test['member_sizes'][member_name]
        member_value = int(test.get(member_name, 0))
        
        fifo.put({'value': member_value, 'size': member_size})

    stop_event = threading.Event()

    # 启动写入SQ线程
    write_thread = threading.Thread(target=write_to_sq, args=(fifo, memory, sq_address, stop_event))
    write_thread.start()

    # 启动轮询CQ线程
    poll_thread = threading.Thread(target=poll_cq, args=(memory, cq_address, 4, stop_event))
    poll_thread.start()

    # 启动定时器
    timeout = test['timeout']
    timer = threading.Timer(timeout, lambda: stop_event.set())
    timer.start()

    # 如果需要，调用主机工具
    if 'host_command' in test:
        stdout, stderr = call_host_tool(test['host_command'])
        if stderr:
            print(f"Error calling host tool: {stderr}")
        else:
            print(f"Host tool output: {stdout}")

    # 等待定时器或轮询线程完成
    timer.join()
    stop_event.set()
    write_thread.join()
    poll_thread.join()

    print(f"Test {test['testid']} completed.")
