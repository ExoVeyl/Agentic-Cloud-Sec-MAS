# Agentic Cloud Security Multi-Agent System (MAS)
**Project Title**: Agentic AI for Autonomous Threat Detection and Mitigation in Virtual Cloud Networks

## 🛡️ Project Overview
This project implements a fully autonomous Multi-Agent Cybersecurity platform designed for resource-constrained environments like SMEs in Pakistan. It utilizes specialized agents to detect attacks, reason through a "Chain of Thought" (CoT), and execute remediation strategies in real-time.

## 🧠 The 6-Pillar Schema
To mitigate AI hallucinations and ensure grounded reasoning, all knowledge is normalized into a unified 6-pillar format:
1. **Source (SRC)**: Origin of the data (NVD, MITRE, etc.).
2. **Identifier (ID)**: Unique vulnerability or technique ID (CVE-2021-44228).
3. **Information (INFO)**: Technical description of the threat.
4. **Action (ACTION)**: Pre-verified remediation steps or "Synthetic Fixes."
5. **Metric (CVSS/TACTIC)**: Severity scores or attack classifications.
6. **Provenance (LINK)**: Verified links to official documentation.

## 🛠️ Tech Stack & Requirements
- **Language**: Python 3.10+
- **AI Models**: Llama 3.2 (3B-Instruct) via **Ollama**
- **Vector Database**: **ChromaDB** & **FAISS**
- **Embeddings**: `all-MiniLM-L6-v2` (384-dimensional math vectors)
- **Frameworks**: LangGraph, Regular Expressions (Regex)

## 📂 Repository Structure
- **/P1-Data-Cleaning**: `Debug.py` - Pre-flight structural integrity checks.
- **/P2-Implementation**: `All.py` (Normalization), `Check.py` (Fidelity Audit), `Vector Creation.py`.
- **/P3-Core-System**: `UI.py` (AI Reasoning Interface), `Final Audit.py`.

## 🚀 Installation & Setup
1. **Install Dependencies**:
   ```bash
   pip install chromadb ollama sentence-transformers faiss-cpu tqdm
