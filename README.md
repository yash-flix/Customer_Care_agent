# Customer Care Agent using AWS Bedrock AgentCore

An AI-powered Customer Support Agent built with AWS Bedrock AgentCore, LangChain, Amazon Titan Embeddings, FAISS Vector Search, and Groq LLMs.

The project simulates a telecom customer support system for a fictional company called **Lauki Phones**, enabling users to ask questions about plans, billing, roaming, SIM activation, security, and account management.

---
<img width="1365" height="633" alt="WhatsApp Image 2026-06-15 at 11 45 18 AM" src="https://github.com/user-attachments/assets/89c46088-0386-4364-b2a8-620d06f026b6" />

<img width="1365" height="640" alt="WhatsApp Image 2026-06-15 at 1 36 42 PM" src="https://github.com/user-attachments/assets/a61dc8c6-ee7b-4275-a029-6a1d61167553" />

<img width="1365" height="636" alt="WhatsApp Image 2026-06-15 at 1 39 37 PM" src="https://github.com/user-attachments/assets/95d73f39-ee74-4f08-9d8d-ddec69c1bdd6" />





## Features

* AI-powered FAQ Assistant
* Semantic Search using Vector Embeddings
* Tool Calling with LangChain Agents
* AWS Bedrock AgentCore Deployment
* Amazon Titan Embeddings v2
* FAISS Vector Database
* Agent Memory Support
* CloudWatch Observability
* Production-style Streamlit Frontend

---

## Problem Statement

Customer support teams repeatedly answer the same questions every day.

Lauki Phones maintains a knowledge base of FAQ question-and-answer pairs used to train support representatives. The goal of this project is to automate that process by building an AI agent capable of retrieving relevant information and generating accurate responses in real time.

---

## Architecture

```text
User
   ↓
Streamlit UI
   ↓
AWS Bedrock AgentCore
   ↓
LangChain Agent
   ↓
Tool Calling
   ↓
FAISS Vector Store
   ↓
Amazon Titan Embeddings v2
   ↓
FAQ Knowledge Base (CSV)
```

---

## Tech Stack

### AWS

* Amazon Bedrock AgentCore
* Amazon Titan Embeddings v2
* CloudWatch Logs
* CloudWatch Observability

### AI / ML

* LangChain
* Groq GPT-OSS-20B
* FAISS Vector Search

### Frontend

* Streamlit

### Language

* Python

---

## How It Works

### Step 1: Load FAQ Data

The FAQ knowledge base is stored as a CSV file containing question-and-answer pairs.

### Step 2: Generate Embeddings

Amazon Titan Embeddings v2 converts FAQ content into vector representations.

### Step 3: Store in FAISS

The vectors are indexed inside a FAISS vector database for fast similarity search.

### Step 4: User Query

A user submits a question through the Streamlit interface.

### Step 5: Tool Calling

The LangChain agent invokes retrieval tools to search the FAQ knowledge base.

### Step 6: Response Generation

The retrieved information is sent to the LLM, which generates a final response.

---

## Challenges Faced

During development, I encountered runtime startup failures after successful deployment, dependency compatibility issues between LangChain packages, and components that worked locally but not in the AgentCore environment. Using CloudWatch observability, runtime logging, dependency updates, and architecture simplification helped identify and resolve the root causes. I also built a custom Streamlit frontend to provide a production-style user experience instead of relying solely on terminal-based interactions.

---

## Example Queries

* How long does porting take?
* What is the refund policy for damaged SIM cards?
* How do I activate roaming?
* What security measures protect my account?
* How do I switch from a physical SIM to an eSIM?

---

## Screenshots

### AWS Bedrock AgentCore Runtime

Deployed and running on AWS AgentCore.

### CloudWatch Observability

Monitoring runtime activity, latency, traces, and telemetry.

### Streamlit Frontend

Production-style customer support interface.

---

## Future Improvements

* Multi-tool customer support workflows
* Ticket creation and management
* Customer profile lookup
* Billing information retrieval
* Escalation handling
* Multi-language support
* RAG pipeline enhancements

---

## Repository

GitHub: https://github.com/yash-flix/Customer_Care_agent

---

## Author

Yash Rane

Artificial Intelligence & Data Science Engineering Student

Passionate about AI Agents, Generative AI, Cloud Computing, and Backend Development.
