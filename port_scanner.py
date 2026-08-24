import socket 
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
target = input("Enter target IP or hostname: ")

try:
    start_port = int(input("Enter start port: "))
    end_port = int(input("Enter end port: "))
except ValueError:
    print("Error!!! Port numbers must be integers.")
    exit()
if start_port < 1 or end_port > 65535:
    print("Error!!! Ports must be between 1 and 65535.")
    exit()
if start_port > end_port:
    print("Error!!! Start port cant be greater than end port.")
    exit()

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Error!!! Invalid hostname or IP address.")
    exit()


print("\n" + "*" * 40)
print(f"Scanning target: {target}")
print(f"Scanning ports: {start_port}-{end_port}")
print(f"Started at: {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
print("\n" + "*" * 40)

start_time = datetime.now()


def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.5)

    result = sock.connect_ex((target_ip, port))


    if result == 0:
        print(f"[OPEN] Port {port}")

    sock.close()



with ThreadPoolExecutor(max_workers=100) as executor:
    executor.map(scan_port, range(start_port, end_port + 1))

end_time = datetime.now()
scan_time = end_time - start_time

print("\n" + "*" * 40)
print("Scan completed successfully!")
print(f"Scan duration: {scan_time.total_seconds():.3f} seconds")
print("\n" + "*" * 40)