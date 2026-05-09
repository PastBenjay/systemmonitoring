import psutil
import datetime
import time
import os

# Config
LOG_FILE = "system_monitor.log"
CHECK_INTERVAL = 60  # seconds
CPU_THRESHOLD = 80   # alert if CPU above 80%
MEM_THRESHOLD = 80   # alert if memory above 80%
DISK_THRESHOLD = 90  # alert if disk above 90%

def get_system_stats():
    """Collect current system statistics."""
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')

    stats = {
        "cpu_percent": cpu,
        "memory_percent": memory.percent,
        "memory_used_gb": round(memory.used / (1024**3), 2),
        "memory_total_gb": round(memory.total / (1024**3), 2),
        "disk_percent": disk.percent,
        "disk_used_gb": round(disk.used / (1024**3), 2),
        "disk_total_gb": round(disk.total / (1024**3), 2),
    }
    return stats

def check_alerts(stats):
    """Check if any metric exceeds thresholds."""
    alerts = []
    if stats["cpu_percent"] > CPU_THRESHOLD:
        alerts.append(f"HIGH CPU: {stats['cpu_percent']}%")
    if stats["memory_percent"] > MEM_THRESHOLD:
        alerts.append(f"HIGH MEMORY: {stats['memory_percent']}%")
    if stats["disk_percent"] > DISK_THRESHOLD:
        alerts.append(f"HIGH DISK: {stats['disk_percent']}%")
    return alerts

def log_stats(stats, alerts):
    """Write stats and alerts to log file."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"""
========================================
Timestamp : {timestamp}
CPU Usage : {stats['cpu_percent']}%
Memory    : {stats['memory_percent']}% ({stats['memory_used_gb']}GB / {stats['memory_total_gb']}GB)
Disk      : {stats['disk_percent']}% ({stats['disk_used_gb']}GB / {stats['disk_total_gb']}GB)
"""
    if alerts:
        log_entry += "⚠️  ALERTS:\n"
        for alert in alerts:
            log_entry += f"   - {alert}\n"
    else:
        log_entry += "Status    : All systems normal ✅\n"

    log_entry += "========================================\n"

    # Print to terminal
    print(log_entry)

    # Write to log file
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def main():
    print(f"🚀 System Monitor Started")
    print(f"📁 Logging to: {os.path.abspath(LOG_FILE)}")
    print(f"⏱️  Checking every {CHECK_INTERVAL} seconds")
    print(f"🔔 Alert thresholds — CPU: {CPU_THRESHOLD}%, Memory: {MEM_THRESHOLD}%, Disk: {DISK_THRESHOLD}%")
    print("Press Ctrl+C to stop.\n")

    try:
        while True:
            stats = get_system_stats()
            alerts = check_alerts(stats)
            log_stats(stats, alerts)
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n✅ Monitor stopped. Log saved to:", LOG_FILE)

if __name__ == "__main__":
    main()