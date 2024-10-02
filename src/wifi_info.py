import subprocess

def get_wifi_ssid():
    try:
        # Run the command to get the current Wi-Fi SSID
        result = subprocess.check_output(['iwgetid', '--raw'], universal_newlines=True)
        ssid = result.strip()  # Remove any leading/trailing whitespace
        return ssid if ssid else "SSID not found"
    except subprocess.CalledProcessError:
        return "Wi-Fi not connected or SSID not available"

def get_ipv4_address():
    try:
        # Run the command to get IP address for the wlan0 interface
        result = subprocess.check_output(['hostname', '-I'], universal_newlines=True)
        ipv4_address = result.split()[0]  # Get the first IP address in the output
        return ipv4_address
    except subprocess.CalledProcessError:
        return "IPv4 address not found"
