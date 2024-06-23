# pcie_interface.py
import mmap
import os
import struct

def get_pcie_bar_address(pci_device):
    # 假设从某个命令或配置文件中获取PCIe BAR地址
    # 这里只是示例，实际需要根据具体情况实现
    bar_address = 0x20000000  # 示例地址
    return bar_address

def map_pcie_bar(bar_address, size):
    fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
    mem = mmap.mmap(fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ, offset=bar_address)
    os.close(fd)
    return mem

def write_pcie_bar(mem, offset, value, size):
    if size == 4:
        mem[offset:offset+size] = struct.pack('I', value)
    elif size == 8:
        mem[offset:offset+size] = struct.pack('Q', value)
    # 添加更多类型及其大小
    else:
        raise ValueError("Unsupported size")

def read_pcie_bar(mem, offset, size):
    if size == 4:
        return struct.unpack('I', mem[offset:offset+size])[0]
    elif size == 8:
        return struct.unpack('Q', mem[offset:offset+size])[0]
    # 添加更多类型及其大小
    else:
        raise ValueError("Unsupported size")
