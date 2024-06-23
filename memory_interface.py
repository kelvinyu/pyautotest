# memory_interface.py
import mmap
import os
import struct
import subprocess

class MemoryInterface:
    def write_memory(self, address, value, size):
        raise NotImplementedError
    
    def read_memory(self, address, size):
        raise NotImplementedError

class PCIBARMemory(MemoryInterface):
    def __init__(self, pci_device, bar_size):
        self.bar_address = self.get_pcie_bar_address(pci_device)
        self.mem = self.map_pcie_bar(self.bar_address, bar_size)

    def get_pcie_bar_address(self, pci_device):
        # 获取PCIe BAR地址的示例实现
        bar_address = 0x20000000  # 示例地址
        return bar_address

    def map_pcie_bar(self, bar_address, size):
        fd = os.open("/dev/mem", os.O_RDWR | os.O_SYNC)
        mem = mmap.mmap(fd, size, mmap.MAP_SHARED, mmap.PROT_WRITE | mmap.PROT_READ, offset=bar_address)
        os.close(fd)
        return mem

    def write_memory(self, address, value, size):
        if size == 4:
            self.mem[address:address+size] = struct.pack('I', value)
        elif size == 8:
            self.mem[address:address+size] = struct.pack('Q', value)
        else:
            raise ValueError("Unsupported size")

    def read_memory(self, address, size):
        if size == 4:
            return struct.unpack('I', self.mem[address:address+size])[0]
        elif size == 8:
            return struct.unpack('Q', self.mem[address:address+size])[0]
        else:
            raise ValueError("Unsupported size")

    def close(self):
        self.mem.close()

class HostMemory(MemoryInterface):
    def write_memory(self, address, value, size):
        gdb_command = f"set *(uint{size * 8}_t*){address} = {value}"
        result = subprocess.run(['gdb', '-ex', gdb_command, '-ex', 'quit'], capture_output=True, text=True)
        if result.stderr:
            raise RuntimeError(result.stderr)
    
    def read_memory(self, address, size):
        gdb_command = f"x/{size}bx {address}"
        result = subprocess.run(['gdb', '-ex', gdb_command, '-ex', 'quit'], capture_output=True, text=True)
        if result.stderr:
            raise RuntimeError(result.stderr)
        return int(result.stdout.strip(), 16)
