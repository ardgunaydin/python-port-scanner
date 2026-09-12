import socket
import argparse
import json
import csv
import sys
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


VERSION = "2.0.0"


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Fast multithreaded TCP port scanner"
    )

    parser.add_argument(
        "target",
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "-p",
        "--ports",
        default="1-1000",
        help=(
            "Ports to scan. Examples: "
            "1-1000 | 22,80,443 | 20-100,443,8080"
        )
    )

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=100,
        help="Number of worker threads (default: 100)"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=0.5,
        help="Socket timeout in seconds (default: 0.5)"
    )

    parser.add_argument(
        "--banner",
        action="store_true",
        help="Attempt banner grabbing on open ports"
    )

    parser.add_argument(
        "-o",
        "--output",
        help="Save scan results to a .json or .csv file"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}"
    )

    return parser.parse_args()


def parse_ports(port_string):
    ports = set()

    try:
        parts = port_string.split(",")

        for part in parts:
            part = part.strip()

            if "-" in part:
                start_port, end_port = map(int, part.split("-", 1))

                if start_port > end_port:
                    raise ValueError(
                        f"Invalid port range: {part}"
                    )

                if start_port < 1 or end_port > 65535:
                    raise ValueError(
                        "Ports must be between 1 and 65535."
                    )

                ports.update(
                    range(start_port, end_port + 1)
                )

            else:
                port = int(part)

                if port < 1 or port > 65535:
                    raise ValueError(
                        "Ports must be between 1 and 65535."
                    )

                ports.add(port)

    except ValueError as error:
        print(f"Error!!! {error}")
        sys.exit(1)

    if not ports:
        print("Error!!! No valid ports were provided.")
        sys.exit(1)

    return sorted(ports)


def resolve_target(target):
    try:
        return socket.gethostbyname(target)

    except socket.gaierror:
        print(
            "Error!!! Invalid hostname or IP address."
        )
        sys.exit(1)


def get_service(port):
    try:
        return socket.getservbyport(
            port,
            "tcp"
        )

    except OSError:
        return "Unknown"


def grab_banner(target_ip, port, timeout):
    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(timeout)
            sock.connect(
                (target_ip, port)
            )

            banner = sock.recv(1024)

            if banner:
                decoded_banner = banner.decode(
                    "utf-8",
                    errors="ignore"
                ).strip()

                if decoded_banner:
                    return decoded_banner[:200]

    except (
        socket.timeout,
        ConnectionError,
        OSError
    ):
        pass

    return None


def scan_port(
    target_ip,
    port,
    timeout,
    banner_enabled
):
    try:
        with socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        ) as sock:

            sock.settimeout(timeout)

            result = sock.connect_ex(
                (target_ip, port)
            )

            if result != 0:
                return None

        service = get_service(port)

        banner = None

        if banner_enabled:
            banner = grab_banner(
                target_ip,
                port,
                timeout
            )

        result_data = {
            "port": port,
            "service": service,
            "banner": banner
        }

        print(
            f"[OPEN] {port:<5}/tcp "
            f"Service: {service}"
        )

        if banner:
            print(
                f"       Banner: {banner}"
            )

        return result_data

    except OSError:
        return None


def export_results(
    output_file,
    target,
    target_ip,
    ports,
    threads,
    timeout,
    banner_enabled,
    scan_duration,
    open_ports,
    started_at
):
    if not output_file:
        return

    output_lower = output_file.lower()

    if output_lower.endswith(".json"):
        results = {
            "scanner_version": VERSION,
            "target": target,
            "target_ip": target_ip,
            "started_at": started_at,
            "ports_scanned": len(ports),
            "threads": threads,
            "timeout_seconds": timeout,
            "banner_grabbing": banner_enabled,
            "scan_duration_seconds": round(
                scan_duration,
                3
            ),
            "open_ports": open_ports
        }

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump(
                results,
                file,
                indent=4
            )

    elif output_lower.endswith(".csv"):
        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.writer(file)

            writer.writerow([
                "target",
                "target_ip",
                "port",
                "service",
                "banner"
            ])

            for item in open_ports:
                writer.writerow([
                    target,
                    target_ip,
                    item["port"],
                    item["service"],
                    item["banner"] or ""
                ])

    else:
        print(
            "Error!!! Output file must end "
            "with .json or .csv"
        )
        sys.exit(1)

    print(
        f"Results saved to: {output_file}"
    )


def main():
    args = parse_arguments()

    if args.threads < 1:
        print(
            "Error!!! Thread count "
            "must be at least 1."
        )
        sys.exit(1)

    if args.timeout <= 0:
        print(
            "Error!!! Timeout must "
            "be greater than 0."
        )
        sys.exit(1)

    ports = parse_ports(
        args.ports
    )

    target_ip = resolve_target(
        args.target
    )

    started_at = datetime.now()

    print(
        "\n" + "*" * 55
    )
    print(
        f"Target:            {args.target}"
    )
    print(
        f"Resolved IP:       {target_ip}"
    )
    print(
        f"Ports selected:    {len(ports)}"
    )
    print(
        f"Threads:           {args.threads}"
    )
    print(
        f"Timeout:           {args.timeout}s"
    )
    print(
        "Banner grabbing:   "
        + (
            "Enabled"
            if args.banner
            else "Disabled"
        )
    )
    print(
        "Started at:        "
        + started_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    )
    print(
        "*" * 55
    )

    scan_start = datetime.now()

    open_ports = []

    with ThreadPoolExecutor(
        max_workers=args.threads
    ) as executor:

        futures = executor.map(
            lambda port: scan_port(
                target_ip,
                port,
                args.timeout,
                args.banner
            ),
            ports
        )

        for result in futures:
            if result:
                open_ports.append(
                    result
                )

    scan_end = datetime.now()

    scan_duration = (
        scan_end - scan_start
    ).total_seconds()

    open_ports.sort(
        key=lambda item: item["port"]
    )

    print(
        "\n" + "*" * 55
    )
    print(
        "Scan completed successfully!"
    )
    print(
        f"Ports scanned:     {len(ports)}"
    )
    print(
        f"Open ports found:  {len(open_ports)}"
    )
    print(
        f"Scan duration:     "
        f"{scan_duration:.3f} seconds"
    )

    export_results(
        output_file=args.output,
        target=args.target,
        target_ip=target_ip,
        ports=ports,
        threads=args.threads,
        timeout=args.timeout,
        banner_enabled=args.banner,
        scan_duration=scan_duration,
        open_ports=open_ports,
        started_at=started_at.isoformat()
    )

    print(
        "*" * 55
    )


if __name__ == "__main__":
    main()

/guno :p 