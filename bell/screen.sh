if adb shell dumpsys power | grep -q 'Display Power: state=ON'; then
     adb shell input keyevent 26
fi
