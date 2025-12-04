#!/usr/bin/env python3
"""Corelink v6.3.15 - Enhanced Self-Update with Source Selection"""

import os
import sys
import json
import subprocess
import datetime
import tkinter as tk
from tkinter import messagebox, filedialog
from pathlib import Path
import pyperclip
import shutil

# ─── CONFIG ──────────────────────────────────────────────────────────────────
ROOT_DIR = Path(r"C:\Soul_Algorithm")
BASE_DIR = ROOT_DIR / "Scripts"
ARCHIVE_DIR = ROOT_DIR / "Archive" / "Backups"
LOG_DIR = BASE_DIR / "logs"
LOG_FILE = LOG_DIR / "corelink.log"
COMPILE_PATH = BASE_DIR / "CoreCompile.py"
VTT_SCRIPT = BASE_DIR / "vtt_processor.py"
__version__ = "6.3.15"

VALID_ACTIONS = ["safe_write", "make_file", "rename", "dirmapper", "run_queue"]
WRITE_ACTIONS = ["safe_write", "make_file", "rename", "dirmapper"]

# ─── LOGGER ───────────────────────────────────────────────────────────────────


def log(msg, data=None):
    """Thread-safe JSON logging"""
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "version": __version__,
        "message": msg,
        "pid": os.getpid()
    }
    if data:
        entry["data"] = data
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

# ─── DIALOGS ────────────────────────────────────────────────────────────────


def error_dbox(title, error_msg):
    """Error dialog with copy-to-clipboard"""
    log(f"ERROR_DBOX: {title}", {"error": error_msg[:500]})
    root = tk.Toplevel()
    root.title(f"❌ {title}")
    root.geometry("600x450")
    root.transient()
    root.grab_set()
    tk.Label(root, text=title, font=("Segoe UI", 12, "bold"),
             fg="#E74C3C").pack(pady=10)
    text = tk.Text(root, height=15, width=70, wrap="word", bg="#FADBD8")
    text.pack(pady=5, padx=10)
    text.insert("1.0", error_msg)
    text.config(state="disabled")

    def copy_error():
        pyperclip.copy(f"{title}\n\n{error_msg}\n\n{datetime.datetime.now()}")
        log("ERROR_COPIED_TO_CLIPBOARD")
        messagebox.showinfo("Copied", "Error copied to clipboard!")
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="📋 Copy Error", command=copy_error,
              width=15, bg="#3498DB", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="OK", command=root.destroy, width=10,
              bg="#95A5A6", fg="white").pack(side="left", padx=5)
    root.wait_window()


def verify_dbox(title, msg, action_type="write"):
    """Single verification dialog per queue execution"""
    log(f"DBOX_VERIFY: {title}")
    root = tk.Toplevel()
    root.title(title)
    root.geometry("500x350")
    root.transient()
    root.grab_set()
    tk.Label(root, text=title, font=("Segoe UI", 12, "bold")).pack(pady=10)
    text = tk.Text(root, height=10, width=60, wrap="word")
    text.pack(pady=5, padx=10)
    text.insert("1.0", msg)
    text.config(state="disabled")
    result = {"action": None}

    def proceed():
        result["action"] = "PROCEED"
        root.destroy()

    def cancel():
        result["action"] = "CANCEL"
        root.destroy()
    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    if action_type == "write":
        tk.Button(btn_frame, text="✅ EXECUTE WRITE", command=proceed,
                  width=18, bg="#E74C3C", fg="white").pack(side="left", padx=5)
    else:
        tk.Button(btn_frame, text="✅ CONTINUE", command=proceed,
                  width=18, bg="#2ECC71", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="🚫 CANCEL", command=cancel, width=15,
              bg="#95A5A6", fg="white").pack(side="left", padx=5)
    root.wait_window()
    return result["action"] == "PROCEED"

# ─── SELF-UPDATE FUNCTION (ENHANCED) ─────────────────────────────────────────


