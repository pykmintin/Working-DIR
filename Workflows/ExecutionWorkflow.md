# Execution Workflow

## Intro/Purpose

A unified, noise‑tolerant execution framework that converts raw, disordered system artifacts into verified operational improvements through five specialized stages. This document merges the operational depth of vTRI (tri‑mode execution) with the clarity of Unified Version schemas, preserving every unique detail from seven source documents while eliminating redundancy.

**Use this workflow when:**
- You have >3 artifacts (logs, blueprints, code, notes) that contradict or overwhelm
- You need a clear brief for a specialized agent but cannot extract it manually
- You require Web UI copy‑paste prompts, Python/inline commands, or Process‑level understanding
- You want to measure execution drift and evolve governance rules automatically

**Do NOT run this when:**
- You already have a single, clear, up‑to‑date task that bypasses synthesis
- All artifacts are >1 month old and the system has materially changed

**Locked Entity Names Used Throughout:**
- **Synthesizer** (cognitive extraction)
- **Brief Architect** (problem structuring)
- **Action Agent** (operational planning)
- **Critic Agent(s)** (reflection & drift analysis)
- **Knowledge Base** (adaptive governance)

---

## 1. Synthesizer

### 🧠 Conceptual Mode
Purpose: Convert disorder into structured insight through iterative reasoning and self‑critique.  
Cognitive Shift: *Chaos → Structured Understanding*

The Synthesizer performs noise‑tolerant synthesis with a built‑in feedback loop. It extracts 3–5 core facts, identifies contradictions, surfaces the most expensive problem, drafts a brief for the next agent, and immediately critiques its own draft. This defense‑in‑depth approach ensures that missing facts, overconfident assumptions, and unclear verification steps are flagged before human review.

### 💬 UI Mode – Three‑Turn Protocol

**Turn 1: Initial Synthesis & Self‑Critique**  
**Your Input:** Paste all messy documents below this prompt. No organization required.

**Prompt:**
You are Synthesizer. Extract 3–5 core facts, contradictions, and the most expensive problem. Draft and critique your own brief.


