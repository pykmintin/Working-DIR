#!/usr/bin/env python3
"""
Chat History Reconstructor v3.0 - Memory Reconstruction Core
Handles: duplicate detection, topic extraction, keyword generation, uncertainty flagging
"""
import os, re, json, csv, uuid, hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Any

# ──────────────────────────────────────────────────────────────
# CONSTANTS
# ──────────────────────────────────────────────────────────────
MANIFEST_CSV = "manifest_export_wide.csv"
PENDING_JSON = "pending_manifest.json"
INDEX_JSON = "conversations_index.json"
DISCARDED_LOG = "discarded_turns_log.json"
UNCERTAIN_LOG = "uncertain_classifications.json"

# Ensure files exist
for f in [PENDING_JSON, INDEX_JSON, DISCARDED_LOG, UNCERTAIN_LOG]:
    Path(f).touch(exist_ok=True)

# ──────────────────────────────────────────────────────────────
# CONVERSATION SPLITTING ENGINE (MS_001)
# ──────────────────────────────────────────────────────────────
def split_conversations(raw_text: str) -> List[str]:
    """
    Detect format by scanning first 1000 chars and split conversations accordingly:
    - Kimi format: 'User:\s' and 'Kimi:\s' found → split by '\n\n'
    - ChatGPT export: '###CHATGPT###' found → split by '###CHATGPT###'
    - Generic separator: '---' separator line found → split by '\n---\n'
    - If no delimiters → return [raw_text] as single conversation
    - Preserve all content, don't strip whitespace
    """
    # MS_003: Pre-compute failure handling - scan first 1000 chars
    sample_text = raw_text[:1000] if len(raw_text) >= 1000 else raw_text
    
    # Check for Kimi format
    kimi_pattern = r'User:\s.*\nKimi:\s'
    if re.search(kimi_pattern, sample_text):
        # Split by double newline (Kimi format)
        conversations = re.split(r'\n\n', raw_text)
        # Filter out empty conversations but preserve whitespace within content
        return [conv for conv in conversations if conv.strip()]
    
    # Check for ChatGPT export format
    if '###CHATGPT###' in sample_text:
        conversations = raw_text.split('###CHATGPT###')
        # Filter out empty conversations but preserve whitespace within content
        return [conv for conv in conversations if conv.strip()]
    
    # Check for generic separator
    if re.search(r'\n---\n', sample_text):
        conversations = re.split(r'\n---\n', raw_text)
        # Filter out empty conversations but preserve whitespace within content
        return [conv for conv in conversations if conv.strip()]
    
    # MS_003: If no patterns found, return single conversation (don't crash)
    return [raw_text]

# ──────────────────────────────────────────────────────────────
# MANIFEST ENTRY GENERATION (MS_002)
# ──────────────────────────────────────────────────────────────
def generate_manifest_entry(raw_text: str) -> Tuple[dict, str, dict]:
    """
    Process raw_text to generate manifest entry:
    - Call split_conversations() first
    - Use first conversation only (index [0])
    - Extract User:/Kimi: pairs using regex
    - Build entry dict with id, title, messages, signatures
    - Extract code blocks with metadata
    - Return tuple: (entry, formatted_text, code_blocks_dict)
    """
    # Split conversations and use first one
    conversations = split_conversations(raw_text)
    first_conversation = conversations[0] if conversations else ""
    
    # Extract User:/Kimi: pairs using regex
    # MS_004: If regex fails to extract any pairs, return empty structures
    message_pairs = re.findall(r'User:\s*(.+?)\nKimi:\s*(.+?)(?:\n|$)', first_conversation, re.DOTALL)
    
    # MS_004: Handle regex failure case
    if not message_pairs:
        empty_entry = {
            "id": str(uuid.uuid4()),
            "title": "Empty",
            "messages": [],
            "signatures": [],
            "topics": [],
            "keywords": []
        }
        return (empty_entry, "", {})
    
    # Build entry dict
    entry_id = str(uuid.uuid4())
    
    # Get first user message for title (max 50 chars)
    first_user_message = message_pairs[0][0] if message_pairs else ""
    title = first_user_message[:50] if first_user_message.strip() else "Untitled"
    
    # Build messages list with role, content, timestamp, turn_id
    messages = []
    for i, (user_msg, kimi_msg) in enumerate(message_pairs):
        # User message
        messages.append({
            "role": "user",
            "content": user_msg.strip(),
            "timestamp": datetime.now().isoformat(),
            "turn_id": i + 1
        })
        # Kimi message
        messages.append({
            "role": "assistant",
            "content": kimi_msg.strip(),
            "timestamp": datetime.now().isoformat(),
            "turn_id": i + 1
        })
    
    # Generate signatures
    signatures = generate_conversation_signature(first_conversation)
    
    # Create entry dict
    entry = {
        "id": entry_id,
        "title": title,
        "messages": messages,
        "signatures": signatures,
        "timestamp": datetime.now().isoformat()
    }
    
    # Extract code blocks via regex
    code_blocks = {}
    code_matches = re.findall(r'```(\w+)?\n(.*?)```', first_conversation, re.DOTALL)
    
    for idx, (language, code) in enumerate(code_matches):
        if code.strip():  # Only process non-empty code blocks
            block_id = f"code_block_{idx + 1}"
            lines = code.split('\n')
            line_count = len([line for line in lines if line.strip()])  # Count non-empty lines
            
            code_blocks[block_id] = {
                "language": language.strip() if language else "unknown",
                "line_count": line_count,
                "description": code[:80].strip(),  # First 80 chars
                "hash": hashlib.md5(code.encode()).hexdigest()[:16],
                "full_code": code  # Store full code for reference
            }
    
    # Format the entry as human-readable text
    formatted_text = format_strict_human_readable(entry)
    
    return (entry, formatted_text, code_blocks)

