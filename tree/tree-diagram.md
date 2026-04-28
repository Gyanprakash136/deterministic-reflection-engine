# Reflection Tree Diagram

```mermaid
graph TD
    START[Start] --> A1_OPEN[Axis 1: Weather]
    A1_OPEN --> A1_D1{Decision}
    
    A1_D1 -- Productive/Mixed --> A1_Q_AGENCY_HIGH[Agency High]
    A1_D1 -- Stormy/Foggy --> A1_Q_AGENCY_LOW[Agency Low]
    
    A1_Q_AGENCY_HIGH --> A1_Q_AGENCY_HIGH_FOLLOWUP[Follow-up High]
    A1_Q_AGENCY_LOW --> A1_Q_AGENCY_LOW_FOLLOWUP[Follow-up Low]
    
    A1_Q_AGENCY_HIGH_FOLLOWUP --> A1_R1[Reflection Axis 1]
    A1_Q_AGENCY_LOW_FOLLOWUP --> A1_R1
    
    A1_R1 --> BRIDGE_1_2[Bridge 1 to 2]
    BRIDGE_1_2 --> A2_OPEN[Axis 2: Energy Currency]
    
    A2_OPEN --> A2_Q2[Moment of Entitlement?]
    A2_Q2 --> A2_Q3[Team Success View]
    
    A2_Q3 --> A2_D1{Decision}
    A2_D1 -- Contribution > Entitlement --> A2_R_CONTRIB[Reflection: Contribution]
    A2_D1 -- Entitlement >= Contribution --> A2_R_ENTITLE[Reflection: Entitlement]
    
    A2_R_CONTRIB --> BRIDGE_2_3[Bridge 2 to 3]
    A2_R_ENTITLE --> BRIDGE_2_3
    
    BRIDGE_2_3 --> A3_OPEN[Axis 3: Frame of Thoughts]
    A3_OPEN --> A3_Q2[Change Experience?]
    A3_Q2 --> A3_Q3[Ripple Effect]
    
    A3_Q3 --> A3_D1{Decision}
    A3_D1 -- Altro > Self --> A3_R_ALTRO[Reflection: Altrocentrism]
    A3_D1 -- Self >= Altro --> A3_R_SELF[Reflection: Self-Centrism]
    
    A3_R_ALTRO --> SUMMARY_D{Summary Decision}
    A3_R_SELF --> SUMMARY_D
    
    SUMMARY_D --> SUMMARY[Summary Node]
    SUMMARY --> END[End]
```

---

## 2. Deterministic Engine Workflow
This diagram illustrates how the system processes each node without any stochastic (AI) elements.

```mermaid
graph LR
    A[Current Node] --> B{Node Type?}
    
    B -- "Start/Bridge" --> C[Auto-Advance after Delay]
    B -- "Question" --> D[Wait for User Selection]
    B -- "Decision" --> E[Evaluate Condition Logic]
    B -- "Reflection" --> F[Wait for 'Continue' Click]
    
    D --> G[Update Signal Tallies]
    G --> H[Update Answer State]
    H --> I[Jump to next ID]
    
    E --> J{Logic Evaluation}
    J -- Match --> K[Jump to Target ID]
    J -- No Match --> L[Error State]
    
    C --> I
    F --> I
    K --> I
```

## 3. Data Flow Architecture
How the tree data and user state interact during a session.

```mermaid
sequenceDiagram
    participant User
    participant App as Streamlit App
    participant Tree as reflection-tree.json
    participant State as Session State

    App->>Tree: Load Nodes
    User->>App: Interaction
    App->>State: Store Answer {NodeID.value}
    App->>State: Update Signals {Axis:Pole}
    App->>Tree: Lookup next NodeID
    Tree->>App: Node Content
    App->>App: Interpolate {Placeholders}
    App->>User: Render Node
```
