#!/usr/bin/env python3
"""Corelink v6.3.12 - Single DBOX Only + Clear Logging"""

import os, sys, json, subprocess, datetime, tkinter as tk
from tkinter import messagebox
from pathlib import Path
import pyperclip

# --- CONFIG ---
ROOT_DIR = r"C:\Soul_Algorithm"
BASE_DIR = r"C:\Soul_Algorithm\Scripts"
ARCHIVE_DIR = r"C:\Soul_Algorithm\Archive\Backups"
LOG_DIR = r"C:\Soul_Algorithm\Scripts\logs"
LOG_FILE = os.path.join(LOG_DIR, "corelink.log")
COMPILE_PATH = os.path.join(BASE_DIR, "CoreCompile.py")
VTT_SCRIPT = os.path.join(BASE_DIR, "vtt_processor.py")
DIRMAPPER_PATH = os.path.join(BASE_DIR, "dirmapper.py")
REPO_DIR = r"C:\Users\JoshMain\Documents\Working-DIR"
BACKUP_ROOT = r"C:\Backups_Soul"
__version__ = "6.3.12"

VALID_ACTIONS = ["safe_write", "make_file", "rename", "dirmapper", "run_python", "checkpoint", "run_queue"]
WRITE_ACTIONS = ["safe_write", "make_file", "rename", "dirmapper"]
READ_ACTIONS = ["run_python", "checkpoint"]