# ──────────────────────────────────────────────────────────────
# DUPLICATE DETECTION ENGINE
# ──────────────────────────────────────────────────────────────
def generate_conversation_signature(text: str) -> List[str]:
    """Generate 10 unique signatures from chat turns (4-5 word snippets)"""
    # Extract User:Assistant turn pairs
    turns = re.findall(r'User:\s*(.+?)\nAssistant:\s*(.+?)(?:\n|$)', text[:3000])
    signatures = []
    
    for user_turn, assist_turn in turns[:10]:  # First 10 turns
        # Take first 4-5 words from each turn
        user_snippet = ' '.join(user_turn.split()[:5])
        assist_snippet = ' '.join(assist_turn.split()[:5])
        if user_snippet and assist_snippet:
            signature = f"{user_snippet}|{assist_snippet}"
            signatures.append(hashlib.md5(signature.encode()).hexdigest()[:16])
    
    return signatures[:10]  # Exactly 10 signatures

def check_strict_duplicate(raw_text: str, threshold: int = 3) -> Tuple[bool, str, int]:
    """
    Check if conversation is duplicate using multi-signature matching
    Returns: (is_duplicate, existing_id, match_count)
    """
    signatures = generate_conversation_signature(raw_text)
    if not signatures:
        return False, "", 0
    
    if os.path.getsize(INDEX_JSON) == 0:
        return False, "", 0
    
    with open(INDEX_JSON, 'r', encoding='utf-8') as f:
        index = json.load(f)
    
    for conv_id, meta in index.items():
        if 'signatures' in meta:
            existing_sigs = meta['signatures']
            match_count = len(set(signatures) & set(existing_sigs))
            if match_count >= threshold:
                return True, conv_id, match_count
    
    return False, "", 0

# ──────────────────────────────────────────────────────────────
# TOPIC & KEYWORD EXTRACTION (LM-Driven)
# ──────────────────────────────────────────────────────────────
def extract_topics_and_keywords(text: str, user_intervention: bool = False) -> Dict[str, Any]:
    """
    Extract topics and keywords with uncertainty flags
    Uses pattern matching + LM-style heuristics
    """
    # Technical patterns (high confidence)
    tech_patterns = {
        'canvas': r'\b(Canvas|CANVAS)\b',
        'workflow': r'\b(Workflow|workflow|process|routine)\b',
        'startup': r'\b(Startup|startup|boot|initialize)\b',
        'shutdown': r'\b(Shutdown|shutdown|finalize|archive)\b',
        'core': r'\b(Core|CORE|system_architecture)\b',
        'schema': r'\b(schema|pydantic|yaml|json)\b',
        'automation': r'\b(automation|script|batch|powershell)\b',
        'logging': r'\b(logging|log|Operational Log|chatlog)\b'
    }
    
    # Conceptual patterns (medium confidence)
    concept_patterns = {
        'learning': r'\b(learning|reference|L[1-5]|Level [1-5])\b',
        'priority': r'\b(priority|P[0-3]|high|low|normal)\b',
        'integration': r'\b(integration|sync|bridge|API)\b',
        'memory': r'\b(memory|reconstruction|archive|index)\b'
    }
    
    topics = []
    keywords = []
    uncertain_flags = []
    
    # High confidence extraction
    for topic, pattern in tech_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            topics.append(topic)
            keywords.extend([m.lower() for m in matches])
    
    # Medium confidence (flag for review if found)
    for concept, pattern in concept_patterns.items():
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            topics.append(concept)
            keywords.extend([m.lower() for m in matches])
            uncertain_flags.append(concept)
    
    # Remove duplicates
    topics = list(set(topics))
    keywords = list(set(keywords))
    
    # If uncertainty threshold exceeded, flag for user
    needs_intervention = len(uncertain_flags) >= 3 and user_intervention
    
    return {
        "topics": topics,
        "keywords": keywords,
        "uncertain_flags": uncertain_flags,
        "needs_intervention": needs_intervention,
        "confidence_score": len([t for t in topics if t in tech_patterns]) / max(len(topics), 1)
    }

