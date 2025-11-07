#!/usr/bin/env python3
"""
CoreLink Bridge v3.7b — Flag Swap Build (no PowerShell)
=======================================================
Worker process. On self_update:
  - Touch update.flag in Scripts\
  - Exit immediately
Launcher (.pyw) will detect the flag, archive old CoreLink.py, move new ROOT\CoreLink.py into Scripts\, and relaunch the worker.
Includes a 📂 Run Grab button.
"""

import os, sys, json, subprocess, pyperclip, datetime, tkinter as tk
from tkinter import messagebox

# ────────────────────────────────
# [10] PATH CONFIG
# ────────────────────────────────
ROOT_DIR     = r"C:\Soul_Algorithm"
BASE_DIR     = os.path.join(ROOT_DIR, "Scripts")
LOG_DIR      = os.path.join(BASE_DIR, "logs")
LOG_FILE     = os.path.join(LOG_DIR, "corelink.log")
CHATLOG_DIR  = os.path.join(BASE_DIR, "ChatLogs")
REPORTS_DIR  = os.path.join(BASE_DIR, "Reports")
FLAG_FILE    = os.path.join(BASE_DIR, "update.flag")
NOTEPADPP    = r"C:\Program Files\Notepad++\notepad++.exe"

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(CHATLOG_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)

# ────────────────────────────────
# [20] LOGGING
# ────────────────────────────────
def write_log(message: str):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

write_log("Init → logs directory confirmed")

# ────────────────────────────────
# [30] GOOGLE DOCS ACTION
# ────────────────────────────────
def handle_google_update(data):
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
    except ImportError:
        messagebox.showerror("CoreLink", "Missing Google API libraries. Install:\n  pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        return

    doc_id = data.get("doc_id")
    section_title = data.get("section_title", "Update")
    content = data.get("content", "")
    creds_path = os.path.join(BASE_DIR, "credentials.json")

    try:
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=["https://www.googleapis.com/auth/documents"]
        )
        service = build("docs", "v1", credentials=creds)

        service.documents().batchUpdate(
            documentId=doc_id,
            body={
                "requests": [
                    {"deleteContentRange": {"range": {"segmentId": "", "startIndex": 1}}},
                    {"insertText": {"location": {"index": 1},
                                    "text": f"{section_title}\n{content}\n"}}
                ]
            },
        ).execute()

        write_log(f"Google Docs updated: {section_title}")
        messagebox.showinfo("CoreLink", "Google Docs update successful.")
    except Exception as e:
        write_log(f"Google Docs update failed: {e}")
        messagebox.showerror("CoreLink", f"Google Docs update failed:\n{e}")

# ────────────────────────────────
# [70] SCRIPT EXECUTION
# ────────────────────────────────
def run_script(data, source="manual"):
    try:
        if isinstance(data, str):
            data = json.loads(data)
    except Exception as e:
        write_log(f"Invalid data: {e}")
        return

    action = data.get("action", "").lower()
    write_log(f"Received action: {action}")

    if action == "google_update":
        handle_google_update(data); return
    if action == "self_update":
        write_log("Self-update requested (flag + exit)")
        try:
            with open(FLAG_FILE, "w", encoding="utf-8") as f:
                f.write(json.dumps({"version": data.get("version", ""), "ts": datetime.datetime.now().isoformat()}))
            write_log(f"Flag written: {FLAG_FILE}")
        except Exception as e:
            write_log(f"Flag write error: {e}")
        os._exit(0)

    if action in ["run_python", "run_inline"]:
        script_path = data.get("script_path")
        code = data.get("code")

        if code and not script_path:
            write_log("Inline Python execution triggered")
            try:
                temp_path = os.path.join(BASE_DIR, "temp_inline.py")
                with open(temp_path, "w", encoding="utf-8") as f: f.write(code)
                subprocess.Popen([sys.executable, temp_path], creationflags=0x08000000)
            except Exception as e:
                write_log(f"Inline exec error: {e}"); messagebox.showerror("CoreLink", f"Inline failed:\n{e}")
            return

        if script_path:
            if not os.path.isabs(script_path):
                script_path = os.path.join(ROOT_DIR, script_path)
            if os.path.exists(script_path):
                args = data.get("args", [])
                try:
                    subprocess.Popen([sys.executable, script_path] + args, creationflags=0x08000000)
                    write_log(f"Launched: {script_path} {args}"); messagebox.showinfo("CoreLink", f"Running {os.path.basename(script_path)}")
                except Exception as e:
                    write_log(f"External run error: {e}"); messagebox.showerror("CoreLink", f"Run failed:\n{e}")
            else:
                write_log(f"Not found: {script_path}"); messagebox.showerror("CoreLink", f"Script not found:\n{script_path}")
            return

    write_log(f"Unknown action: {action}"); messagebox.showwarning("CoreLink", f"Unknown action: {action}")

# ────────────────────────────────
# [150] UI
# ────────────────────────────────
def build_ui():
    root = tk.Tk()
    root.title("CoreLink Runtime v3.7b")
    root.geometry("480x260")
    root.resizable(False, False)

    frame_left = tk.Frame(root, padx=20, pady=20)
    frame_left.pack(side="left", fill="both", expand=True)
    frame_right = tk.Frame(root, padx=10, pady=20)
    frame_right.pack(side="right", fill="y")

    tk.Button(frame_left, text="▶ Play from Clipboard", width=30,
              command=lambda: run_script(pyperclip.paste(), "clipboard")).pack(pady=5)
    # tk.Button(frame_left, text="📄 Play from Default File", width=30,
    #           command=lambda: run_script(open(os.path.join(BASE_DIR, "CoreLink_load.json")).read(), "file")).pack(pady=5)
    tk.Button(frame_left, text="📂 Run Grab", width=30,
              command=lambda: subprocess.Popen([sys.executable, os.path.join(BASE_DIR, "grab.py")], creationflags=0x08000000)).pack(pady=5)
    # 🗒️ Note: 'Play from Default File' function still exists internally,
    #   but the button is hidden (for potential future use).
    # 🗑️ 'New Chat' button removed as redundant.
    tk.Button(frame_left, text="📜 Open Log (Notepad++)", width=30,
              command=lambda: subprocess.Popen([NOTEPADPP, LOG_FILE])).pack(pady=5)
    tk.Button(frame_left, text="❌ Exit", width=30, command=root.destroy).pack(pady=5)

    global btn_record
    btn_record = tk.Button(frame_right, text="🛑 OFF", width=10, height=4,
                           bg="#DC143C", fg="white", font=("Segoe UI", 14, "bold"),
                           command=toggle_record)
    btn_record.pack(expand=True, fill="both")

    # [DEBUG] simple file logger
    DEBUG_MODE = True
    def debug_log(msg):
        if DEBUG_MODE:
            write_log(f"[DEBUG] {msg}")

    root.mainloop()


# ────────────────────────────────
# [200] RECORD BUTTON
# ────────────────────────────────
recording = False
def toggle_record():
    global recording
    recording = not recording
    btn_record.config(text="🎙 ON" if recording else "🛑 OFF",
                      bg="#32CD32" if recording else "#DC143C",
                      activebackground="#228B22" if recording else "#8B0000")
    write_log(f"Recording toggled: {'ON' if recording else 'OFF'}")

# ────────────────────────────────
# [250] MAIN
# ────────────────────────────────
if __name__ == "__main__":
    write_log("CoreLink initialized (v3.7b)")
    build_ui()