def log(msg, data=None):
    entry = {"timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "version": __version__, "message": msg}
    if data: entry["data"] = data
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def error_dbox(title, error_msg):
    """Error DBOX with Copy Log button"""
    log(f"ERROR_DBOX: {title}", {"error": error_msg})
    root = tk.Toplevel()
    root.title(f"❌ {title}")
    root.geometry("600x450")
    root.transient()
    root.grab_set()
    tk.Label(root, text=title, font=("Segoe UI", 12, "bold"), fg="#E74C3C").pack(pady=10)
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
    tk.Button(btn_frame, text="📋 Copy Error", command=copy_error, width=15, bg="#3498DB", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="OK", command=root.destroy, width=10, bg="#95A5A6", fg="white").pack(side="left", padx=5)
    root.wait_window()

def verify_dbox(title, msg, action_type="write"):
    """Single verification DBOX - ONLY ONE PER QUEUE"""
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
        tk.Button(btn_frame, text="✅ EXECUTE WRITE", command=proceed, width=18, bg="#E74C3C", fg="white").pack(side="left", padx=5)
    else:
        tk.Button(btn_frame, text="✅ CONTINUE", command=proceed, width=18, bg="#2ECC71", fg="white").pack(side="left", padx=5)
    tk.Button(btn_frame, text="🚫 CANCEL", command=cancel, width=15, bg="#95A5A6", fg="white").pack(side="left", padx=5)
    root.wait_window()
    return result["action"] == "PROCEED"

# --- QUEUE SYSTEM ---
action_queue = []
is_processing_queue = False

def validate_payload():
    """Parse and validate clipboard"""
    try:
        clip = pyperclip.paste().strip()
        if not clip:
            error_dbox("Empty Clipboard", "No JSON payload in clipboard")
            return None
        
        payload = json.loads(clip)
        log("PAYLOAD_RECEIVED", {"raw": clip})
        
        if payload.get("action") == "run_queue":
            actions = payload.get("queue", [])
            if not actions:
                error_dbox("Empty Queue", f"Your payload has 'action': 'run_queue' but no queue items.\n\nPayload:\n{json.dumps(payload, indent=2)}")
                return None
        else:
            actions = [payload]
        
        # Validate each action
        invalid_actions = []
        for i, action in enumerate(actions):
            if not isinstance(action, dict):
                invalid_actions.append(f"Item #{i+1}: Not a dictionary (got {type(action).__name__})")
                continue
            
            action_name = action.get("action")
            if action_name is None:
                action_preview = json.dumps(action, indent=2)
                invalid_actions.append(f"Item #{i+1}: Missing 'action' field or value is null/None\n\nProblematic item:\n{action_preview}")
                continue
            
            if action_name not in VALID_ACTIONS:
                invalid_actions.append(f"Item #{i+1}: '{action_name}' is not a valid action")
        
        if invalid_actions:
            full_payload = json.dumps(payload, indent=2)
            error_msg = f"❌ VALIDATION FAILED\n\nFound {len(invalid_actions)} problem(s):\n\n"
            error_msg += "\n\n".join(invalid_actions)
            error_msg += f"\n\n{'='*50}\n\nFull payload from clipboard:\n{full_payload}"
            error_msg += f"\n\n{'='*50}\n\n💡 EXAMPLE of correct format:\n"
            error_msg += json.dumps({
                "action": "make_file",
                "params": {"filename": "example.txt", "content": "hello"}
            }, indent=2)
            
            error_dbox("Invalid Payload", error_msg)
            return None
        
        # Check for write actions
        has_write = any(a.get("action") in WRITE_ACTIONS for a in actions)
        action_type = "write" if has_write else "read"
        
        # Build message (shows actions only, not success confirmations)
        msg = f"📋 {payload.get('description', 'Execution')}\n\nActions: {len(actions)}\n\n"
        for i, action in enumerate(actions, 1):
            msg += f"{i}. {action.get('action', 'unknown').upper()}\n"
            params = action.get("params", {})
            if "target_path" in params:
                msg += f"   → {params['target_path']}\n"
            elif "filename" in params:
                msg += f"   → {params['filename']}\n"
            elif "source_path" in params:
                msg += f"   → {params['source_path']} → {params.get('dest_path', '?')}\n"
        
        if has_write:
            msg += "\n⚠️ WRITE ACTIONS: Targets will be archived"
        else:
            msg += "\n✅ READ-ONLY: No modifications"
        
        return actions if verify_dbox("Confirm Execution", msg, action_type) else None
        
    except json.JSONDecodeError as e:
        error_dbox("Invalid JSON", f"Clipboard contains invalid JSON:\n\n{e}")
    except Exception as e:
        error_dbox("Payload Error", f"Critical error:\n\n{e}")
    
    return None

def process_queue():
    """Execute queue - SILENT execution, no per-action DBOXes"""
    global is_processing_queue, action_queue
    
    if not action_queue:
        is_processing_queue = False
        log("QUEUE_END")
        # FINAL SUMMARY DBOX
        messagebox.showinfo("Queue Complete", "✅ All actions executed successfully\n\nCheck logs for details.")
        return
    
    is_processing_queue = True
    action = action_queue.pop(0)
    action_name = action.get("action", "unknown")
    params = action.get("params", {})
    
    try:
        log("QUEUE_EXECUTE", {"action": action_name, "remaining": len(action_queue)})
        
        # Execute via CoreCompile
        payload = {"action": action_name, "params": params}
        result = subprocess.run([sys.executable, COMPILE_PATH], input=json.dumps(payload), text=True, capture_output=True, timeout=120)
        
        if result.returncode != 0:
            raise Exception(result.stderr)
        
        log(f"QUEUE_SUCCESS: {action_name}", {"target": params.get("target_path") or params.get("filename", "unknown")})
        
        # NO SUCCESS DBOX HERE - LOGS ONLY
        
        process_queue()
        
    except Exception as e:
        log(f"QUEUE_FAILED: {action_name}", {"error": str(e)})
        action_queue.clear()
        is_processing_queue = False
        
        target = params.get("target_path") or params.get("filename", "unknown")
        error_dbox("Execution Failed", f"ACTION: {action_name}\nTARGET: {target}\n\nERROR: {e}")

def execute_from_clipboard():
    """Button click handler"""
    actions = validate_payload()
    if actions:
        global action_queue
        action_queue = actions
        process_queue()

def self_update_from_clipboard():
    """WORKING SELF-UPDATE: Updates Corelink.py from clipboard"""
    try:
        clip = pyperclip.paste().strip()
        if not clip:
            error_dbox("Update Error", "Clipboard is empty. Copy the Corelink.py code first.")
            return
        
        # Parse as JSON payload
        payload = json.loads(clip)
        
        # If it's a raw string (the actual code), wrap it
        if isinstance(payload, str):
            code_content = payload
        elif isinstance(payload, dict) and "params" in payload and "content" in payload["params"]:
            code_content = payload["params"]["content"]
        else:
            # Assume it's a make_file payload
            code_content = payload.get("params", {}).get("content", "")
        
        if not code_content or "#!/usr/bin/env python3" not in code_content:
            error_dbox("Update Error", "Clipboard does not contain valid Corelink.py code. Copy the full script first.")
            return
        
        # Write to Corelink.py
        target_path = os.path.join(BASE_DIR, "Corelink.py")
        
        log("SELF_UPDATE_START", {"target": target_path})
        
        # Archive existing
        if os.path.exists(target_path):
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"Corelink.py_{timestamp}"
            archive_path = os.path.join(ARCHIVE_DIR, archive_name)
            os.makedirs(ARCHIVE_DIR, exist_ok=True)
            shutil.copy2(target_path, archive_path)
            log("UPDATE_ARCHIVE_CREATED", {"from": target_path, "to": archive_path})
        
        # Write new version
        with open(target_path, "w", encoding="utf-8") as f:
            f.write(code_content)
        
        log("SELF_UPDATE_SUCCESS", {"target": target_path})
        
        # SUCCESS DBOX - then restart
        if messagebox.askyesno("Update Complete", "✅ Corelink updated successfully!\n\nRestart now to apply changes?"):
            log("RESTART_REQUESTED")
            os.execl(sys.executable, sys.executable, target_path)
        
    except Exception as e:
        log(f"SELF_UPDATE_FAILED", {"error": str(e)})
        error_dbox("Update Failed", f"Error during self-update:\n\n{e}")

def launch_vtt():
    log("VTT_LAUNCH")
    try:
        result = subprocess.run([sys.executable, VTT_SCRIPT, "--clipboard", "--duration", "8"], capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            log("VTT_SUCCESS", {"length": data.get("length", 0)})
            messagebox.showinfo("VTT Success", f"✅ Transcribed {data.get('length', 0)} chars")
        else:
            log("VTT_ERROR", {"stderr": result.stderr})
            error_dbox("VTT Failed", result.stderr)
    except Exception as e:
        log("VTT_EXCEPTION", {"error": str(e)})
        error_dbox("VTT Error", str(e))

def build_ui():
    """Build UI"""
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
    
    tk.Button(left, text="▶ Execute Queue (Clipboard)", **btn_style, command=execute_from_clipboard).pack(pady=5)
    tk.Button(left, text="📋 Load to Queue", **btn_style, command=lambda: action_queue.extend(json.loads(pyperclip.paste()))).pack(pady=5)
    tk.Button(left, text="🗺️ Update Directory Map", **btn_style, command=execute_from_clipboard).pack(pady=5)
    tk.Button(left, text="🔄 Self-Update System", **btn_style, command=self_update_from_clipboard).pack(pady=5)
    tk.Button(left, text="🧹 Clear Queue", **btn_style, command=lambda: action_queue.clear()).pack(pady=5)
    tk.Button(left, text="📜 Open Log", **btn_style, command=lambda: subprocess.Popen(["notepad.exe", LOG_FILE])).pack(pady=5)
    tk.Button(left, text="❌ Exit", **btn_style, command=root.destroy).pack(pady=5)
    
    tk.Button(right, text="📊 Queue Status", width=15, height=2, command=lambda: messagebox.showinfo("Status", f"Queue: {len(action_queue)}\nProcessing: {is_processing_queue}")).pack(pady=5)
    tk.Button(right, text="🎤", **square_style, bg="#9B59B6", fg="white", command=launch_vtt).pack(pady=10)
    
    log("UI_INITIALIZED")
    root.mainloop()

if __name__ == "__main__":
    log("CORELINK_START")
    build_ui()