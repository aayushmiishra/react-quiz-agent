# ReAct Quiz Agent (using local LLM with Ollama)

A Socratic-style AI agent that quizzes users on **Agentic AI concepts** using the **ReAct (Reason + Act)** pattern — built from scratch using Python and qwen2.5:7b model locally run.

---

## Overview

This project implements an **interactive AI tutor agent** that:

* Asks questions about Agentic AI concepts
* Evaluates user answers
* Decides next steps using tools
* Uses the **ReAct loop (Thought → Action → Observation)**
* Runs completely **locally using Ollama (no API cost)**

---

## How it works

The agent follows a structured reasoning loop:

```text
Thought → Action → Observation → (repeat) → Final Answer
```

### Flow:

1. User answers a question
2. Agent reasons about the answer (**Thought**)
3. Agent calls a tool (**Action**)
4. Tool returns result (**Observation**)
5. Agent decides next step

---

## Tools Implemented

| Tool                      | Description                         |
| ------------------------- | ----------------------------------- |
| `get_question(concept)`   | Generates next question             |
| `evaluate_answer(answer)` | Scores answer (0–1) + feedback      |
| `get_probe(question)`     | Asks follow-up if answer is shallow |
| `advance()`               | Moves to next concept               |

---

## Concepts Covered

1. Agent vs Chain
2. ReAct Pattern
3. Tool Calling
4. Failure modes (loops, hallucination, context limits)

---

## Tech Stack

* Python
* Ollama (local LLM runtime)
* Model: `qwen2.5:7b`
* Regex-based tool parsing

---

## How to Run

### 1. Install Ollama

Download and install Ollama from:
👉 https://ollama.com

### 2. Pull model

```bash
ollama pull qwen2.5:7b
```

### 3. Install Python dependency

```bash
pip install ollama
```

### 4. Run the agent

```bash
python main.py
```

---

## Usage

```text
You: What is an agent?
Agent:
Thought: ...
Action: get_question: agent_vs_chain
Observation: ...
```

The agent will:

* Ask questions
* Evaluate your answers
* Guide you Socratically

Type `exit` to stop.

---

## Features

* ReAct-based reasoning loop
* Interactive human-in-the-loop design
* Local LLM (no API cost)
* Tool-based modular architecture
* Iteration safety (max steps)
* Hallucination detection

---

## Limitations

* Uses regex for tool parsing (can be fragile)
* Tools are LLM-based (not deterministic)
* No persistent memory across sessions

---
