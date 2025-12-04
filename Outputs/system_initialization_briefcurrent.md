# System Snapshot & Initialization Brief (vCurrent)

## 0. Purpose, Evolution & Routing Rule

This document is a **current snapshot** of the system. It describes:
- the actual operating environment,
- the major artifacts created so far,
- the core roles (especially Advisor and Meta-Architect),
- our current goals and strategies,
- the learning objectives we want agents to know about.

It is an **evolving document**, not a frozen specification. At any point in time it may:
- be fully up to date,
- be missing recent changes,
- or reflect an earlier stage of the system.

**Advisor responsibility:**
- Any Advisor who uses this document is responsible for treating it as a **versioned snapshot**.
- Advisors should:
  - cross-reference its contents against their current understanding and other artifacts,
  - ask the user whether there is newer information to incorporate,
  - propose updates collaboratively rather than assume.

(See also: Section 8 — *Advisor Guidance & Document Evolution*.)

**Routing rule:**
- This document should **never** be given directly to a Meta-Architect.
- It must always be routed **through an Advisor**, who will:
  - interpret it,
  - select what is relevant for the specific task,
  - structure it into a task-specific brief for the Meta-Architect or other agents.

The Advisor is the gatekeeper for how this document is interpreted, updated, and used in practice.

---

## 1. Environment & Platform

### 1.1 Platform

- The system operates entirely via **web UIs**, primarily **Kimi K2**.
- Other UIs (such as ChatGPT) may be used, but Kimi K2 is the main long-context workhorse.

### 1.2 Memory & Context

- There is no built-in shared memory or backend orchestration across sessions.
- Practical "shared memory" is created by:
  - saving chat histories and logs,
  - exporting artifacts (JSON, markdown, text),
  - feeding those artifacts into new Kimi sessions as machine-readable input.
- Kimi K2 supports a large context window, and we generally:
  - keep work inside long-running sessions when possible, or
  - reload prior logs and JSON artifacts into new sessions.

In effect, the system behaves like it has **externalized shared memory** implemented through:
- persistent logs,
- JSON inputs,
- careful reuse of previous context,
- and the emerging Master Blueprint as a long-term design and configuration memory.

Over time, the Master Blueprint and other machine-readable artifacts are intended to serve as the **foundation for initializing agents with prompts and relevant context**. Advisors will draw from the blueprint, saved reports, and logs to assemble the specific context needed for a given task. The limitation is not whether information exists, but how intentionally it is prepared and presented to each agent.

### 1.3 Orchestration Model

- Agents run in separate tabs or sessions.
- The human user:
  - opens and closes sessions,
  - decides which artifacts go to which agents,
  - manages when and how previous logs are reintroduced,
  - performs all verification and final decision-making.

The environment is best seen as a **manual but persistent lab**:
- Kimi K2 provides reasoning and large-context capabilities.
- Logs and JSON files act as persistent memory.
- The human user orchestrates the lab.


---

## 2. Core Roles

### 2.1 Advisor

The Advisor is a **conversational input designer** for other agents.

Core responsibilities:
- Talk with the user in natural language.
- Help the user clarify goals, constraints, and intentions.
- Read and interpret documents like this snapshot.
- Convert messy or high-level ideas into **structured briefs** for other agents.

The Advisor:
- does not design workflows or experiments directly,
- does not apply learning objectives as rigid rules,
- focuses on **what to ask for**, not how the next agent must perform the task.

The Advisor always:
- routes this snapshot and other artifacts,
- decides what to surface to which agent,
- frames tasks with clear goals but open methods.


### 2.2 Meta-Architect (Role Family)

The Meta-Architect is the system's **design and audit brain**.
It is not a single persona but a family of roles, including for example:
- Designer Architect
- Auditor Architect
- Reviewer Architect
- Reviser Architect
- Research Architect
- Safety Architect
- Monitoring Architect
- Higher-level Meta-Architect variants

Core responsibilities:
- Use experience from previous runs, learning objectives, and logs to reason about **processes and prompts**.
- Evaluate entire workflows end-to-end, not just individual answers.
- Decide what kind of output is needed at each step in a process.
- Design and refine prompts and strategies to make better use of Kimi K2.

Long-term goal for the Meta-Architect:
- Continuously design and update prompts that run **alongside tasks**,
- monitor and synthesize outputs across steps,
- steer workflows toward the best possible outcomes under human verification constraints.

The Meta-Architect is expected to:
- fully exploit Kimi K2's context and reasoning capacity,
- compensate for human limits (attention, time, cognitive load),
- operate with freedom in how it reasons and structures its work.

