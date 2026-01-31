import os, sys, subprocess, requests, shutil

filename = "cslckrwbcl.exe"
appdata_roaming = os.environ.get('APPDATA')
base_url = "https://cslckrwbcl.lrdevstudio.com/resources"
destination = os.path.join(appdata_roaming, '.cslckrwbcl')
exe = os.path.join(destination, filename)
version = 0

gv, vv = float(requests.get("https://raw.githubusercontent.com/raedhashmi/cslckrwbcl/main/version.txt").text.strip()), float(requests.get(f"{base_url}/version.txt").text.strip())

if gv > vv:
    base_url = "https://github.com/raedhashmi/cslckrwbcl/raw/refs/heads/main/output/"
    version = gv
else:
    base_url = "https://cslckrwbcl.lrdevstudio.com/resources/"
    version = vv

if "update" not in sys.argv:
    if os.path.exists(destination):
        shutil.rmtree(destination)
    
    os.makedirs(destination, exist_ok=True)
    
    response = requests.get(f"{base_url}/cslckrwbcl.exe", stream=True)
    response.raise_for_status()

    with open(exe, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    subprocess.Popen([exe])
    os._exit()
elif "update" in sys.argv:
    response = requests.get(f"{base_url}/cslckrwbcl.exe", stream=True)
    response.raise_for_status()

    with open(os.path.join(destination, "cslckrwbcln.exe"), "wb") as f:
        for chunk in response.iter_content(8192):
            if chunk:
                f.write(chunk)
    
    def replacer():
        try:
            os.replace(os.path.join(destination, "cslckrwbcln.exe"), exe)
        except OSError:
            replacer()
            
    replacer()
    subprocess.Popen(exe, shell=False)
    os._exit(0)