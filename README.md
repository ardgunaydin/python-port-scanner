# Python Port Scanner

A fast, multithreaded TCP port scanner built with Python for learning and practicing networking, socket programming, and cybersecurity concepts.

The project started as a simple TCP port scanner and was gradually developed into a configurable command-line tool with service identification, optional banner grabbing, flexible port selection, and structured result exports.

## Features

* Multithreaded TCP port scanning
* Hostname to IPv4 address resolution
* Flexible port selection

  * Port ranges: `1-1000`
  * Individual ports: `22,80,443`
  * Combined selection: `20-100,443,8080`
* Service identification for open ports
* Configurable worker thread count
* Configurable socket timeout
* Optional banner grabbing
* JSON result export
* CSV result export
* Scan duration and summary
* Input validation and error handling
* Built-in CLI help
* Version information
* Automatic socket cleanup

## Requirements

* Python 3.x

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

### Basic Scan

```bash
python port_scanner.py localhost
```

By default, the scanner checks TCP ports `1-1000` using 100 worker threads.

### Scan a Port Range

```bash
python port_scanner.py 192.168.1.10 -p 1-1000
```

### Scan Specific Ports

```bash
python port_scanner.py 192.168.1.10 -p 22,80,443
```

### Combine Port Ranges and Individual Ports

```bash
python port_scanner.py 192.168.1.10 -p 20-100,443,8080
```

### Configure Threads and Timeout

```bash
python port_scanner.py 192.168.1.10 -p 1-1000 -t 200 --timeout 0.3
```

### Enable Banner Grabbing

```bash
python port_scanner.py 192.168.1.10 -p 1-1000 --banner
```

Banner grabbing is optional because not all services provide a readable banner immediately after a TCP connection is established.

### Export Results to JSON

```bash
python port_scanner.py 192.168.1.10 -p 1-1000 -o results.json
```

### Export Results to CSV

```bash
python port_scanner.py 192.168.1.10 -p 1-1000 -o results.csv
```

### Display Help

```bash
python port_scanner.py --help
```

### Display Version

```bash
python port_scanner.py --version
```

## Example Output

```text
*******************************************************
Target:            localhost
Resolved IP:       127.0.0.1
Ports selected:    1000
Threads:           200
Timeout:           0.5s
Banner grabbing:   Disabled
Started at:        2026-09-13 00:10:00
*******************************************************

[OPEN] 135  /tcp Service: epmap
[OPEN] 445  /tcp Service: microsoft-ds

*******************************************************
Scan completed successfully!
Ports scanned:     1000
Open ports found:  2
Scan duration:     2.593 seconds
*******************************************************
```

## JSON Output

Scan results can be stored in a structured JSON format:

```json
{
    "scanner_version": "2.0.0",
    "target": "localhost",
    "target_ip": "127.0.0.1",
    "ports_scanned": 1000,
    "threads": 200,
    "timeout_seconds": 0.5,
    "banner_grabbing": false,
    "open_ports": [
        {
            "port": 135,
            "service": "epmap",
            "banner": null
        },
        {
            "port": 445,
            "service": "microsoft-ds",
            "banner": null
        }
    ]
}
```

## Technologies & Concepts

* Python
* TCP/IP
* Socket Programming
* Multithreading
* `ThreadPoolExecutor`
* Command-Line Interfaces
* `argparse`
* JSON
* CSV
* Service Identification
* Banner Grabbing
* Exception Handling

## What I Learned

Building and improving this project gave me practical experience with:

* Creating TCP connections using Python sockets
* Understanding how TCP port scanning works
* Using concurrency to improve scan performance
* Resolving hostnames to IPv4 addresses
* Mapping TCP ports to common services
* Implementing basic banner grabbing
* Designing a command-line interface with `argparse`
* Validating user input and handling network errors
* Exporting structured scan results to JSON and CSV
* Refactoring a basic script into a more modular Python application

## Ethical Use

This project was created for educational purposes and authorized security testing only.

Only scan systems that you own or have explicit permission to test. Unauthorized scanning may violate organizational policies, terms of service, or applicable laws.

## Future Improvements

Potential future improvements include:

* IPv6 support
* UDP scanning
* Improved service fingerprinting
* Progress indicators
* Automated tests
* Additional output formats

## Author

**Arda Günaydın**

Computer Science student focused on networking and cybersecurity.
