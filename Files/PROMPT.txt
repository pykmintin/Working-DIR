📋 NEW SESSION PROMPT: ChatGPT Conversation Processor
PROJECT SNAPSHOT
Repository: https://github.com/pykmintin/Working-DIR
Source Data: conversations.json (85MB, 242 conversations, Nov 2025)
Goal: Build manifest system + deduplication pipeline
Key Files:
chat_processor.py (main entry point)
Files/CoreLink.py (core logic)
Files/DupeChecker.py (duplicate detection - BROKEN)
🎯 IMMEDIATE TASKS (Priority Order)
1. FIX Critical Bugs First
[ ] Fix DupeChecker.py - Change return True/False to return {'status': 'new', 'filename': '...'}
[ ] Fix test_suite.py line 17 - Handle status dictionary instead of boolean
[ ] Repair TODO.md - Replace malformed line with proper task list structure
2. Generate Master CSV
Create manifest_source_master.csv with these columns:
conversation_id (internal ID)
normtime_name (normalized: YYYY-MM-DD_HHMMSS_title.json)
create_time (ISO format after seconds→ms conversion)
turn_count (number of messages)
first_100_chars (first message preview)
last_100_chars (last message preview)
source_hash (SHA256 of full conversation JSON)
status (new, existing, duplicate)
3. Run Filename Matching
[ ] Scan current directory for existing .json files
[ ] Generate normtime_name for each of 242 conversations
[ ] Mark status as existing if file already exists, new otherwise
[ ] Output: filename_matching_report.csv
4. Explain Deterministic Seeding
"Seeding" = Using the same random starting point to get identical results every time.
5 seeds = 5 different hash variations (for audit trail):
Seed 0: Hash of full conversation
Seed 1: Hash of messages array only
Seed 7: Hash of first+last message pair
Seed 42: Hash of filename (normtime_name)
Seed 100: Hash of timestamp-normalized version
Why? Creates reproducible signatures. Run it today or next year, same input = same hash output.
📁 CSV Merge Strategy
You have:
manifest_original.csv (first batch)
manifest_stage4.csv (processed results)
Solution: Master-Slave Merge
Load both CSVs into pandas
Use normtime_name as the merge key (unique identifier)
Preview mode first: Generate merge_preview.csv showing conflicts
Decision logic:
If same normtime_name exists in both → Keep stage4 version (more complete)
If only in original → Copy to master with status: imported
If only in stage4 → Keep as-is with status: processed
Output: manifest_source_master.csv (single source of truth)