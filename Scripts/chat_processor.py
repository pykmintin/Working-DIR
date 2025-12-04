import os, json
from pathlib import Path
from datetime import datetime
from hashlib import sha256

# --- Safe Write: archive → .tmp → verify → rename → log ---
def safe_write(target_path: str, content: dict | str, category: str) -> bool:
    """
    Corelink-compliant atomic write with archival
    Steps: archive → .tmp → verify → rename → log
    """
    if os.path.exists(target_path):
        archive_dir = Path("Archive") / category
        archive_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        archive_name = f"{Path(target_path).stem}_{timestamp}{Path(target_path).suffix}"
        os.replace(target_path, archive_dir / archive_name)

    tmp_path = Path(target_path).with_suffix('.tmp')
    try:
        with open(tmp_path, 'w', encoding='utf-8') as f:
            if isinstance(content, dict):
                json.dump(content, f, indent=2)
            else:
                f.write(content)

        if tmp_path.stat().st_size == 0:
            raise IOError("Zero-byte write detected")

        os.replace(tmp_path, target_path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise

    log_event("safe_write", {
        "target": target_path,
        "category": category,
        "size": Path(target_path).stat().st_size,
        "status": "success"
    })

    return True

# --- Logging Event to queue_log.jsonl ---
def log_event(action: str, context: dict) -> None:
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "context": context
    }
    log_file = Path("Archive/Logs/queue_log.jsonl")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(log_entry) + '\n')

# --- Save Conversation to Archive/ChatLogs/conv_[id].json ---
def save_conversation(entry: dict) -> str:
    conv_id = entry["id"]
    file_path = Path("Archive/ChatLogs") / f"conv_{conv_id}.json"
    safe_write(str(file_path), entry, "ChatLogs")
    return str(file_path)

# --- Update CoreLink-Manifest.json ---
def update_manifest(conv_id: str, metadata: dict) -> None:
    path = "CoreLink-Manifest.json"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            manifest = json.load(f)
    else:
        manifest = {}
    manifest[conv_id] = metadata
    safe_write(path, manifest, "CoreLink")

# --- Main File Processor ---
def process_chat_file(raw_text: str, user_review_mode: bool = False) -> dict:
    lines = raw_text.strip().splitlines()
    user_turns = [line for line in lines if line.startswith("User:")]
    kimi_turns = [line for line in lines if line.startswith("Kimi:")]

    if not user_turns or not kimi_turns:
        return {"status": "format_error", "error": "No valid turns found"}

    conv_id = sha256(raw_text.encode()).hexdigest()[:12]
    timestamp = datetime.now().isoformat()

    entry = {
        "id": conv_id,
        "title": user_turns[0][5:].strip()[:40],
        "timestamp": timestamp,
        "raw": raw_text,
        "relevance_score": 1.0,
        "topics": ["general"]
    }

    file_path = save_conversation(entry)
    update_manifest(conv_id, {
        "title": entry["title"],
        "create_time": entry["timestamp"],
        "file_path": file_path,
        "relevance_score": entry["relevance_score"]
    })
    log_event("import_chat", {
        "conv_id": conv_id,
        "status": "keep",
        "topics": entry["topics"]
    })

    return {"status": "keep", "entry": entry, "formatted": format_strict_human_readable(entry)}

# --- Extract a Single Archived Conversation by ID ---
def extract_from_manifest(conv_id: str) -> str | None:
    path = "CoreLink-Manifest.json"
    if not os.path.exists(path):
        return None
    with open(path, 'r') as f:
        manifest = json.load(f)
    if conv_id not in manifest:
        return None
    with open(manifest[conv_id]['file_path'], 'r') as f:
        return format_strict_human_readable(json.load(f))

# --- Format as Human-Readable Output ---
def format_strict_human_readable(entry: dict) -> str:
    lines = []
    for line in entry.get("raw", "").splitlines():
        if line.startswith("User:"):
            lines.append(f"👤 {line[5:].strip()}")
        elif line.startswith("Kimi:"):
            lines.append(f"🤖 {line[5:].strip()}")
    return "\n".join(lines)
