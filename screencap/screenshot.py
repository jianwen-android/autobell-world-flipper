import subprocess

subprocess.check_output(
    "adb shell /system/bin/screencap -p /sdcard/screencap.png", shell=True
)
subprocess.check_output("adb pull /sdcard/screencap.png ./screencap.png", shell=True)
