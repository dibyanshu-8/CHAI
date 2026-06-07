# Cognitive Hazard AI (CHAI) 


---

## Summary
Cognitive Hazard AI (CHAI)  is an autonomous multi-agent system designed to detect, analyze, and predict global supply chain disruptions in real time.

Unlike traditional systems that rely on manual queries and historical data, CHAI  operates as a **24/7 intelligent agent**, leveraging real-time web signals and causal reasoning to generate actionable risk alerts.

---

##  Problem Statement

Modern supply chains face:
- High dependency on global manufacturing hubs
- Sensitivity to geopolitical, weather, and labor disruptions
- Lack of proactive intelligence in traditional tools

 Existing systems are:
- Reactive  
- Query-dependent  
- Limited to surface-level insights  

---

##  Evolution of the System

### Phase 1: CHAI 1.0 (Passive RAG System)

- Chatbot-style interface over vector database
- Manual query required for risk analysis

#### Limitations
-  Requires human trigger
-  Passivity bias (missed risks)
-  Linear summaries (no causal reasoning)

---

###  Phase 2: CHAI 2.0 (Agentic AI System)

Transition to a **fully autonomous agent architecture**

#### Key Improvements
-  Autonomous execution (scheduled runs)
-  Real-time intelligence via web search
-  Deep causal reasoning (second-order effects)
-  Stateful memory for context retention

---

##  System Architecture

### Multi-Agent DAG (LangGraph)

1. **Researcher Agent**
   - Uses Tavily Search API
   - Filters relevant global signals (geo + domain-specific)

2. **Analyst Agent**
   - Powered by Groq (Llama 3.3 70B)
   - Performs causal reasoning
   - Evaluates impact on:
     - Production
     - Labor
     - Logistics

3. **Alerter Agent**
   - Generates structured reports
   - Assigns severity levels:
     - High / Medium / Low
   - Suggests mitigation strategies

---

##  Core Technology Stack

| Layer                | Technology Used                     |
|---------------------|------------------------------------|
| Orchestration       | LangGraph                          |
| LLM Inference       | Groq Cloud (Llama 3.3 70B)         |
| Real-time Data      | Tavily Search API                  |
| Backend             | Python 3.12                        |
| Containerization    | Docker                             |
| Deployment Target   | AWS Lambda (Serverless)            |

---

##  Workflow Pipeline (DAG Execution)

1. **State Initialization**
   - Load supplier context + memory

2. **Research Phase**
   - Fetch real-time global signals

3. **Analysis Phase**
   - Perform structured reasoning
   - Generate severity scores

4. **Alert Generation**
   - Output standardized reports

---

##  Key LLMOps Features

###  Semantic Memory & Deduplication
- Hash-based memory system
- Prevents duplicate alerts
- Stores previous event signatures (JSON / scalable to DynamoDB)

---

### Containerization
- Fully Dockerized environment
- Ensures reproducibility across systems
- Eliminates dependency conflicts

---

### Cloud-Ready Design
- AWS Lambda-compatible handler
- Event-driven execution via Amazon EventBridge
- Scalable and cost-efficient architecture .

---





