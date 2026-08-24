# Python Port Scanner

A simple multithreaded TCP port scanner built with Python.

This project was created to practice Python networking concepts, TCP sockets, multithreading, and basic network reconnaissance.

## Features

- TCP port scanning
- Custom port range selection
- Multithreaded scanning for improved performance
- Hostname to IPv4 address resolution
- Input validation for port numbers
- Invalid hostname/IP error handling
- Open port detection
- Scan duration measurement

## How It Works

The scanner attempts to establish a TCP connection with each port in the specified range.

If the connection is successful, the port is reported as open.

To improve scanning speed, the program uses Python's `ThreadPoolExecutor` to scan multiple ports concurrently.

## Requirements

- Python 3.x

No external Python packages are required.

## Usage

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd python-port-scanner
```

Run the scanner:

```bash
python port_scanner.py
```

Enter the target hostname or IP address and the port range when prompted:

```text
Enter target IP or hostname: 127.0.0.1
Enter start port: 1
Enter end port: 1000
```

## Example Output

```text
****************************************
Scanning target: 127.0.0.1
Scanning ports: 1-1000
Started at: 23:45:12.315

****************************************
[OPEN] Port 135
[OPEN] Port 445

****************************************
Scan completed successfully!
Scan duration: 5.124 seconds

****************************************
```

## Technologies Used

- Python
- Socket Programming
- TCP/IP
- Multithreading

## Disclaimer

This project is intended for educational purposes and authorized security testing only.

Only scan systems that you own or have explicit permission to test.

## Future Improvements

- Service detection
- Command-line arguments
- Improved scan result formatting
- Export scan results to a file
- Additional scanning options