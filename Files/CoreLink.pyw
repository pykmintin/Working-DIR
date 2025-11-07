# CoreLink.pyw - Launcher (Prototype)
# Buttons:
# 1) Run CoreLink
# 2) Update CoreLink (timestamp prompt, archive+swap+relaunch)
# 3) Clear Cache + Launch (calls external cacheclearedge.py)
# 4) Run Grab

import os
import sys
import shutil
import subprocess
import time
from datetime import datetime, timedelta

# Third-party optional (preferred) for process handling; fallback uses taskkill
try:
    import psutil
except Exception:
    psutil = None

import tkinter as tk
from tkinter import messagebox
# [ADD] Single-instance protection (refined)
if psutil is not None:
    try:
        this_pid = os.getpid()
        this_exe = sys.executable.lower()
        for p in psutil.process_iter(attrs=["pid", "cmdline", "exe", "name"]):
            if p.info["pid"] == this_pid:
                continue
            exe = (p.info.get("exe") or "").lower()
            cmd = " ".join(p.info.get("cmdline") or []).lower()
            if ("corelink.pyw" in cmd or "corelink launcher" in cmd) and exe == this_exe:
                messagebox.showwarning("CoreLink", "CoreLink Launcher is already running.")
                sys.exit(0)
    except Exception:
        pass
else:
    # Fallback for systems without psutil
    import subprocess
    out = subprocess.run(
        'tasklist /FI "IMAGENAME eq pythonw.exe"', capture_output=True, text=True
    )
    if out.returncode == 0 and out.stdout.lower().count("pythonw.exe") > 1:
        messagebox.showwarning("CoreLink", "CoreLink Launcher is already running.")
        sys.exit(0)


BASE_ROOT = r"C:\Soul_Algorithm"
SCRIPTS_DIR = os.path.join(BASE_ROOT, "Scripts")
ARCHIVE_DIR = os.path.join(BASE_ROOT, r"Archive\CoreLink")
WORKER_PATH = os.path.join(SCRIPTS_DIR, "CoreLink.py")
ROOT_WORKER_SOURCE = os.path.join(BASE_ROOT, "CoreLink.py")
CACHE_CLEAR_SCRIPT = os.path.join(SCRIPTS_DIR, "cacheclearedge.py")
GRAB_SCRIPT = os.path.join(SCRIPTS_DIR, "grab.py")

def _ensure_dirs():
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

def _is_corelink_proc(p):
    """True if process appears to be running CoreLink.py"""
    try:
        # check command line first
        cl = " ".join(p.cmdline()).lower()
        if "corelink.py" in cl:
            return True
        # fallback: check name heuristic
        name = (p.name() or "").lower()
        if name.startswith("python") and "corelink" in cl:
            return True
    except Exception:
        pass
    return False

