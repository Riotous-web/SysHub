import platform
import os
import psutil
import json
import win32api
import win32process
import socket
import time

def get_system_info():
    system_info = {}

    # OS Information
    system_info['os'] = {
        'name': platform.system(),
        'version': platform.version(),
        'release': platform.release(),
        'architecture': platform.architecture(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'platform': platform.platform(),
    }

    # User Information
    system_info['user'] = {
        'user_name': os.getlogin(),
        'home_dir': os.path.expanduser('~'),
        'hostname': socket.gethostname(),
        'ip_address': socket.gethostbyname(socket.gethostname())
    }

    # CPU Information
    system_info['cpu'] = {
        'cpu_count': psutil.cpu_count(logical=True),
        'cpu_physical_count': psutil.cpu_count(logical=False),
        'cpu_percent': psutil.cpu_percent(interval=1),
        'cpu_freq': psutil.cpu_freq()._asdict(),
        'cpu_times': psutil.cpu_times()._asdict(),
        'cpu_stats': psutil.cpu_stats()._asdict(),
    }

    # Memory Information
    memory_info = psutil.virtual_memory()._asdict()
    swap_info = psutil.swap_memory()._asdict()

    system_info['memory'] = {
        'virtual_memory': memory_info,
        'swap_memory': swap_info,
        'virtual_memory_percent': memory_info['percent'],
        'swap_memory_percent': swap_info['percent'],
    }

    # Disk Information
    disk_info = {
        'partitions': [partition._asdict() for partition in psutil.disk_partitions()],
        'disk_usage': {partition.device: psutil.disk_usage(partition.mountpoint)._asdict()
                       for partition in psutil.disk_partitions()},
    }
    system_info['disk'] = disk_info

    # Network Information
    network_info = psutil.net_if_addrs()
    system_info['network'] = {iface: {addr.family.name: addr.address for addr in addresses}
                              for iface, addresses in network_info.items()}

    # Process Information (Top processes)
    process_info = {}
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        process_info[proc.info['pid']] = proc.info

    system_info['processes'] = process_info

    # System Uptime
    system_info['uptime'] = time.time() - psutil.boot_time()

    # Windows specific info (using win32api)
    system_info['windows'] = {
        'windows_version': win32api.GetVersion(),
        'windows_build': win32api.GetVersionEx()[1],
    }

    return system_info

def main():
    system_info = get_system_info()

    # Convert the data to JSON format and print it
    json_data = json.dumps(system_info, indent=4)
    print(json_data)

if __name__ == "__main__":
    main()