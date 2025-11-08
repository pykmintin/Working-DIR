# Working-DIR: ChatGPT Conversation Processor

## Overview
**Repository:** https://github.com/pykmintin/Working-DIR   
**Source Data:** `conversations.json` (85MB, 242 conversations, Nov 2025)  
**Goal:** Build manifest system + deduplication pipeline

## Quick Start
1. Place `conversations.json` in project root
2. Load `PROMPT.md` into CoreLink to initialize context
3. Execute tasks in priority order (see PROMPT.md)

## Key Concepts

### Normalized Naming (normtime_name)
Universal identifier format: `YYYY-MM-DD_HHMMSS_title.json`

### Deterministic Seeding
Creates reproducible hash signatures using 5 variations (Seed 0-100)

### CSV Merge Strategy
Master-slave merge using `normtime_name` as key

## File Structure
## ENVIRONMENT
CoreLink v3.7b structure: `ROOT\\Scripts\\{CoreLink.py, logs/, ChatLogs/, Reports/, *.py modules}`

## OUTPUT RULES
- Single-step scripts preferred
- Use `normtime_name` as universal identifier
- Keep responses lean and actionable
- Maintain rolling task lists

## KEY FILES
- `chat_processor.py` - Main entry point
- `Files/CoreLink.py` - Core logic bridge
- `Files/DupeChecker.py` - Duplicate detection (CRITICAL: must return dict, not bool)
- `test_suite.py` - Line 17 needs dict handling fix
- `TODO.md` - Malformed task list needs repair