def close_running_corelink():
    """Terminate running CoreLink.py processes if any."""
    if psutil is None:
        # Fallback: best-effort kill by windowless process name pattern
        # (may kill unrelated python processes; so we filter by working dir if possible)
        subprocess.run('tasklist', shell=True)
        # safer: try wmic to filter commandline
        subprocess.run(r'wmic process where "CommandLine like \'%%CoreLink.py%%\'" call terminate',
                       shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return

    victims = []
    for p in psutil.process_iter(attrs=['pid','name','cmdline']):
        if _is_corelink_proc(p):
            victims.append(p)
            try:
                p.terminate()
            except Exception:
                pass
    if victims:
        psutil.wait_procs(victims, timeout=5)

def run_corelink():
    _ensure_dirs()
    if not os.path.exists(WORKER_PATH):
        messagebox.showerror("CoreLink", f"Worker not found:\n{WORKER_PATH}")
        return
    try:
        subprocess.Popen(
            ["pythonw", WORKER_PATH],
            creationflags=(subprocess.DETACHED_PROCESS if hasattr(subprocess, "DETACHED_PROCESS") else 0) |
                          (subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP") else 0)
        )
    except Exception as e:
        messagebox.showerror("CoreLink", f"Failed to launch CoreLink.py\n{e}")

def update_corelink():
    _ensure_dirs()
    if not os.path.exists(ROOT_WORKER_SOURCE):
        messagebox.showerror("Update CoreLink", f"No update found at:\n{ROOT_WORKER_SOURCE}")
        return

    # Timestamp validation: warn if older than 1 hour
    try:
        mtime = os.path.getmtime(ROOT_WORKER_SOURCE)
        age_sec = time.time() - mtime
        if age_sec > 3600:  # older than 1h
            if not messagebox.askyesno("Update CoreLink",
                "The update file is more than 1 hour old.\nContinue anyway?"):
                return
    except Exception:
        pass

    # Close running worker
    close_running_corelink()

    # Archive current worker if exists
    if os.path.exists(WORKER_PATH):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"CoreLink_{ts}.py"
        dest = os.path.join(ARCHIVE_DIR, archive_name)
        try:
            shutil.move(WORKER_PATH, dest)
        except Exception as e:
            messagebox.showerror("Update CoreLink", f"Failed to archive old worker:\n{e}")
            return

    # Copy new worker in place
    try:
        shutil.copy2(ROOT_WORKER_SOURCE, WORKER_PATH)
    except Exception as e:
        messagebox.showerror("Update CoreLink", f"Failed to copy new worker:\n{e}")
        return

    # Launch new worker
    run_corelink()
    messagebox.showinfo("Update CoreLink", "CoreLink updated and launched.")

def clear_cache_and_launch():
    _ensure_dirs()
    if not os.path.exists(CACHE_CLEAR_SCRIPT):
        messagebox.showerror("Clear Cache + Launch", f"cacheclearedge.py not found:\n{CACHE_CLEAR_SCRIPT}")
        return
    try:
        subprocess.Popen(
            ["python", CACHE_CLEAR_SCRIPT],
            creationflags=(subprocess.DETACHED_PROCESS if hasattr(subprocess, "DETACHED_PROCESS") else 0) |
                          (subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP") else 0)
        )
    except Exception as e:
        messagebox.showerror("Clear Cache + Launch", f"Failed to run cacheclearedge.py\n{e}")

def run_grab():
    _ensure_dirs()
    if not os.path.exists(GRAB_SCRIPT):
        messagebox.showerror("Run Grab", f"grab.py not found:\n{GRAB_SCRIPT}")
        return
    try:
        subprocess.Popen(
            ["python", GRAB_SCRIPT],
            creationflags=(subprocess.DETACHED_PROCESS if hasattr(subprocess, "DETACHED_PROCESS") else 0) |
                          (subprocess.CREATE_NEW_PROCESS_GROUP if hasattr(subprocess, "CREATE_NEW_PROCESS_GROUP") else 0)
        )
    except Exception as e:
        messagebox.showerror("Run Grab", f"Failed to run grab.py\n{e}")

def build_ui():
    root = tk.Tk()
    root.title("CoreLink Launcher (Prototype)")
    root.geometry("420x240")

    pad = {"padx": 10, "pady": 10}

    tk.Button(root, text="▶ Run CoreLink", height=2, width=28, command=run_corelink).pack(**pad)
    tk.Button(root, text="🔄 Update CoreLink", height=2, width=28, command=update_corelink).pack(**pad)
    tk.Button(root, text="🧹 Clear Cache + Launch", height=2, width=28, command=clear_cache_and_launch).pack(**pad)
    tk.Button(root, text="📂 Run Grab", height=2, width=28, command=run_grab).pack(**pad)

    # Footer
    footer = tk.Label(root, text=f"Root: {BASE_ROOT}  |  Scripts: {SCRIPTS_DIR}", fg="#555")
    footer.pack(side=tk.BOTTOM, pady=8)

    root.mainloop()

if __name__ == "__main__":
    build_ui()
