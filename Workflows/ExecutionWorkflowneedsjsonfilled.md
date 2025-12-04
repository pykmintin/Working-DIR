# Action Agent Execution Workflow v2

## Introduction
This document provides a copy‑paste‑optimized workflow template for document assembly operations. It defines seven human interaction points, each delivering immediate prose guidance paired with static JSON schemas for verification. All initialization logic is embedded in Step 1, and no domain‑specific runtime logic appears in main sections.

## Step 1: Synthesizer
### Prose
The Synthesizer converts disordered source materials into structured insight through iterative reasoning and self‑critique. It extracts core facts, identifies contradictions, surfaces the most expensive problem, and drafts a brief for the next agent. This phase follows enterprise prompt architecture principles (per L1) and uses condensed blueprint patterns (per L7) to ensure consistency.

### JSON Schema (Documentation Only)
```json
{
  "phase": "synthesizer",
  "purpose": "Convert disorder into structured insight",
  "core_functions": ["extract_facts", "identify_contradictions", "surface_expensive_problem", "draft_brief", "self_critique"],
  "output_format": "JSON with explainer_version, draft_brief, self_critique, feedback_request",
  "learning_references": "L1, L7",
  "documentation_only": true
}
```

## Step 2: Brief Architect
### Prose
The Brief Architect distills structured insight into a clean problem specification. It asks exactly two clarifying questions, defines constraints, and emits a copy‑paste‑ready JSON brief. It never prescribes technical solutions—its job is "what to fix," not "how." This maintains the minimalist focus required by R4.

### JSON Schema (Documentation Only)
```json
{
  "phase": "brief_architect",
  "purpose": "Distill insight into problem specification",
  "core_functions": ["ask_two_questions", "define_constraints", "emit_json_brief"],
  "rules": ["no_technical_prescription", "exactly_two_questions", "copy_paste_ready"],
  "output_format": "JSON with clarified_goal, action_agent, constraints, user_approved",
  "documentation_only": true
}
```

## Step 3: Prompt Generation
### Prose
The Prompt Generation phase translates the refined brief into a structured prompt template using principles from learning.json. It applies enterprise prompt architecture patterns (L1) to ensure modularity, cost control, and reproducibility. It references condensed blueprints (L7) for consistent structure and embeds validation layers per L5. This phase is explicitly inserted per user strategy to fill the gap between Brief Architect and Action Agent.

### JSON Schema (Documentation Only)
```json
{
  "phase": "prompt_generation",
  "purpose": "Translate brief into structured prompt template",
  "learning_references": "L1, L5, L7, L8",
  "core_principles": ["modular_design", "cost_control", "reproducibility", "validation_layers"],
  "output_format": "JSON with prompt_template, validation_rules, fallback_strategies",
  "insertion_rationale": "Explicitly added per system_facts[0] to bridge Brief Architect and Action Agent",
  "documentation_only": true
}
```

## Step 4: Action Agent
### Prose
The Action Agent operates exclusively in the Specification → Document Assembly cognitive domain. It transforms brief_for_next_agent JSON into a structured, copy‑paste‑optimized markdown document. It generates complete workflow documentation with dual-format output, embeds initialization logic sequentially, and ensures domain-agnostic shape per R7.

### JSON Schema (Documentation Only)
```json
{
  "phase": "action_agent",
  "purpose": "Transform brief into structured markdown document",
  "cognitive_domain": "Specification → Document Assembly",
  "core_functions": ["generate_skeleton", "assemble_human_points", "populate_content", "audit_rubrics", "generate_verification"],
  "locked_terminology": ["Synthesizer", "Brief Architect", "Action Agent", "Critic Agent(s)", "Knowledge Base"],
  "output_format": "Markdown with prose+JSON per Step",
  "documentation_only": true
}
```

## Step 5: Critic Agent(s)
### Prose
Critic Agent(s) evaluate the assembled document for drift, simplification opportunities, and structural compliance. They measure verification time, identify misalignment with goals, and assess whether the workflow can be simplified or reused. If verification exceeds 30 minutes, they trigger a simplification rule per the constitutional constraint.

### JSON Schema (Documentation Only)
```json
{
  "phase": "critic_agents",
  "purpose": "Evaluate document for drift and simplification",
  "review_dimensions": ["verification_time", "goal_alignment", "simplification_opportunity", "structural_compliance"],
  "trigger_rules": {
    "simplification_rule": "verification_minutes > 30",
    "reuse_threshold": "similarity > 0.8"
  },
  "output_format": "CSV row with verification_minutes, has_drift, failure_mode, simplified",
  "documentation_only": true
}
```

## Step 6: Knowledge Base
### Prose
The Knowledge Base searches past workflows for >80% similarity before creating new ones. When matches are found, it copies and renames the workflow, logging reuse with verification_minutes=0. Over time, execution signals feed a constitution that auto-enforces constraints. It maintains constitutional rules per L3's self-hardening framework.

### JSON Schema (Documentation Only)
```json
{
  "phase": "knowledge_base",
  "purpose": "Enable workflow reuse and governance evolution",
  "core_functions": ["search_past_workflows", "copy_and_rename_on_match", "log_reuse", "evolve_constitution"],
  "similarity_threshold": 0.8,
  "constitutional_references": "L3, L4",
  "output_format": "Updated signals.csv and constitution.json",
  "documentation_only": true
}
```

## Step 7: Final Verification
### Prose
Final Verification confirms the document contains no domain-specific logic in main sections, all 7 Steps follow the prose+JSON pattern, the prompt generation phase is explicitly defined, and the verification command passes. It executes the structure validation command and logs the result to signals.csv.

### JSON Schema (Documentation Only)
```json
{
  "phase": "final_verification",
  "purpose": "Confirm all success criteria met",
  "validation_checks": [
    "no_domain_logic_in_main",
    "seven_human_points_with_dual_format",
    "prompt_generation_explicitly_defined",
    "verification_command_passes"
  ],
  "command": "grep -q '^# Action Agent' ExecutionWorkflow_v2_template.md && grep -q '```json' ExecutionWorkflow_v2_template.md && grep -q '## APPENDIX B' ExecutionWorkflow_v2_template.md && echo PASS || echo FAIL",
  "log_destination": "signals.csv",
  "documentation_only": true
}
```

## APPENDIX B: Optional Reference Implementations
### Example B.1: Generic Execution Pattern
```python
# Tutorial-level code - unverified implementation
def example_task():
    # Placeholder for domain-specific logic
    pass
```

### Example B.2: Alternative Domain Template
```python
# Tutorial-level code - unverified implementation
def example_check():
    # Placeholder for domain-specific logic
    pass
```

### Final Verification Command
```bash
grep -q '^# Action Agent' ExecutionWorkflow_v2_template.md && grep -q '```json' ExecutionWorkflow_v2_template.md && grep -q '## APPENDIX B' ExecutionWorkflow_v2_template.md && echo PASS || echo FAIL
```
