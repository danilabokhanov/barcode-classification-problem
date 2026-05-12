import platform
import psutil
import subprocess

def print_pc_info():
    lscpu_output = subprocess.check_output("lscpu | grep 'Model name'", shell=True)
    print(lscpu_output.decode())

    print("System:", platform.system())
    print("Node Name:", platform.node())
    print("Release:", platform.release())
    print("Version:", platform.version())
    print("Machine:", platform.machine())
    print("Processor:", platform.processor())
    print("CPU Cores (Physical):", psutil.cpu_count(logical=False))
    print("CPU Cores (Logical):", psutil.cpu_count(logical=True))
    print("CPU Frequency:", psutil.cpu_freq())

    ram = psutil.virtual_memory()
    print("Total RAM (GB):", ram.total / (1024**3))
    print("Available RAM (GB):", ram.available / (1024**3))

    disk = psutil.disk_usage('/')
    print("Disk Total (GB):", disk.total / (1024**3))
    print("Disk Used (GB):", disk.used / (1024**3))
    print("Disk Free (GB):", disk.free / (1024**3))
