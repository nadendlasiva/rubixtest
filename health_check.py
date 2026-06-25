#!/usr/bin/env python3

import os
import platform
import shutil
import socket
import subprocess

def check_cpu():
    try:
        with open("/proc/loadavg") as f:
            load = f.read().split()
        return {"1min": load[0], "5min": load[1], "15min": load[2]}
    except Exception as e:
        return {"error": str(e)}

def check_memory():
    try:
        with open("/proc/meminfo") as f:
            lines = f.readlines()
        mem = {}
        for line in lines:
            parts = line.split()
            if parts[0] in ("MemTotal:", "MemFree:", "MemAvailable:"):
                mem[parts[0].rstrip(":")] = f"{int(parts[1]) // 1024} MB"
        return mem
    except Exception as e:
        return {"error": str(e)}

def check_disk():
    total, used, free = shutil.disk_usage("/")
    return {
        "total": f"{total // (1024**3)} GB",
        "used":  f"{used  // (1024**3)} GB",
        "free":  f"{free  // (1024**3)} GB",
    }

def check_network():
    try:
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return {"hostname": hostname, "ip": ip}
    except Exception as e:
        return {"error": str(e)}

def check_services(services):
    results = {}
    for svc in services:
        try:
            ret = subprocess.run(
                ["systemctl", "is-active", svc],
                capture_output=True, text=True
            )
            results[svc] = ret.stdout.strip()
        except FileNotFoundError:
            results[svc] = "systemctl not available"
    return results

def check_env_vars(keys):
    return {k: ("set" if os.environ.get(k) else "NOT SET") for k in keys}

def separator(title):
    print(f"\n{'='*40}")
    print(f"  {title}")
    print('='*40)

def print_dict(d):
    for k, v in d.items():
        print(f"  {k:<20}: {v}")

def main():
    print("\n*** DevOps Health Check ***")
    print(f"  OS      : {platform.system()} {platform.release()}")
    print(f"  Python  : {platform.python_version()}")

    separator("CPU Load Average")
    print_dict(check_cpu())

    separator("Memory")
    print_dict(check_memory())

    separator("Disk Usage (/)")
    print_dict(check_disk())

    separator("Network")
    print_dict(check_network())

    separator("Key Services")
    print_dict(check_services(["docker", "nginx", "sshd", "cron"]))

    separator("Environment Variables")
    print_dict(check_env_vars(["HOME", "USER", "PATH", "PYTHONPATH", "CI"]))

    print("\n*** Health check complete ***\n")

if __name__ == "__main__":
    main()
