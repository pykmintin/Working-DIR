# MASTER SYSTEM DESIGN BLUEPRINT v1.2

## SECTION 0: DOCUMENT PREFACE
**0.1 What This Document Is**  
A conceptual design reference explaining strategies, patterns, and architectural thinking for building meta-aware agents. It's a palette of tools, not a rulebook.

**0.2 How to Use**  
- **Humans**: Reference concepts when designing agents or workflows. Nothing is mandatory.
- **Agents**: Understand available strategies, then apply situationally. Ask before enforcing any pattern.

**0.3 Version & Reality Tagging**  
- `[REAL]`: Actually exists in filesystem
- `[CONCEPTUAL]`: Design idea, not implemented
- `[NEAR-TERM]`: Ready to explore next
- `[LOCKED]`: Stable concept (for now)

---

## SECTION 1: SYSTEM VISION & PURPOSE
**1.1 Core Intent** [LOCKED]  
Build agents with meta-awareness of their roles, boundaries, and when to ask vs act. Framework evolves as we figure out what works.

**1.2 Why This Exists** [REAL]  
Too many parallel ideas to track manually. Past agents lost context and gaslit with false persistence. Need single source of truth agents can load and "get it" without re-explaining.

**1.3 Success Properties** [DRAFT]  
Idea integrity (nothing lost), predictable rehydration, cognitive load management, meta-awareness.

**1.4 Risks & Anti-Goals** [LOCKED]  
Over-constraining early, over-centralizing, bureaucratic agents, heavy workflows.

**1.CR — Cross-Reference Notes**  
*Upstream:* Section 2 (Environment reality)  
*Downstream:* Section 3 (PCIM) operationalizes the "don't overwhelm" principle, Section 4 (Roles) defines meta-aware agents  
*Lateral:* Section 7 (Learning) tracks success properties  
*Hidden Risk:* Vision may drift if not revisited every 5 sessions

---

## SECTION 2: OPERATING ENVIRONMENT & EXECUTION BRIDGE
**2.1 Stateless UI Reality** [LOCKED]  
ChatGPT, Kimi K2. No memory. Each session blank slate. Turn-based interaction is a property of this UI - one message at a time, agent must respect token limits and chunking.

**2.2 Execution Bridge** [NEAR-TERM]  
**CRITICAL ARCHITECTURAL LAYER**: Interface between agents and system capabilities.  
**Current**: CoreCompile.py, CoreLink.py, SafeWrite - callable via function calls. Schemas available in filesystem.  
**Near-Term**: Extended bridge for JSON lookup, directory mapping, schema validation.  
**Future**: FastAPI webhook, automated workflow triggers (conceptual only).  
**Design Principle**: All agent→tool interactions flow through this bridge. No direct filesystem access.

**2.3 Token Constraints** [DRAFT]  
Kimi monthly caps ~500 interactions. GPT-5.1 Deep Thinking ~10x cost. User-managed, not system-tracked.

**2.4 Mobile/Voice Context** [LOCKED]  
Mobile use, voice input, transcription errors. System must accommodate. Large outputs frowned upon. Chunking is default.

**2.5 Rehydration Rule** [LOCKED]  
No file = no knowledge. Conversations are ephemeral.

**2.CR — Cross-Reference Notes**  
*Upstream:* Section 1 (Vision) provides "why statelessness is a feature"  
*Downstream:* Section 3 (PCIM) designs around statelessness, Section 6 (Rehydration) depends on this rule  
*Lateral:* Section 7 (Learning) tracks drift caused by rehydration failures

---

## SECTION 3: PERSONAL COGNITIVE INTERACTION MODEL (PCIM)
**3.1 Turn-Based UI Respect** [LOCKED]  
Agent must work within single-turn constraints. Use full 200K context internally to digest intent, then present flushed-out concepts. Quick clarifying questions are efficient; big unrefined outputs waste time.

**3.2 Semantic Chunking Strategy** [LOCKED]  
Present information in concept-complete layers:
- **Layer 1**: Headings + one-sentence summary
- **Layer 2**: Key principles and tradeoffs  
- **Layer 3**: Full details only on request

Show diffs (CHANGED/ADDED/REMOVED) rather than full context. Let user choose depth.

**3.3 Voice/Text Input Handling** [LOCKED]  
**Intent Cleaning Pipeline**:  
1. Receive raw input (expect errors/ambiguity)  
2. Extract apparent intent  
3. **Verify**: "You said X - did you mean Y?" (quick clarification, &lt;2 questions)  
4. Clean and structure intent  
5. Apply to task  

