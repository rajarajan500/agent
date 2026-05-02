import os
import subprocess
import glob
import winreg
import threading
from config import USERNAME, PATHS

def create_folder(path, **_):
    os.makedirs(path, exist_ok=True)
    print(f"  ✓ Folder created: {path}")
    return f"✓ Folder created: {path}"

def create_file(path, content="", **_):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  ✓ File created: {path}")
    return f"✓ File created: {path}"

def read_file(path, **_):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def open_folder(path, **_):
    if os.path.exists(path):
        subprocess.Popen(f'explorer "{path}"', shell=True)
        print(f"  ✓ Opened folder: {path}")
        return f"✓ Opened: {path}"
    return f"✗ Not found: {path}"

def find_folder(name, **_):
    print(f"  ⟳ Searching for folder: {name}...")
    skip = {"appdata","python","node_modules","site-packages",".git","typeshed","jedi","__pycache__"}
    for root, dirs, _ in os.walk(f"C:\\Users\\{USERNAME}"):
        dirs[:] = [d for d in dirs if d.lower() not in skip]
        for d in dirs:
            if name.lower() in d.lower():
                path = os.path.join(root, d)
                subprocess.Popen(f'explorer "{path}"', shell=True)
                print(f"  ✓ Found and opened: {path}")
                return f"✓ Opened: {path}"
    return f"✗ Folder not found: {name}"

def open_app(name, **_):
    print(f"  ⟳ Looking for {name}...")
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
              r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths")
        for i in range(winreg.QueryInfoKey(key)[0]):
            k = winreg.EnumKey(key, i)
            if name.lower() in k.lower():
                p = winreg.QueryValue(winreg.OpenKey(key, k), None)
                if p and os.path.exists(p):
                    subprocess.Popen([p])
                    print(f"  ✓ Opened: {p}")
                    return f"✓ Opened: {p}"
    except:
        pass

    skip = {"python","node_modules","site-packages","jedi","typeshed","__pycache__"}
    search = [
        f"C:\\Users\\{USERNAME}\\AppData\\Local",
        f"C:\\Users\\{USERNAME}\\AppData\\Roaming",
        "C:\\Program Files",
        "C:\\Program Files (x86)",
    ]
    for base in search:
        for root, dirs, files in os.walk(base):
            dirs[:] = [d for d in dirs if d.lower() not in skip]
            for f in files:
                if f.lower().endswith(".exe") and name.lower() in f.lower():
                    full = os.path.join(root, f)
                    subprocess.Popen(full)
                    print(f"  ✓ Opened: {full}")
                    return f"✓ Opened: {full}"

    subprocess.Popen(f"start {name}", shell=True)
    return f"✓ Tried: {name}"

def open_url(url, **_):
    subprocess.Popen(f"start {url}", shell=True)
    print(f"  ✓ Opened: {url}")
    return f"✓ Opened: {url}"

def run_command(command, cwd=None, **_):
    """Run a quick command, show output instantly"""
    print(f"\n  ⟳ Running: {command}")
    if cwd:
        print(f"  📁 In folder: {cwd}")
    print("  " + "─"*50)

    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd,
        bufsize=1,
        universal_newlines=True
    )

    output_lines = []
    for line in process.stdout:
        line = line.rstrip()
        if line:
            print(f"  {line}")
            output_lines.append(line)

    process.wait()
    print("  " + "─"*50)

    if process.returncode == 0:
        print(f"  ✓ Done!\n")
    else:
        print(f"  ✗ Finished with errors\n")

    return "\n".join(output_lines[-5:]) or "✓ Done"

def run_npm_install(cwd, **_):
    return run_command("npm install", cwd=cwd)

def run_npm_dev(cwd, **_):
    """Run npm run dev and show the local URL"""
    print(f"\n  ⟳ Starting dev server in: {cwd}")
    print(f"  ℹ  Press CTRL+C to stop the server\n")
    print("  " + "─"*50)
    process = subprocess.Popen(
        "npm run dev",
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        cwd=cwd,
        bufsize=1,
        universal_newlines=True
    )
    for line in process.stdout:
        line = line.rstrip()
        if line:
            print(f"  {line}")
        if "localhost" in line.lower() or "local:" in line.lower():
            print(f"\n  ✓ Server is running! Open the link above in your browser\n")
    process.wait()
    return "✓ Dev server stopped"

def create_vite_app(path, template="react", **_):
    folder_name = os.path.basename(path)
    parent = os.path.dirname(path)
    os.makedirs(parent, exist_ok=True)
    print(f"\n  ⟳ Creating Vite + React app: {folder_name}")
    run_command(
        f"npm create vite@latest {folder_name} -- --template {template}",
        cwd=parent
    )
    print(f"  ⟳ Installing dependencies...")
    run_command("npm install", cwd=path)
    print(f"  ✓ Vite app ready at: {path}")
    return f"✓ Vite app created at: {path}"

ACTIONS = {
    "create_folder":   create_folder,
    "create_file":     create_file,
    "read_file":       read_file,
    "open_folder":     open_folder,
    "find_folder":     find_folder,
    "open_app":        open_app,
    "open_url":        open_url,
    "run_command":     run_command,
    "run_npm_install": run_npm_install,
    "run_npm_dev":     run_npm_dev,
    "create_vite_app": create_vite_app,
}