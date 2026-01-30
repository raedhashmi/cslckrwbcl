import os, sys, time, subprocess, requests

base_url = "https://cslckrwbcl.lrdevstudio.com/resources/"
filename = "cslckrwbcl.exe"
appdata_roaming = os.environ.get('APPDATA')
destination = os.path.join(appdata_roaming, '.cslckrwbcl')
exe = os.path.join(destination, filename)

def get_ver(url):
    return requests.get(url).text.strip()

git_v_raw = get_ver("https://github.com/raedhashmi/cslckrwbcl/raw/main/version.txt")
vps_v_raw = get_ver(f"{base_url}version.txt")

git_v = tuple(map(int, git_v_raw.split('.')))
vps_v = tuple(map(int, vps_v_raw.split('.')))

if git_v > vps_v:
    base_url = "https://github.com/raedhashmi/cslckrwbcl/raw/refs/heads/main/"
else:
    base_url = "https://cslckrwbcl.lrdevstudio.com/resources/"

if len(sys.argv) !=2:
    print('[LOG] Installing')
    if os.path.exists(destination):
        with os.scandir(destination) as entries:
            for entry in entries:
                os.remove(entry)
        os.removedirs(destination)
    else: pass
    
    
    os.makedirs(os.path.join(appdata_roaming, 'screen_recordings'), exist_ok=True)
    os.makedirs(destination, exist_ok=True)
    with open(os.path.join(destination, 'version.txt'), 'w') as f:
        f.write('')
    
    response = requests.get(f"{base_url}cslckrwbcl.exe", stream=True)
    response.raise_for_status()

    with open(exe, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    subprocess.Popen([os.path.abspath(os.path.join(destination, filename))])
    sys.exit(0)
elif len(sys.argv) == 2:
    print("[LOG] Downloading new client")

    response = requests.get(f"{base_url}cslckrwbcl.exe", stream=True)
    response.raise_for_status()

    old_exe = os.path.join(destination, "cslckrwbcl.exe")
    new_temp_exe = os.path.join(destination, "cslckrwbcln.exe")

    with open(new_temp_exe, "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)

    time.sleep(4)
    
    if os.path.exists(old_exe):
        os.remove(old_exe)

    os.rename(new_temp_exe, old_exe)

    subprocess.Popen(old_exe, shell=True)
    sys.exit(0)

# pyinstaller --clean --onefile --noconsole "cslckrwbcl updater.py" --name="cslckrwbcl updater" --icon="favicon.ico" --workpath ../cslckrwbcl-builds --distpath output/updater --upx-dir="C:\Users\raedh\AppData\Local\Microsoft\WinGet\Packages\UPX.UPX_Microsoft.Winget.Source_8wekyb3d8bbwe\upx-5.1.0-win64\"