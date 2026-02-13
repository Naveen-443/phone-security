import subprocess
from whitelist import TRUSTED_PREFIXES

def detect_unknown_apps():
    output = subprocess.getoutput("adb shell pm list packages")
    unknown = []

    for line in output.splitlines():
        pkg = line.replace("package:", "").strip()
        if not any(pkg.startswith(p) for p in TRUSTED_PREFIXES):
            unknown.append(pkg)

    return unknown