**Turn 1 Output (MANDATORY):**
```json
{
  "explainer_version": "v2.0_turn1",
  "draft_brief": {
    "system_state_digest": {
      "core_facts": [
        {"fact": "...", "value": "...", "source": "..."}
      ],
      "most_expensive_problem": {
        "issue": "...",
        "cost": "...",
        "blocks": "..."
      },
      "contradictions": [
        {"topic": "...", "doc1_says": "...", "doc2_says": "..."}
      ],
      "unknowns": ["...", "..."]
    },
    "prescription": {
      "problem_to_solve": "...",
      "agent_family": "...",
      "one_artifact": "...",
      "one_verification": "...",
      "success_criteria": "..."
    }
  },
  "self_critique": {
    "missing_facts": ["I didn't check X", "I assumed Y without evidence"],
    "overconfident_assumptions": ["Assumed Z based on old logs"],
    "unclear_to_human": ["Verification step is vague because..."]
  },
  "feedback_request": "What did I miss? Which assumption is wrong? Is the verification step clear?"
}
Turn 2: Feedback Parsing & Revision
Your Input: Natural language feedback.
Feedback Parsing Rules: The system interprets your feedback using five categories:
Corrections — You provide accurate information (e.g., "GPU VRAM is 2.8GB").
Clarifications — You express confusion or request precision.
Scope Additions — You ask for extra elements such as fallbacks or edge‑case handling.
Rejections — You instruct a restart from Turn 1 with a new focus.
Approvals — You indicate readiness to move to Turn 3.
Turn 2 Output (MANDATORY):
JSON

{
  "explainer_version": "v2.0_turn2",
  "revised_brief": {
    "system_state_digest": {
      "core_facts": [...],
      "most_expensive_problem": {...},
      "contradictions": [...],
      "unknowns": [...]
    },
    "prescription": {
      "problem_to_solve": "...",
      "agent_family": "...",
      "one_artifact": "...",
      "one_verification": "SPECIFIC: Run X, see Y in queue_log.jsonl",
      "success_criteria": "...",
      "fallbacks": { "if_webhook_key_missing": "use_placeholder_key" }
    }
  },
  "feedback_applied": [
    {
      "type": "correction",
      "field": "system_state_digest.core_facts",
      "old_value": "GPU VRAM unknown",
      "new_value": "GPU VRAM 2.8GB",
      "source": "Section 4"
    }
  ],
  "remaining_uncertainties": ["Still unclear why paths are defined but unused"],
  "feedback_request": "Better? What's still off? Any final adjustments?"
}
Turn 3: Final Polishing & Handoff
Your Input: Any final polish requests or "Proceed".
Turn 3 Output (FINAL):
JSON

{
  "explainer_version": "v2.0_final",
  "brief_for_next_agent": {
    "agent_family": "...",
    "problem_statement": "...",
    "one_artifact": "...",
    "one_verification": "...",
    "success_criteria": "...",
    "fallbacks": {...},
    "context": {
      "system_facts": [{"fact": "...", "value": "...", "source": "..."}],
      "contradictions": [],
      "unknowns": ["..."]
    }
  }
}
Your Action: Copy this JSON into the next session with the target agent.
💻 Filesystem/Python Mode
bash

# Tutorial-level code - unverified implementation

# Turn 1: Initial synthesis from artifact directory
python synth.py --input artifacts/ --output synth_turn1.json

# Turn 2: Incorporate feedback
python synth.py --input synth_turn1.json --feedback feedback.txt --output synth_turn2.json

# Turn 3: Final brief
python synth.py --input synth_turn2.json --final --output briefs/today.json
2. Brief Architect
🧠 Conceptual Mode
Purpose: Distill structured insight into a clean problem specification with defined constraints.
Cognitive Shift: Understanding → Specification
The Brief Architect acts as the router: it asks exactly two clarifying questions, selects one Action Agent based on your answers, and emits a copy‑paste‑ready JSON brief. It never prescribes technical solutions—its job is "what to fix," not "how."
💬 UI Mode
Prompt:
You are Brief Architect. Ask exactly two clarifying questions, define constraints, and output the JSON brief.
Self‑Critique Checklist (perform first):
[ ] Am I asking >2 questions? If yes, delete extras.
[ ] Am I prescribing a technical solution? If yes, stop.
[ ] Is the brief copy‑paste ready? If not, reformat to a single JSON block.
Example Interaction:
You (pasting goal): "CoreLink GPU blocks when WhisperX runs. Fix it."
Brief Architect Response:

Q1: Do you want to eliminate GPU blocking, or just reduce queue wait time?
Q2: Should the solution work for v6.3.15 as-is, or are you okay migrating to v6.3.16?

# After you answer:
{
  "clarified_goal": "Eliminate GPU blocking during WhisperX inference by implementing preemption checks in v6.3.16 executor",
  "action_agent": "Infrastructure Architect",
  "constraints": ["Must not break save_file actions", "Must log preemption events to queue_log.jsonl"],
  "user_approved": false
}
Output Format:
JSON

{
  "clarified_goal": "...",
  "action_agent": "...",
  "constraints": ["...", "..."],
  "user_approved": false
}
💻 Filesystem/Python Mode
bash

# Tutorial-level code - unverified implementation

python brief.py --input briefs/today.json --output briefs/today_refined.json
Expected Output:
JSON

{
  "clarified_goal": "Optimize data flow",
  "action_agent": "Infrastructure Architect",
  "constraints": ["time_limit=24h", "memory<4GB"],
  "user_approved": true
}
3. Action Agent
🧠 Conceptual Mode
Purpose: Translate structured intent into a minimal, verifiable action plan with embedded validation and resilience.
Cognitive Shift: Specification → Action
The Action Agent designs the smallest possible fix—no more than one file change and 30 lines of code. It wraps solutions in try/except blocks that log to queue_log.jsonl and provides a single, clear verification step: "Run X, then run Y, expect Z."
💬 UI Mode
Prompt:
You are Action Agent. Generate a five-step plan with verification tags, fallbacks, and self-critique.
Self‑Critique Requirements:
[ ] Does my fix require >1 file change? If yes, simplify to one file.
[ ] Did I leave out error handling? If yes, add try/except that logs to queue_log.jsonl.
[ ] Is the verification step clear enough for a non-expert? If no, rewrite it as: "Run X, then run Y, expect Z."
GPU Blocking Example (Tutorial‑Level Code):
Python

# Tutorial-level code - unverified implementation
# CoreLink Fix: GPU Preemption
# Paste this into Scripts/corelink_executor.py

import psutil  # Add to blueprint dependencies

def gpu_preempt() -> bool:
    """Check if GPU is busy. Returns True if safe to proceed."""
    # Mock: In real code, check nvidia-smi or process list
    for proc in psutil.process_iter(['pid', 'name']):
        if 'whisperx' in proc.info['name'].lower():
            return False
    return True

# Wrapper for WhisperX actions:
def execute_whisperx_safe(action):
    if not gpu_preempt():
        log_event({"event_type": "gpu_busy", "action_blocked": action})
        return {"status": "blocked", "retry_after_ms": 500}
    return execute_subprocess(action)

# Manual verification: Run a test queue with WhisperX, then run:
# grep "gpu_busy" Scripts/logs/queue_log.jsonl
# Expected: 1 line showing the block event
Output Format:
Python

# Tutorial-level code - unverified implementation
# CoreLink Fix: GPU Preemption
# Paste into Scripts/corelink_executor.py

def gpu_preempt():
    # Your code here (30 lines max)

# Manual verification: [single sentence]
# Confirm via: grep "gpu_preempt" Scripts/logs/queue_log.jsonl
💻 Filesystem/Python Mode
bash

# Tutorial-level code - unverified implementation

python action.py --input briefs/today_refined.json --output workflows/today.txt
4. Critic Agent(s)
🧠 Conceptual Mode
Purpose: Evaluate execution accuracy, identify misalignment between expected and actual outcomes, and measure drift.
Cognitive Shift: Evidence → Insight
Critic Agent(s) operate post‑execution to generate objective signals. They answer: Did verification take longer than 30 minutes? Did the solution drift from the original goal? What was the failure mode? Should this workflow be simplified or reused?
💬 UI Mode
Prompt:
You are Critic Agent. Evaluate drift, simplification, and success metrics. Output as CSV.
Execution Review Process:
Open the executed workflow: workflows/today.txt
Record:
verification_minutes: ___ (time spent verifying)
has_drift: yes/no (did outcome match goal?)
failure_mode: none / missed_edge_case / prescriptive_solution / etc.
simplified: yes/no (could this be shorter?)
Append the row to signals.csv
Manual Review Trigger: If verification exceeds 30 minutes, the rule is: Simplify before next run. This is logged as a constitutional constraint.
💻 Filesystem/Python Mode
bash

# Tutorial-level code - unverified implementation

python critic.py --input logs/today.json --output signals.csv
Output Example:
csv

workflow_id,verification_minutes,has_drift,failure_mode,simplified
workflow_today.txt,22,no,none,yes
workflow_tuesday.txt,25,yes,missed_edge_case,no
5. Knowledge Base
🧠 Conceptual Mode
Purpose: Transform execution signals and insights into adaptive governance rules and searchable institutional memory.
Cognitive Shift: Insight → Evolution
The Knowledge Base prevents re‑solving solved problems. When a new goal arrives, it searches past workflows for >80% similarity. If found, it copies and renames the workflow (today_v2.txt) and logs reuse in signals.csv. Over time, signals feed a constitution that auto‑enforces constraints.
💬 UI Mode
Workflow Reuse Command:
bash

cd C:\Meta_Architect
findstr "keyword" workflows\*.txt
If similar workflow found (>80% match):
Copy: copy workflows\monday.txt workflows\today_v2.txt
Log reuse in signals.csv with workflow_id=today_v2.txt,verification_minutes=0,has_drift=reuse
Governance Update Prompt:
You are Knowledge Base. Summarize all signals from signals.csv and propose new governance rules. Output updated constitution.json.
💻 Filesystem/Python Mode
bash

# Tutorial-level code - unverified implementation

# Summarize signals into metrics
python knowledge.py --signals signals.csv --metrics metrics/summary.json

# Evolve constitutional constraints
python constitution.py --update metrics/summary.json --output constitution.json
5a. Signals CSV Template
Mandatory Fields:
csv

workflow_id,verification_minutes,has_drift,failure_mode,simplified
Example Data:
csv

workflow_monday.txt,15,no,none,yes
workflow_tuesday.txt,25,yes,missed_edge_case,no
workflow_wednesday_reuse.txt,0,reuse,none,none
Logging Protocol: Append one row per executed or reused workflow immediately after verification. Empty or malformed rows invalidate the Knowledge Base update cycle.
5b. Constitution
Adaptive Constitution Example (Tutorial‑Level JSON):
JSON

{
  "RULE_1": "Always validate inputs before Synthesizer run.",
  "RULE_2": "Simplify workflows exceeding 30min verification.",
  "RULE_3": "Auto-retrigger Synthesizer when drift_rate > 0.3",
  "RULE_4": "Ensure ≥30% workflow reuse by Week 2.",
  "RULE_5": "Never start without checking failures.txt"
}
Evolving Process: The constitution is read by all agents before each session. New rules are proposed by the Knowledge Base after every 5 workflow executions and require manual approval via user_approved: true flag before becoming active.
Emergency Commands & Lean Runbook
Entities Recap:
Brief Architect – converts clarified goals into JSON briefs.
Action Agent – designs 5‑step workflows with verification.
Critic Agent(s) – you, reviewing workflows with fresh eyes.
Knowledge Base – your folder of past workflows C:\Meta_Architect\.
File Structure (Create This):

C:\Meta_Architect\
  briefs\
  workflows\
  logs\
  signals.csv
  constitution.json
Quick Start:
Brief Architect: Paste 2‑sentence summary → save as briefs\today.json
Action Agent: Paste brief → save workflow as workflows\today.txt
Critic Review: Next session, open workflows/today.txt and log metrics to signals.csv
Knowledge Base: Search for reuse before creating new workflows
EmergencyCommands:
Format drift: Type RESET in any session to restart Synthesizer Turn 1 with empty context.
Lost: Check constitution.json for current rules.
Low SNR: Stop generating; run Critic Agent review instead.

# Verification Command (run in repository root)
grep -q '^## 5. Knowledge Base' ExecutionWorkflow.md && \
grep -q '^### 5a' ExecutionWorkflow.md && \
grep -q '^### 5b' ExecutionWorkflow.md && \
echo PASS || echo FAIL