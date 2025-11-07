import json
from datetime import datetime

# === Load Manifest ===
with open("rebuild_manifest_complete.json", encoding="utf-8") as f:
    data = json.load(f)

convs = data.get("conversations", [])
print(f"✅ Loaded {len(convs)} conversations\n")

def format_norm_time(create, update):
    avg = (create + update) / 2
    dt = datetime.fromtimestamp(avg)
    return {
        "normalized_time": avg,
        "normtimename": dt.strftime("This_is_normalized.%H%M.%d%m%y")
    }

# === Expand Fields for Review ===
expanded = []

for conv in convs:
    title = conv.get("title", "")
    id_ = conv.get("id", "")
    turns = conv.get("turns", 0)
    messages = conv.get("messages", [])
    validation = conv.get("validation", {})

    norm = format_norm_time(conv.get("create_time", 0), conv.get("update_time", 0))

    result = {
        "title": title,
        "normalized_title": conv.get("normalized_title"),
        "id": id_,
        "create_time": conv.get("create_time"),
        "update_time": conv.get("update_time"),
        "normalized_time": norm["normalized_time"],
        "normtimename": norm["normtimename"],
        "source_part": conv.get("source_part"),
        "part_source": conv.get("part_source"),
        "mapping_entries": conv.get("mapping_entries"),
        "turns": turns,
        "user_msg_count": sum(1 for m in messages if m["role"] == "user"),
        "assistant_msg_count": sum(1 for m in messages if m["role"] == "assistant"),
        "first_preview": conv.get("first_preview", ""),
        "last_preview": conv.get("last_preview", ""),
        "status": conv.get("status"),
        "validation_total_messages": validation.get("total_messages"),
        "validation_exchanges": validation.get("exchanges")
    }

    expanded.append(result)

# === Save to Expanded CSV ===
import csv

with open("conversations_expanded.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=expanded[0].keys())
    writer.writeheader()
    writer.writerows(expanded)

print("✅ Expanded data written to conversations_expanded.csv")
