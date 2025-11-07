def process_raw_chat_history(raw_text, manifest_csv_path):
    """
    Takes raw pasted chat history and either:
    1. Returns existing ID if found in manifest
    2. Creates new JSON entry and appends to CSV
    """
    
    # Extract previews
    first_preview = raw_text.strip()[:100] if raw_text.strip() else "Unknown"
    last_preview = raw_text.strip()[-100:] if raw_text.strip() else "Unknown"
    
    # Check existence
    existing_id = None
    try:
        with open(manifest_csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('first_preview') == first_preview or row.get('last_preview') == last_preview:
                    existing_id = row.get('id')
                    break
    except FileNotFoundError:
        pass
    
    if existing_id:
        return {"status": "exists", "id": existing_id}
    
    # Generate new entry
    _, _, manifest_entry = convert_chat_to_manifest_format(raw_text, manifest_csv_path)
    
    # Append to CSV
    append_to_manifest_csv(manifest_entry, manifest_csv_path)
    
    # Save individual JSON
    json_filename = f"conversation_{manifest_entry['id']}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump(manifest_entry, f, indent=2)
    
    return {
        "status": "new",
        "id": manifest_entry['id'],
        "json_file": json_filename,
        "csv_updated": True
    }