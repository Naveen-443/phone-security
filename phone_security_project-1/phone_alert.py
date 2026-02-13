import subprocess

def send_phone_alert(title, message):
    subprocess.run(
        f'adb shell cmd notification post -S bigtext security "{title}" "{message}"',
        shell=True
    )

    subprocess.run(
        f'adb shell am broadcast -a android.intent.action.SHOW_TOAST --es toast "{title}"',
        shell=True
    )

    subprocess.run("adb shell media volume --set 15", shell=True)
