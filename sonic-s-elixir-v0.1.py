import os
import sys
import platform
import subprocess

def check_adb_availability():
    try:
        subprocess.check_output(["adb", "devices"], text=True)
    except subprocess.CalledProcessError:
        print("adb is not installed. Please install it before running this script.")
        sys.exit(1)

def check_connected_devices():
    devices = subprocess.check_output(["adb", "devices"], text=True).strip().split("\n")
    if len(devices) == 1:
        print("No connected devices found.")
        sys.exit(1)
    return devices

def check_usb_debugging_enabled(device):
    device = device.strip()
    try:
        subprocess.check_output(["adb", "shell", "getprop", "sys.usb.config"], text=True)
    except subprocess.CalledProcessError:
        print(f"USB debugging is not enabled on device '{device}'. Please enable it before running this script.")
        sys.exit(1)

def get_device_information():
    model = subprocess.check_output(["adb", "shell", "getprop", "ro.product.model"], text=True)
    model = model.strip()

    brand = subprocess.check_output(["adb", "shell", "getprop", "ro.product.brand"], text=True)
    brand = brand.strip()

    version = subprocess.check_output(["adb", "shell", "getprop", "ro.build.version.release"], text=True)
    version = version.strip()

    return {"model": model, "brand": brand, "version": version}

def execute_adb_commands(commands):
    for command in commands:
        print(f"Executing command: {command}")
        subprocess.check_call(["adb", "shell", command])

def main():
    check_adb_availability()
    connected_devices = check_connected_devices()
    for device in connected_devices:
        check_usb_debugging_enabled(device)

    device_info = get_device_information()
    print(f"Device information:")
    print("- Model:", device_info["model"])
    print("- Brand:", device_info["brand"])
    print("- Android version:", device_info["version"])

    adb_commands = ["pm trim-caches 999999999999999999", "cmd package compile -m speed-profile -f -a", "cmd package bg-dexopt-job"]
    execute_adb_commands(adb_commands)

    print("Operation completed.")

if __name__ == "__main__":
    main()
