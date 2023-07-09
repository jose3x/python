import subprocess
import platform

def get_wifi_info():
    wifi_info = {
        "ssid": None,
        "channel": None,
        "signal_info": {
            "RSSI": None,
            "Noise": None
        }
    }

    if platform.system() == "Darwin":  # macOS
        try:
            ssid_output = subprocess.Popen(["networksetup", "-getairportnetwork", "en0"], stdout=subprocess.PIPE)
            ssid_result = ssid_output.communicate()[0].decode("utf-8").strip()
            wifi_info["ssid"] = ssid_result.split(":")[-1].strip()
        except subprocess.CalledProcessError:
            wifi_info["ssid"] = "Error: Unable to retrieve Wi-Fi information"

        try:
            channel_output = subprocess.Popen(["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport", "-I"], stdout=subprocess.PIPE)
            channel_result = channel_output.communicate()[0].decode("utf-8").strip()
            wifi_info["channel"] = channel_result.split(" channel: ")[-1].split("\n")[0]
            wifi_info["signal_info"]["RSSI"] = channel_result.split("agrCtlRSSI: ")[-1].split("\n")[0]
            wifi_info["signal_info"]["Noise"] = channel_result.split("agrCtlNoise: ")[-1].split("\n")[0]
        except subprocess.CalledProcessError:
            wifi_info["channel"] = "Error: Unable to retrieve Wi-Fi channel"
    elif platform.system() == "Windows":  # Windows
        try:
            output = subprocess.Popen(['netsh', 'wlan', 'show', 'interfaces'], stdout=subprocess.PIPE)
            output_result = output.communicate()[0].decode("utf-8").strip().split('\n')
            ssid_line = [line for line in output_result if "SSID" in line][0]
            wifi_info["ssid"] = ssid_line.split(":")[1].strip()
        except subprocess.CalledProcessError:
            wifi_info["ssid"] = "Error: Unable to retrieve Wi-Fi information"

    return wifi_info

wifi_info = get_wifi_info()
output = f"Wi-Fi SSID: {wifi_info['ssid']}\nWi-Fi Channel: {wifi_info['channel']}\nWi-Fi Signal Info: {wifi_info['signal_info']}"

print(output)
