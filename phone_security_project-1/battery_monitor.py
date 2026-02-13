import subprocess

def get_battery_status():
    data = subprocess.getoutput("adb shell dumpsys battery")

    level = None
    charging = False

    for line in data.splitlines():
        if "level:" in line:
            level = int(line.split(":")[1].strip())
        if "AC powered: true" in line or "USB powered: true" in line:
            charging = True

    return level, charging
