# The Daily Reflection Tree
**A Deterministic Engine for Guided Self-Observation and Behavioral Growth**

This repository contains the architecture and implementation for a deterministic reflection tool, designed to map organizational psychology onto a navigable decision tree.

## Project Structure
- `/tree/`: Contains the structured data and design documents.
  - `reflection-tree.json`: The core deterministic tree (25+ nodes).
  - `tree-diagram.md`: Visual representation of the tree structure.
  - `write-up.md`: Psychological grounding and design rationale.
- `/agent/`: The web-based reflection agent (React).
- `/transcripts/`: Sample session walkthroughs.

## The Three Axes
1. **Axis 1: Locus (Victim ↔ Victor)**: Do you see yourself as a participant or a spectator in today's events?
2. **Axis 2: Orientation (Contribution ↔ Entitlement)**: Did you focus on what you gave or what you were owed?
3. **Axis 3: Radius (Self-Centrism ↔ Altrocentrism)**: How wide was your lens of concern today?

## How to Run the Agent
1. Navigate to the `agent` directory:
   ```bash
   cd agent
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the Streamlit server:
   ```bash
   streamlit run app.py
   ```

## Technical Architecture
The system is built as a **Deterministic Finite State Machine (FSM)**.

- **Data Layer**: A structured JSON graph ([reflection-tree.json](tree/reflection-tree.json)) defining nodes, logic conditions, and signal weights.
- **Logic Engine**: A Python-based traversal engine in Streamlit that evaluates boolean expressions against the current session state.
- **State Management**: Tracks cumulative "signals" across three axes and stores historical answers for context-aware interpolation.

## Quality Assurance & Knowledge Engineering
To ensure the integrity of the reflection paths, we've implemented an automated validation suite:

- **Tree Validator**: `tree/validate_tree.py`
  - Checks for dead ends (nodes with no next path).
  - Validates all jump targets exist.
  - Ensures all interpolation placeholders refer to valid node IDs.
  - Identifies orphaned/unreachable nodes.

Run the validator:
```bash
python3 tree/validate_tree.py
```

## Folder Structure
```text
/tree/
  reflection-tree.json    ← Core Decision Tree (Data)
  tree-diagram.md         ← Visual branching & workflow diagrams
  validate_tree.py        ← Automated QA Validation Script
/agent/
  app.py                  ← Streamlit Reflection Agent
  requirements.txt        ← Dependencies
/transcripts/
  persona-1-transcript.md <-- Victor persona walkthrough
  persona-2-transcript.md <-- Victim persona walkthrough
write-up.md               <-- Design rationale & Psychological grounding
README.md                 <-- You are here
```

## Design Philosophy
This tool is **fully deterministic**. It does not use any LLMs at runtime. Branching is handled via a logic engine that tallies "signals" from user responses and interpolates text to create a personalized reflection experience.
