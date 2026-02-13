import time
from app_scanner import detect_unknown_apps
from battery_monitor import get_battery_status
from network_monitor import detect_high_network_usage
from phone_alert import send_phone_alert

print("\n PHONE SECURITY & POWER SAFETY SCAN STARTED\n")

report = []

# UNKNOWN APPS
unknown_apps = detect_unknown_apps()
if unknown_apps:
    report.append(" UNKNOWN APPS DETECTED:")
    report.extend(unknown_apps)
    send_phone_alert(
        "SECURITY WARNING",
        "Unknown apps detected on your phone"
    )

# NETWORK
network_risk, used_mb = detect_high_network_usage()

if network_risk:
    print(f"HIGH NETWORK USAGE DETECTED: {used_mb} MB in 10 seconds")
    send_phone_alert(
        "NETWORK WARNING",
        f"High background data usage detected ({used_mb} MB)"
    )
else:
    print(f"Network usage normal: {used_mb} MB")

# BATTERY MONITOR LOOP
level, charging = get_battery_status()
report.append(f" Battery Level: {level}%")

if level < 25 and not charging:
    send_phone_alert(
        "CRITICAL BATTERY WARNING",
        "Battery below 25%! Phone safety risk.\nConnect charger within 5 minutes."
    )

    print(" Waiting 5 minutes for charging...")
    for minute in range(5):
        time.sleep(60)
        level, charging = get_battery_status()
        print(f"Minute {minute+1}: Battery {level}%, Charging: {charging}")

        if charging:
            send_phone_alert(
                "CHARGING DETECTED",
                "Charging started. Shutdown prevention activated."
            )
            report.append(" Charging started — shutdown prevented")
            break
    else:
        send_phone_alert(
            "EMERGENCY POWER WARNING",
            "Battery critically low!\nPlease shut down phone manually."
        )
        report.append(" Charging not started — user warned to shutdown manually")

# SAVE REPORT
with open("scan_report.txt", "w") as f:
    for line in report:
        f.write(line + "\n")

print("\n".join(report))
print("\n Scan report saved as scan_report.txt")