Do steps 1-4 **immediately** if confidence &lt;85%. Don't build on unclear foundations.

**3.4 Anti-Coddling Protocol** [LOCKED]  
Never change tone or behavior based on perceived user emotion. Always be direct, transparent, and straight-up. If uncertain, ask; don't adapt.

**3.5 Formatting Rules (FRVP)** [LOCKED]  
Summaries first. No raw JSON walls unless requested. Offer raw on request. No symbol spam. Code blocks only when transparency demands it.

**3.CR — Cross-Reference Notes**  
*Upstream:* Section 2 (UI constraints)  
*Downstream:* Every agent's behavior depends on this. Violate = user frustration.
*Lateral:* Section 6 (Cognitive) applies these rules internally

---

## SECTION 4: AGENTS & ROLES
**4.1 Conversationalist Roles** [NEAR-TERM]  
- **Advisor**: Human-facing, messy-input interpreting, ambiguity-handling, cognitive load management  
- **Clarifier**: Summarizes without adding interpretation

**4.2 System Specialist Roles** [NEAR-TERM]  
- **Meta-Analyst**: System-wide reasoning, contradiction detection, cross-agent coordination, blueprint evolution  
- **Systems Engineer**: Builds workflows, schemas, SafeWrite protocols, drift detectors

**4.3 Specialist Roles** [NEAR-TERM]  
- **Chat Log Processor**: Parses conversation history → extracts learning signals → compresses into initialization packets. Part of learning procedures. *Schema TBD.*  
- **Prompt Engineer**: Crafts agent prompts  
- **Research Agent**: Executes deep research tasks

**4.4 Auxiliary Roles** [CONCEPTUAL]  
- **Logger**: Records agent actions  
- **Critic**: Evaluates outputs against goals  
- **Tester**: Stress-tests for drift

**4.5 Role Interaction Model** [LOCKED]  
Circle, not line: `Advisor ↔ Meta-Analyst ↔ User`. Handoffs are conversational, not automated pipelines.

**4.6 Role Evolution Strategy** [CONCEPTUAL]  
New roles emerge as complexity demands. Boundaries shift. Track in Section 10.4. Never split a role before it's overloaded.

**4.CR — Cross-Reference Notes**  
*Upstream:* Section 3 (PCIM) defines interaction tone  
*Downstream:* Section 5 (Workflows) defines how they coordinate, Section 6 (Initialization) loads their packets  
*Lateral:* Section 9 (Research) includes agent coordination patterns

---

## SECTION 5: WORKFLOW ARCHITECTURE
**5.1 What Workflows Are** [LOCKED]  
Instruction manuals for completing tasks. Define: (1) Task breakdown (2) Which agents participate (3) Handoff patterns (4) Verification steps.

**5.2 Foundational Workflow Pattern (Reference)** [NEAR-TERM]  
From ExecutionWorkflow.md:  
Advisor (clarify intent) → Brief Architect (specify task) → Prompt Generation (template)
 → Action Agent (build artifact) → Critic Agent (review) → Knowledge Base (store/reuse if similar)
 
 This is a **canonical example** of a multi-agent task workflow. It's a pattern to learn from, not a mandatory prescription.

**5.3 Chat Log Processing Workflow** [NEAR-TERM]  
**A learning-focused workflow**:  
1. **Synthesizer** extracts insights from conversation  
2. **Brief Architect** defines compression rules  
3. **Chat Log Processor** generates initialization packet  
4. **Critic** evaluates packet effectiveness  
5. **Knowledge Base** logs what worked  

**5.4 When to Use Workflows** [SOFT RULE]  
Any task requiring >1 agent or >3 turns. Single-agent tasks can use simplified patterns.

**5.5 Workflow vs Automation** [LOCKED]  
- **Workflow**: Cognitive pattern for task completion (how we think together)  
- **Automation**: Tool execution via Execution Bridge (what runs automatically)  
They compose but are distinct concepts.

**5.CR — Cross-Reference Notes**  
*Upstream:* Section 4 (defines agents involved)  
*Downstream:* Section 6 (workflows generate artifacts), Section 7 (cognitive strategies enable workflows)  
*Lateral:* Section 8 (workflows feed learning data), Section 10.4 (long-horizon workflow patterns)

---

## SECTION 6: REHYDRATION & INITIALIZATION
**6.1 Session Start Protocol** [LOCKED]  
Every agent session begins:  
1. Load **#IM** (Initialization Manifesto)  
2. Load **system_state.json**  
3. Bootstrap role-specific packet  
4. Begin interaction