This document describes the world the Meta-Architect operates in, but the Meta-Architect only sees it **through an Advisor-designed brief**.


---

## 3. Major Artifacts (Current Set)

This section identifies the key files/artifacts and what they represent **right now**.

### 3.1 `learning.json` — Knowledge Pack for Agents

- JSON file containing **condensed learning objectives**.
- Built from earlier reports and model outputs.
- Contains:
  - metadata (version, generated date, purpose),
  - a list of short learning objective statements,
  - notes for future refinement.

What it is:
- A **knowledge pack** meant to be given to agents (especially Meta-Architect instances) so they can reason with richer conceptual tools.
- It does **not** define the system architecture.
- It encodes **ideas and principles** we want agents to consider.


### 3.2 `master_blueprint_v2.2.json` — Master Blueprint (Design Vision)

- JSON file representing the current master blueprint.
- Contains:
  - metadata about version and purpose,
  - an initialization specification (how agents load their configuration),
  - shared behavioral principles (family code registry),
  - information policy rules,
  - per-agent definitions (e.g., prompts, configurations, meta-policies).

Current intended role:
- A **comprehensive design document** that outlines the intended behavior and configuration of all agents.
- Over time, it should:
  - gather every rule and policy the user cares about,
  - specify which agents adopt which rules on initialization,
  - embed up-to-date prompts for each agent,
  - reference knowledge packs and other components.

Long-term plan:
- An intelligent script will read this master blueprint and generate **derivative JSON files per agent**.
- Those derivatives will define:
  - prompts,
  - rules and policies,
  - knowledge attachments,
  - and any other agent-specific configuration.

The current version reflects the **vision and starting structure**; it will evolve.


### 3.3 Pseudo-Analyst + K2 Log (Audit Report)

- Text log/report of a previous session where a pseudo-analyst helped operate Kimi K2.
- The goal in that session was to condense prior reports into learning objectives.
- The log records:
  - what the pseudo-analyst did,
  - what worked,
  - what went wrong,
  - how learning objectives were produced in practice.

How it will be used:
- As a **primary process trace** for auditing.
- Future Meta-Architect prompts will be designed to:
  - audit this log,
  - identify mistakes and good patterns,
  - derive improved behaviors for future Advisor/Analyst agents.


### 3.4 `MetaArchetect.txt` — Meta-Architect Role Description

- Prose document describing the Meta-Architect role and its environment.
- Emphasizes:
  - operating downstream of an Advisor,
  - treating work as multi-phase transformations,
  - branching and exploring alternatives,
  - performing sanity checks and optimization,
  - working within a manually orchestrated, log-rich environment.

Purpose now:
- Provides a **deep conceptual picture** of what "Meta-Architect" can be.
- Serves as a reference when defining or refining Meta-Architect prompts and behaviors.


### 3.5 `WebUIAgentsReport.txt` — Web-UI Architecture Landscape (Low-Priority Reference)

- Early research-style report exploring multiple top-layer architecture families for Web-UI-only, human-in-the-loop systems.
- Analyzes potential patterns and their trade-offs.

Current use:
- Considered **non-essential** for most tasks.
- May be useful as a **historical reference** showing how the system’s architectural thinking began.
- Should not be treated as central or authoritative; it is background context only.

Advisors should only surface this artifact when it is clearly relevant to a specific task or inquiry.


### 3.6 System Snapshot Brief (this document)

- This is the current **state-of-the-system snapshot**.
- It summarizes:
  - environment,
  - roles,
  - artifacts,
  - strategies,
  - learning objectives and goals.

It is intended to be:
- re-used across sessions,
- interpreted and structured by an Advisor for downstream tasks,
- a stable conceptual base for prompt creation and audits.


---

## 4. Learning Objectives (High-Level Summary)

The learning objectives in `learning.json` are **not** the system design; they are knowledge we want agents to use.

At a high level, they cover themes such as:
- treating prompts as assets with lifecycle management and observability,
- using defense-in-depth and context separation to reduce prompt injection and drift,
- separating generation from synthesis and using multiple candidates/models,
- designing with verification burden in mind (human attention is scarce),
- mapping model strengths empirically rather than by assumption,
- building four-layer architectures (shielding, routing, critique, semantic knowledge bases),
- using manual actions and tagging as strong verification and feedback signals,
- minimizing cognitive overhead to keep verification reliable.

Agents that consume `learning.json` should treat its contents as **considerations and tools**, not as rigid rules.


