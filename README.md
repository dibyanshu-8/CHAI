# Cognitive Hazard AI (CHAI)

## Project Overview
Cognitive Hazard AI (CHAI) is a supply chain risk intelligence system designed for large-scale retail operations.
It tracks, analyzes, and predicts disruptions by synthesizing unstructured global data into actionable insights.


---

## Problem Statement
Supply chains are extremely time‑sensitive.
- A 48‑hour delay in key global hubs (e.g., Shanghai, Singapore, Mumbai) can cause:
- Inventory disruption
- Margin erosion
Traditional systems are reactive, updating only after delays occur.


 CHAI solves this by enabling **proactive risk intelligence**.

---

##  Phase 1: CHAI 1.0 (RAG-Based System) 

### Concept
A Retrieval-Augmented Generation (RAG) dashboard where users:
- Query suppliers manually
- System retrieves relevant global events
- LLM summarizes risks

### Limitations
-  Passive system (requires manual queries)
-  Single-pass reasoning (misses causal chains)
-  Poor scalability for thousands of suppliers

---

## Phase 2: CHAI 2.0 (Agentic AI System)

### Key Shift
From **passive querying → autonomous monitoring system**

CHAI 2.0 operates as a **multi-agent system** running continuously.

---

##  Architecture Overview

### Multi-Agent Design
- **Researcher Agent**
  - Filters geographically relevant news signals
- **Analyst Agent**
  - Performs causal reasoning (powered by LLM)
- **Alerter Agent**
  - Generates actionable risk reports

---

### ⚙️ Core Capabilities
-  Continuous monitoring (24/7)
-  Multi-step reasoning workflow
-  Second-order impact analysis
-  Autonomous execution (no manual trigger)

---

##  Technical Stack

| Component            | Technology Used                          |
|---------------------|------------------------------------------|
| Orchestration       | LangGraph                                |
| LLM Inference       | Groq Cloud (Llama 3.3 70B)               |
| Vector Search       | FAISS                                    |
| Embeddings          | Sentence-Transformers                    |
| Framework           | LangChain (Groq integration)             |
| Backend             | Python (Modular Architecture)            |
| Data Processing     | Pandas, PyTorch                          |

---

##  System Workflow (DAG Pipeline)

1. **State Initialization**
   - Load supplier context and memory

2. **Researcher Node**
   - Semantic filtering of global intelligence feeds

3. **Analyst Node**
   - JSON-structured reasoning
   - Determines impact & severity

4. **Alerter Node**
   - Generates standardized risk reports
   - Provides recommendations

---

##  Business Impact

-  **Proactive Detection**
  - Identifies risks **3–4 days early**

-  **Scalability**
  - Handles global supplier monitoring automatically

-  **Decision Intelligence**
  - Severity-based alerts: High / Medium / Low

---