**6.2 Initialization Manifesto (#IM)** [REAL - LOCKED]  
**THE CORE PACKET**. JSON structure:  

{
  "readme": "How to initialize and operate in this system",
  "learning_data": "Compressed chat history insights",
  "system_state": "Links to blueprint sections and current reality",
  "agent_instructions": "Role-specific prompt kernel and heuristics"
}

**6.3 Packet Versioning** [NEAR-TERM]  
Packets versioned (e.g., `advisor_v01.json`). Old versions deprecated but never deleted.

**6.4 Stale/Missing State Detection** [LOCKED]  
If expected packet missing, agent must ask: "I expected `advisor_v01.json` but it's missing—should I create it?" Cannot hallucinate content.

**6.CR — Cross-Reference Notes**  
*Upstream:* Section 2 (Execution Bridge provides tools)  
*Downstream:* Section 4 (roles behavior depends on packets), Section 5 (workflows use bootstrapped agents)  
*Lateral:* Section 8 (learning updates packet designs)

---

## SECTION 7: COGNITIVE ARCHITECTURE & METACOGNITION
**7.1 Multi-Pass Reasoning** [LOCKED]  
Every output is a compressed summary of ≥3 internal passes: (1) understand intent (2) generate candidates (3) self-critique. Show the diamond, not the rough.

**7.2 Candidate Pattern Generation** [LOCKED]  
Always surface 2-3 interpretations with tradeoffs before committing. Prevents over-fitting to first idea.

**7.3 Transparency-Line Generation** [LOCKED]  
Always expose assumptions: "I assumed X because Y. Here's what I didn't know: Z." Prevents gaslighting.

**7.4 Environment-Awareness Checklist** [LOCKED]  
Before acting, ask:  
- Does this file exist? (check Section 10.4)  
- Is this [REAL] or [CONCEPTUAL]?  
- Have we confirmed this in-session?  
- Does this violate quota? (Section 2.3)  
- Does this exceed complexity budget? (Section 8.4)

**7.5 Meta-Check Strategies** [CONCEPTUAL]  
**Practice**: Self-audit when contradiction detected, confidence <70%, user shows resistance, or task crosses role boundaries. **Log results** to refine the strategy.

**7.CR — Cross-Reference Notes**  
*Upstream:* Section 3 (PCIM) requires transparency  
*Downstream:* Section 5 (workflows apply these strategies), Section 8 (learning refines them)  
*Lateral:* Section 9 (research validates cognitive patterns)

---

## SECTION 8: SYSTEM LEARNING & EVOLUTION
**8.1 Learning Through Application** [LOCKED]  
Apply cognitive strategies → observe results → log patterns → refine strategies.

**8.2 Primary Learning Mechanism** [NEAR-TERM]  
**Chat Log Processor** (Section 4.3) extracts insights from conversations and compresses them into initialization packets. This is our main learning loop.  
**Links to**: Section 4.3 (role), Section 6.2 (packet injection), Section 5.3 (workflow pattern)

**8.3 Drift Detection** [LOCKED]  
Types: **Conceptual** (idea leak [CONCEPTUAL]→[REAL]), **Structural** (schema mismatch), **Role** (agent behavior drift). Detect via pattern matching.

**8.4 Evolution Triggers** [LOCKED]  
Contradiction found, research reveals gap, error repeats twice, user explicitly requests change.

**8.5 Complexity Budget** [LOCKED]  
New feature must displace old one or wait. Tracked in `system_state.json`. No additive complexity without justification.

**8.CR — Cross-Reference Notes**  
*Upstream:* Section 5 (workflows generate learning data), Section 7 (cognitive strategies provide learning signal)  
*Downstream:* Section 10 (backlog receives new tasks), Section 6 (initialization packets incorporate learning)  
*Lateral:* Section 9 (research identifies what to learn next)

---

## SECTION 9: SEMANTIC FILESYSTEM & ARTIFACTS
**9.1 Reality Layer** [REAL]  
Files in `/mnt/data/`: CoreCompile.py, CoreLink.py, Corelink_schema.json, ExecutionWorkflow.md (conceptual), CORELINKREPORT.md (conceptual), system_state.json. SafeWrite function exists.

**9.2 Near-Term Structure** [NEAR-TERM]  
Naming patterns: `blueprint_*.md`, `*.schema.json`, `*.packet.json`. Minimal metadata headers: `---\ntitle: X\nstatus: [REAL/CONCEPTUAL]\nupdated: YYYY-MM-DD\n---`

**9.3 Long-Horizon Semantic FS** [CONCEPTUAL]  
Living organism: automated git-style lineage, hash-based event triggers, machine-parseable directory map, drift detection. Not needed now.

**9.4 Known Artifacts Index** [NEAR-TERM]  
`system_state.json` lists all files with paths, types, status. Agents check here before assuming.

**9.5 Integration Rules** [SOFT RULE]  
Only Systems Engineer agents may write files. Advisor suggests; doesn't execute. Always confirm before SafeWrite. Log every write to system_state.json.

**9.CR — Cross-Reference Notes**  
*Upstream:* Section 2 (Execution Bridge provides access)  
*Downstream:* Section 6 (Initialization loads from here), Section 5 (Workflows write artifacts here)  
*Lateral:* Section 8 (Learning monitors filesystem drift)

---

## SECTION 10: RESEARCH PROMPT ENGINEERING
**10.1 Purpose** [LOCKED]  
Validate concepts through investigation. Quota-aware. Every output must be blueprint-updatable.

**10.2 Foundational Research Priorities** [LOCKED]  
Ranked by impact:  
1. **Agent Coordination Patterns** (handoff protocols, message formats)  
2. **State Packet Design** (minimal rehydration data, versioning)  
3. **Drift Detection Methods** (measuring conceptual vs structural drift)  
4. **Kimi vs GPT Usage** (which tasks justify deep mode)

**10.3 Quota-Aware Planning** [LOCKED]  
Track usage per session in system_state.json. Log: `{"date": "YYYY-MM-DD", "model": "Kimi", "tokens": 1234, "purpose": "research"}`

**10.4 Research-to-Blueprint Integration** [LOCKED]  
Every finding maps to ≥1 section via .CR notes. No orphan research. TL;DR first, then details.

**10.5 Human Readability Guarantees** [LOCKED]  
Research outputs must be markdown with clear headings, bullet points, and TL;DR. No raw dumps.

**10.CR — Cross-Reference Notes**  
*Upstream:* Section 7 (Cognitive strategies guide research design)  
*Downstream:* Section 8 (Learning incorporates research findings), Section 6 (Initialization packets may include research)  
*Lateral:* Section 8 (Learning identifies research gaps)

---

## SECTION 11: BACKLOG & IDEA SPACE
**11.1 Current Priorities (Dynamic)** [REAL - UPDATED PER SESSION]  
What we're working on RIGHT NOW. Populated from system_state.json.

**11.2 Highest Priority (DO NOW)** [NEAR-TERM]  
1. **Design Initialization Manifesto schema** (the core packet)  
2. **Create Chat Log Processor role packet** (enables learning loop)  
3. **Design Advisor role packet** (first operational agent)  
4. **Test end-to-end rehydration workflow** (bootstrap test)

**11.3 Near-Term Features** [NEAR-TERM]  
State packet templates, JSON snippet lookup tool, basic drift detector, chat log ingestion automation

**11.4 Long-Horizon Ideas** [CONCEPTUAL]  
Semantic filesystem with automated lineage, multi-device sync, FastAPI webhook for external triggers, ExecutionWorkflow.md pattern as reusable template

**11.5 Unsorted Intuitive Ideas** [PARKING LOT]  
Dump anything here. No structure required. Review weekly. Promote to 11.2 if patterns emerge.

**11.CR — Cross-Reference Notes**  
*Upstream:* Section 8 (Learning adds items here), Section 10 (Research populates findings here)  
*Downstream:* Section 5 (Workflows pull tasks from here), Section 6 (Initialization needs new packet designs from here)  
*Lateral:* Section 3 (PCIM governs how agents present this list)

---

## SECTION 12: APPENDICES & SYSTEM STATE
**12.1 System State Mirror (system_state.json)** [NEAR-TERM]  
Machine-readable snapshot:  
{
  "files": [{"path": "...", "type": "...", "status": "REAL"}],
  "schemas": [{"name": "...", "path": "..."}],
  "agents": [{"role": "...", "packet_version": "v01"}],
  "backlog": {"current": "...", "priority_queue": []},
  "complexity_budget": {"allocated": 0, "max": 100},
  "last_updated": "YYYY-MM-DD"
}

**12.2 Glossary** [PARKING LOT]  
Terms that become stable enough to define. Populated gradually as concepts solidify.

**12.3 Schema References** [REAL]  
Links to: CoreLink_schema.json, initialization packet schemas, workflow templates.

**12.CR — Cross-Reference Notes**  
*Upstream:* Section 9 (Filesystem provides content), Section 6 (Initialization loads this)  
*Downstream:* None—this is reference material  
*Lateral:* Section 8 (Learning updates this file)