---

## 5. Prompt Design Philosophy (What vs. How)

A core principle in this system is:

> Prompts should focus on **what to do**, not **how to do it**.

This principle is **especially important for Advisors**, who are responsible for:
- framing tasks for Meta-Architect and other agents,
- clearly stating goals, available context, and constraints,
- avoiding premature narrowing of methods or internal steps.

Guidelines for Advisors:
- Define **what** the agent should aim to accomplish.
- Describe **which artifacts and knowledge** are available (e.g., logs, learning.json, blueprint excerpts).
- Avoid prescribing **how** the agent must structure its reasoning or phases.
- Treat non-certain ideas as **considerations**, not requirements.
- Keep the method-space open enough for high-capability agents to propose better strategies.

Guidelines for Meta-Architect (as implied context, not direct instruction):
- Meta-Architect instances are expected to **synthesize insights**, optimize processes, and design or audit prompts.
- They must balance:
  - when to keep options open and explore multiple lines of thought,
  - when to narrow attention and focus on a specific strategy,
  - when a multi-step process is necessary to reach a reliable outcome.
- The Meta-Architect should be free to choose its own internal methods, as long as they respect the goals and environment described by the Advisor.

This philosophy exists to preserve flexibility, avoid over-constraining agents, and allow them to fully exploit Kimi K2’s capabilities.

---

## 6. Current Goals & Tasks

Short- to medium-term goals include:

1. **Maintain this snapshot as the canonical system overview**
   - Use it as the base description for any agent that needs to understand the system.
   - Update it when major changes occur.

2. **Design inputs for a deep prompt creator**
   - The Advisor will use this snapshot to brief a deep prompt creator about:
     - the environment,
     - the roles,
     - the artifacts,
     - the learning objectives,
     - and the goals.
   - The deep prompt creator will then design open, non-prescriptive prompts for tasks like:
     - auditing the pseudo-analyst + K2 log,
     - learning from past mistakes,
     - designing better pseudo-Advisor roles.

3. **Audit the pseudo-analyst + K2 log using current knowledge**
   - A Meta-Architect-like agent will eventually be asked to:
     - examine the log,
     - identify success patterns and failure modes,
     - recommend improvements to processes and prompts.

4. **Evolve the Master Blueprint**
   - Gradually turn the master blueprint into a comprehensive, up-to-date design document.
   - Ensure it captures:
     - agent-specific prompts,
     - rules and policies,
     - knowledge attachments.
   - Enable scripted generation of per-agent JSON configs from this blueprint.


---

## 7. How Agents Should Use This Snapshot

- **Advisor instances**
  - Read this snapshot to understand the system.
  - Use it to design task-specific briefs for other agents.
  - Interpret and restructure its content based on the user’s immediate goals.

- **Meta-Architect instances**
  - Do not receive this snapshot directly.
  - Receive Advisor-designed briefs derived from this snapshot and from other artifacts.
  - Use those briefs, along with knowledge packs like `learning.json`, to design and audit processes and prompts.

- **Meta-prompt-creator or deep prompt-creator agents**
  - Receive Advisor-designed inputs based on this snapshot.
  - Use that information to design prompts that are:
    - goal-focused,
    - context-aware,
    - method-open (what to do, not how to do it).

- **Analyst/Auditor agents**
  - May receive this snapshot (via Advisor) to understand what they are analyzing and why.

This document exists to provide a **shared, up-to-date picture** of the system without constraining how high-capability agents must think.

---

## 8. Advisor Guidance & Document Evolution

This document is an **evolving artifact**. It may be fully up to date, partially outdated, or missing recent changes.

Expectations for any Advisor who reads this snapshot:
- Treat it as a **versioned snapshot**, not guaranteed to be final.
- Assume there may be new information, clarifications, or corrections that are not yet reflected here.
- Before making any edits to this document or treating it as canonical, the Advisor should:
  - check with the user whether there is newer information to incorporate,
  - confirm whether an update is appropriate at this time.
- If the Advisor believes they have new, relevant information or insights, they must:
  - discuss these with the user first,
  - only propose edits collaboratively,
  - avoid unilateral changes.

Key rules:
- **No edits** to this document should occur without the user’s knowledge and explicit agreement.
- Assumptions should be minimized; when in doubt, the Advisor asks rather than infers.
- The conversation around this document is **collaborative by design**, to keep top-level alignment between the user and any Advisor instance.

This section exists to ensure that the system’s conceptual core is updated deliberately, transparently, and always with the user in the loop.