# ──────────────────────────────────────────────────────────────
# DISCARD & UNCERTAINTY LOGGING
# ──────────────────────────────────────────────────────────────
def log_classification_decision(
    conv_id: str, 
    decision: str,  # "keep", "flag", "discard"
    reason: str,
    topics: List[str],
    confidence: float
):
    """Log every classification decision for audit trail"""
    log_file = UNCERTAIN_LOG if decision == "flag" else DISCARDED_LOG
    
    entry = {
        "conv_id": conv_id,
        "timestamp": datetime.now().isoformat(),
        "decision": decision,
        "reason": reason,
        "topics": topics,
        "confidence": confidence,
        "user_overridden": False  # Set to True if user changes decision
    }
    
    existing = []
    if os.path.getsize(log_file) > 0:
        with open(log_file, 'r', encoding='utf-8') as f:
            existing = json.load(f)
    
    existing.append(entry)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(existing, f, indent=2)

# ──────────────────────────────────────────────────────────────
# STRICT FORMATTING ENGINE
# ──────────────────────────────────────────────────────────────
def format_strict_human_readable(entry: Dict) -> str:
    """Format with strict turn-by-turn structure"""
    output = f"{{Header: {entry['title']}}}\n"
    output += f"ID: {entry['id']}\n"
    output += f"Timestamp: {datetime.now().isoformat()}\n"
    output += f"Topics: {', '.join(entry.get('topics', []))}\n"
    output += f"Keywords: {', '.join(entry.get('keywords', []))}\n\n"
    
    if 'messages' in entry:
        for i, msg in enumerate(entry['messages'], 1):
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '').strip()
            
            # Wrap turns clearly
            output += f"## Turn {i}\n"
            output += f"{role}: {content}\n\n"
    
    # Add code refs if present
    if 'code_blocks' in entry and entry['code_blocks']:
        output += "###[REF]###\n"
        for ref_id, block in entry['code_blocks'].items():
            output += f"###{ref_id}###\n"
            output += f"Language: {block['language']}\n"
            output += f"Lines: {block['line_count']}\n"
            output += f"Description: {block['description']}\n\n"
    
    return output

# ──────────────────────────────────────────────────────────────
# MAIN PROCESSING PIPELINE
# ──────────────────────────────────────────────────────────────
def process_chat_file(filepath: str, user_review_mode: bool = False) -> Dict[str, Any]:
    """
    Full pipeline: load → dedupe → extract topics → classify → format → log
    Returns result dict with classification decision
    """
    if not os.path.exists(filepath):
        return {"error": "File not found"}
    
    with open(filepath, 'r', encoding='utf-8') as f:
        raw_text = f.read()
    
    # Skip if too short
    if len(raw_text) < 500:
        return {"error": "Content too short"}
    
    # Check for duplicates
    is_dup, dup_id, match_count = check_strict_duplicate(raw_text)
    if is_dup:
        log_classification_decision(
            conv_id=str(uuid.uuid4()),
            decision="discard",
            reason=f"Duplicate of {dup_id} ({match_count} signature matches)",
            topics=[],
            confidence=1.0
        )
        return {"status": "duplicate_skipped", "duplicate_id": dup_id}
    
    # Extract topics and keywords
    extraction = extract_topics_and_keywords(raw_text, user_intervention=user_review_mode)
    
    # Classify relevance to CORE
    relevance_score = extraction['confidence_score']
    core_keywords = ['canvas', 'core', 'workflow', 'startup', 'shutdown', 'schema', 'automation']
    core_match = len([k for k in extraction['keywords'] if k in core_keywords])
    
    # Decision logic
    if core_match >= 3 and relevance_score >= 0.6:
        decision = "keep"
        reason = "High CORE relevance"
    elif extraction['needs_intervention']:
        decision = "flag"
        reason = "Uncertain classification - needs review"
    elif core_match == 0 and relevance_score < 0.3:
        decision = "discard"
        reason = "Low CORE relevance"
    else:
        decision = "flag"
        reason = "Borderline relevance"
    
    # Generate manifest entry
    entry, formatted, code_blocks = generate_manifest_entry(raw_text)
    entry.update({
        "topics": extraction['topics'],
        "keywords": extraction['keywords'],
        "relevance_score": relevance_score,
        "core_matches": core_match,
        "classification": {
            "decision": decision,
            "reason": reason,
            "confidence": relevance_score
        }
    })
    entry['code_blocks'] = code_blocks
    
    # Log decision
    log_classification_decision(
        conv_id=entry['id'],
        decision=decision,
        reason=reason,
        topics=extraction['topics'],
        confidence=relevance_score
    )
    
    return {
        "status": decision,
        "entry": entry,
        "formatted": formatted,
        "duplicate_check": {"is_duplicate": False}
    }

# ──────────────────────────────────────────────────────────────
# COMMAND-LINE INTERFACE
# ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python chat_processor.py <chat_file.txt> [--review]")
        sys.exit(1)
    
    filepath = sys.argv[1]
    review_mode = "--review" in sys.argv
    
    result = process_chat_file(filepath, user_review_mode=review_mode)
    
    print(json.dumps(result, indent=2, default=str))