def self_update_from_clipboard():
    """
    Self-Update: Choose source (clipboard or file) then update Corelink.py
    Uses safe_write pattern to avoid circular imports
    """
    try:
        # Step 1: Choose source dialog
        root = tk.Toplevel()
        root.title("Update Corelink.py")
        root.geometry("450x180")
        root.transient()
        root.grab_set()

        tk.Label(root, text="Choose Update Source", font=(
            "Segoe UI", 12, "bold")).pack(pady=10)

        source_choice = {"value": None}

        def choose_clipboard():
            source_choice["value"] = "clipboard"
            root.destroy()

        def choose_file():
            source_choice["value"] = "file"
            root.destroy()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="📋 Clipboard", width=15, bg="#3498DB", fg="white",
                  command=choose_clipboard).pack(side="left", padx=5)
        tk.Button(btn_frame, text="📁 Select File...", width=15, bg="#2ECC71", fg="white",
                  command=choose_file).pack(side="left", padx=5)

        root.wait_window()

        if source_choice["value"] is None:
            return  # User cancelled

        # Step 2: Get code content
        code_content = ""
        if source_choice["value"] == "clipboard":
            clip = pyperclip.paste().strip()
            if not clip:
                error_dbox("Update Error",
                           "Clipboard is empty. Copy Python code first.")
                return

            # Try to parse as JSON payload, fallback to raw code
            try:
                payload = json.loads(clip)
                if isinstance(payload, dict) and "params" in payload:
                    code_content = payload["params"].get("content", "")
                else:
                    code_content = clip
            except json.JSONDecodeError:
                code_content = clip

            if "#!/usr/bin/env python3" not in code_content:
                error_dbox("Update Error",
                           "Clipboard does not contain valid Corelink.py code")
                return
        else:
            # File selection
            file_path = filedialog.askopenfilename(
                title="Select Python File",
                initialdir=BASE_DIR,
                filetypes=[("Python", "*.py"), ("All Files", "*.*")]
            )

            if not file_path:
                return

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    code_content = f.read()
            except Exception as e:
                error_dbox("File Error", f"Could not read file:\n\n{e}")
                return

            if "#!/usr/bin/env python3" not in code_content:
                error_dbox("Update Error",
                           "Selected file is not valid Corelink.py code")
                return

        # Step 3: Update using safe_write logic (self-contained)
        target_path = BASE_DIR / "Corelink.py"
        log("SELF_UPDATE_START", {"target": str(
            target_path), "source": source_choice["value"]})

        # Replicate safe_write behavior (avoid circular imports)
        target_path.parent.mkdir(parents=True, exist_ok=True)

        # Archive existing
        if target_path.exists():
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{target_path.stem}_{timestamp}{target_path.suffix}"
            archive_path = ARCHIVE_DIR / archive_name
            archive_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target_path, archive_path)
            log("ARCHIVE_CREATED", {"from": str(
                target_path), "to": str(archive_path)})

        # Atomic write
        temp_path = target_path.with_suffix('.tmp')
        with open(temp_path, "w", encoding="utf-8") as f:
            f.write(code_content)
        temp_path.replace(target_path)

        log("SELF_UPDATE_SUCCESS", {"target": str(target_path)})

        # Step 4: Ask to restart
        if messagebox.askyesno("Update Complete", "✅ Corelink.py updated successfully!\n\nRestart now to apply changes?"):
            log("RESTART_REQUESTED")
            os.execl(sys.executable, sys.executable, str(target_path))

    except Exception as e:
        log(f"SELF_UPDATE_FAILED", {"error": str(e)})
        error_dbox("Update Failed", f"Error during self-update:\n\n{e}")


# ─── QUEUE SYSTEM ────────────────────────────────────────────────────────────
action_queue = []
is_processing_queue = False


def validate_payload():
    """Validate clipboard JSON payload"""
    try:
        clip = pyperclip.paste().strip()
        if not clip:
            error_dbox("Empty Clipboard", "No JSON payload in clipboard")
            return None

        payload = json.loads(clip)
        log("PAYLOAD_RECEIVED", {"raw": clip[:200]})

        if payload.get("action") == "run_queue":
            actions = payload.get("queue", [])
            if not actions:
                error_dbox("Empty Queue",
                           "run_queue action has no queue items")
                return None
        else:
            actions = [payload]

        invalid = []
        for i, act in enumerate(actions):
            if not isinstance(act, dict):
                invalid.append(f"Item #{i+1}: Not a dict")
                continue
            name = act.get("action")
            if name not in VALID_ACTIONS:
                invalid.append(f"Item #{i+1}: Invalid action '{name}'")
                continue
            params = act.get("params", {})
            if not isinstance(params, dict):
                invalid.append(f"Item #{i+1}: Params must be dict")
                continue

        if invalid:
            error_dbox("Invalid Payload", "\n\n".join(invalid))
            return None

        has_write = any(a.get("action") in WRITE_ACTIONS for a in actions)
        msg = f"📋 {payload.get('description', 'Execution')}\n\nActions: {len(actions)}\n\n"
        for i, act in enumerate(actions, 1):
            params = act.get("params", {})
            msg += f"{i}. {act['action'].upper()}\n"
            if "filename" in params:
                msg += f"   → {params['filename']}\n"
            elif "target_path" in params:
                msg += f"   → {params['target_path']}\n"
        msg += f"\n{'⚠️ WRITE' if has_write else '✅ READ-ONLY'}: Files will be archived" if has_write else ""

        return actions if verify_dbox("Confirm Execution", msg, "write" if has_write else "read") else None

    except json.JSONDecodeError as e:
        error_dbox("Invalid JSON", str(e))
    except Exception as e:
        error_dbox("Validation Error", str(e))

    return None


