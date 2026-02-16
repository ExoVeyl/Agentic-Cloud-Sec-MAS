# Phase 3: Core System & AI Interface

## 🎯 Objective
This module provides the "Executive Agentic Layer," allowing a security analyst to interact with the audited knowledge base. It uses RAG (Retrieval-Augmented Generation) to ensure all AI responses are grounded in the 6-pillar schema.

## 📄 Key Scripts
- `UI.py` (The Executive): 
  - Manages the RAG loop using localized Llama 3.2 (3B-Instruct).
  - Implements a hybrid search mechanism: exact Regex matching for CVE/Technique IDs and Semantic Vector search for natural language queries.
  - Enforces a "Grounded Reasoning" policy, preventing hallucinations by strictly using retrieved context.
- `Final Audit.py`:
  - Acts as the system's "Black Box" recorder.
  - Generates forensic logs of every query, retrieved context, and the resulting AI remediation plan.

## 🛡️ Security Features
- 100% Offline Inference: No data leaves the local environment, satisfying SME privacy constraints.
- Chain of Thought (CoT): The agent explicitly displays its logic path for human-in-the-loop verification.
- Distance-Based Accuracy: Queries are matched with mathematical precision scores to ensure relevance.

## 🚀 Usage
Launch the interface after the Phase 2 vector store has been initialized:
```bash
python UI.py
