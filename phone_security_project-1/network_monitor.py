import subprocess
import re

def get_network_bytes():
    """
    Returns total rx + tx bytes from Android netstats
    """
    data = subprocess.getoutput("adb shell dumpsys netstats")

    rx_total = 0
    tx_total = 0

    rx_matches = re.findall(r'rxBytes=(\d+)', data)
    tx_matches = re.findall(r'txBytes=(\d+)', data)

    for r in rx_matches:
        rx_total += int(r)
    for t in tx_matches:
        tx_total += int(t)

    return rx_total, tx_total


def detect_high_network_usage(threshold_mb=50):
    """
    Detects abnormal network usage based on byte difference
    """
    rx1, tx1 = get_network_bytes()

    # wait interval (seconds)
    import time
    time.sleep(10)

    rx2, tx2 = get_network_bytes()

    used_mb = ((rx2 - rx1) + (tx2 - tx1)) / (1024 * 1024)

    if used_mb >= threshold_mb:
        return True, round(used_mb, 2)

    return False, round(used_mb, 2)