def process_queue():
    """Execute queue silently (no per-action DBOX)"""
    global is_processing_queue, action_queue

    if not action_queue:
        is_processing_queue = False
        log("QUEUE_END")
        messagebox.showinfo(
            "Complete", f"✅ Queue finished\n\nLogged to: {LOG_FILE}")
        return

    is_processing_queue = True
    action = action_queue.pop(0)
    name = action.get("action", "unknown")
    params = action.get("params", {})

    try:
        log("QUEUE_EXECUTE", {"action": name, "remaining": len(action_queue)})

        payload = {"action": name, "params": params}
        result = subprocess.run(
            [sys.executable, COMPILE_PATH],
            input=json.dumps(payload),
            text=True,
            capture_output=True,
            timeout=120,
            cwd=ROOT_DIR  # <--- THE ONLY CHANGE: Force CoreCompile to run from ROOT_DIR
        )

        if result.returncode != 0:
            raise Exception(result.stderr)

        log(f"QUEUE_SUCCESS: {name}")
        process_queue()

    except Exception as e:
        log(f"QUEUE_FAILED: {name}", {"error": str(e)})
        action_queue.clear()
        is_processing_queue = False
        error_dbox("Execution Failed", f"ACTION: {name}\nERROR: {e}")


def execute_from_clipboard():
    """Main entry point from UI"""
    actions = validate_payload()
    if actions:
        action_queue.clear()
        action_queue.extend(actions)
        process_queue()


def launch_vtt():
    """Launch voice transcription"""
    log("VTT_LAUNCH")
    try:
        result = subprocess.run([
            sys.executable, VTT_SCRIPT,
            "--clipboard", "--duration", "8"
        ], capture_output=True, text=True, timeout=60)

        if result.returncode == 0:
            data = json.loads(result.stdout)
            log("VTT_SUCCESS", {"length": data.get("length", 0)})
            messagebox.showinfo(
                "VTT Success", f"✅ Transcribed {data.get('length', 0)} chars")
        else:
            log("VTT_ERROR", {"stderr": result.stderr})
            error_dbox("VTT Failed", result.stderr)
    except Exception as e:
        log("VTT_EXCEPTION", {"error": str(e)})
        error_dbox("VTT Error", str(e))


def build_ui():
    """Build Tkinter UI"""
    root = tk.Tk()
    root.title(f"Corelink v{__version__}")
    root.geometry("520x420")
    root.resizable(False, False)

    left = tk.Frame(root, padx=20, pady=20)
    left.pack(side="left", fill="both", expand=True)
    right = tk.Frame(root, padx=10, pady=20)
    right.pack(side="right", fill="y")

    btn_style = {"width": 30, "font": ("Segoe UI", 9)}
    square_style = {"width": 15, "height": 2, "font": ("Segoe UI", 12, "bold")}

    # Main controls
    tk.Button(left, text="▶ Execute Queue (Clipboard)", **btn_style,
              command=execute_from_clipboard).pack(pady=5)
    tk.Button(left, text="📋 Load to Queue", **btn_style,
              command=lambda: action_queue.extend(json.loads(pyperclip.paste()))).pack(pady=5)
    tk.Button(left, text="🗺️ Update Directory Map", **btn_style,
              command=execute_from_clipboard).pack(pady=5)
    tk.Button(left, text="🔄 Self-Update System", **btn_style,
              command=self_update_from_clipboard).pack(pady=5)
    tk.Button(left, text="🧹 Clear Queue", **btn_style,
              command=lambda: action_queue.clear()).pack(pady=5)
    tk.Button(left, text="📜 Open Log", **btn_style,
              command=lambda: subprocess.Popen(["notepad.exe", LOG_FILE])).pack(pady=5)
    tk.Button(left, text="❌ Exit", **btn_style,
              command=root.destroy).pack(pady=5)

    # Status controls
    tk.Button(right, text="📊 Queue Status", width=15, height=2, command=lambda: messagebox.showinfo(
        "Status", f"Queue: {len(action_queue)}\nProcessing: {is_processing_queue}")).pack(pady=5)
    tk.Button(right, text="🎤", **square_style, bg="#9B59A6",
              fg="white", command=launch_vtt).pack(pady=10)

    log("UI_INITIALIZED")
    root.mainloop()


if __name__ == "__main__":
    log("CORELINK_START")
    build_ui()
