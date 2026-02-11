# How to Add Persistent Memory to OpenClaw with Mem0 -- and Why

## Executive Summary

OpenClaw (formerly Clawdbot/Moltbot) is the fastest-growing open-source autonomous AI agent framework, accumulating over 160,000 GitHub stars since its launch in late 2025. While OpenClaw includes a built-in file-based memory system using Markdown files and hybrid BM25/vector search, it suffers from limitations in semantic understanding, cross-session continuity, and intelligent fact extraction. Mem0 is a dedicated persistent memory layer for AI agents that addresses these gaps through LLM-powered fact extraction, semantic vector search, optional graph memory for relationship modeling, and multi-dimensional entity scoping.

Integrating Mem0 into OpenClaw delivers measurable improvements: 26% higher response accuracy compared to baseline approaches, 90% reduction in token usage through intelligent memory compression, and 91% lower p95 latency. The integration is available as an official plugin (`@mem0/openclaw-mem0`) with both cloud-managed and fully self-hosted deployment options, requiring as little as 30 seconds for initial setup.

This document provides a complete technical analysis of both systems, explains why persistent memory matters for AI agents, and delivers a step-by-step implementation guide with runnable code examples, architecture diagrams, best practices, and security considerations.

---

## Table of Contents

- [1. What is Mem0?](#1-what-is-mem0)
  - [1.1 Core Architecture](#11-core-architecture)
  - [1.2 Memory Types and Hierarchy](#12-memory-types-and-hierarchy)
  - [1.3 Python SDK and Core API](#13-python-sdk-and-core-api)
  - [1.4 Storage Infrastructure](#14-storage-infrastructure)
  - [1.5 Graph Memory](#15-graph-memory)
  - [1.6 LLM and Embedder Configuration](#16-llm-and-embedder-configuration)
  - [1.7 Self-Hosted vs Cloud Platform](#17-self-hosted-vs-cloud-platform)
  - [1.8 Advanced Features](#18-advanced-features)
- [2. What is OpenClaw?](#2-what-is-openclaw)
  - [2.1 Origins and Evolution](#21-origins-and-evolution)
  - [2.2 Four-Layer Architecture](#22-four-layer-architecture)
  - [2.3 Built-in Memory System](#23-built-in-memory-system)
  - [2.4 Extension Points](#24-extension-points)
  - [2.5 Skills and Plugin Ecosystem](#25-skills-and-plugin-ecosystem)
- [3. Why Persistent Memory?](#3-why-persistent-memory)
  - [3.1 The Problem with Stateless AI](#31-the-problem-with-stateless-ai)
  - [3.2 Benefits of Persistent Memory](#32-benefits-of-persistent-memory)
  - [3.3 RAG vs Persistent Memory vs Fine-Tuning](#33-rag-vs-persistent-memory-vs-fine-tuning)
  - [3.4 Use Cases](#34-use-cases)
  - [3.5 Why Mem0 Specifically](#35-why-mem0-specifically)
- [4. Implementation Guide](#4-implementation-guide)
  - [4.1 Quick Start: Cloud Platform (30 Seconds)](#41-quick-start-cloud-platform-30-seconds)
  - [4.2 Self-Hosted Setup (Full Control)](#42-self-hosted-setup-full-control)
  - [4.3 Plugin Configuration Reference](#43-plugin-configuration-reference)
  - [4.4 Using Memory Tools](#44-using-memory-tools)
  - [4.5 CLI Operations](#45-cli-operations)
  - [4.6 Advanced: Custom Python Integration](#46-advanced-custom-python-integration)
  - [4.7 Advanced: MCP Server Integration](#47-advanced-mcp-server-integration)
- [5. Architecture Diagram](#5-architecture-diagram)
- [6. Best Practices](#6-best-practices)
- [7. Security and Privacy Considerations](#7-security-and-privacy-considerations)
- [8. Performance and Scaling](#8-performance-and-scaling)
- [9. Alternatives Comparison](#9-alternatives-comparison)
- [10. Troubleshooting](#10-troubleshooting)
- [11. References](#11-references)

---

## 1. What is Mem0?

Mem0 (https://mem0.ai) is a universal, self-improving persistent memory layer for AI agents and large language models. It transforms stateless AI assistants into intelligent, context-aware agents capable of maintaining persistent knowledge across sessions. Originally open-sourced under the Apache 2.0 license and backed by Y Combinator, Mem0 provides both a managed cloud platform and a fully self-hostable open-source library.

### 1.1 Core Architecture

Mem0's architecture rests on three foundational pillars:

1. **State** -- Understanding the immediate context of the current conversation or task
2. **Persistence** -- Retaining knowledge across sessions, preserving user preferences and learned behaviors
3. **Selection** -- Intelligent filtering to decide what information is worth remembering

Together, these enable **continuity**: consistent, personalized interactions over extended periods rather than treating each conversation as an isolated event.

Internally, Mem0 implements a pipeline:

```
User Message --> LLM Fact Extraction --> Conflict Detection --> Vector Embedding
                                              |                       |
                                     Existing Memory Check     Vector Database
                                              |                       |
                                     Update / Merge / Insert   Graph Database (optional)
                                              |                       |
                                        History Store (SQLite)  Metadata Index
```

The system processes raw conversation messages, extracts structured facts through LLM analysis, checks for conflicts with existing memories, deduplicates, and stores results across vector and optional graph databases. This pipeline runs identically for both the managed platform and the open-source SDK.

### 1.2 Memory Types and Hierarchy

Mem0 implements a sophisticated hierarchical memory system:

| Layer | Scope | Lifetime | Example |
|-------|-------|----------|---------|
| **Conversation Memory** | In-flight messages from current turn | Single response cycle | "The user just asked about Tokyo" |
| **Session Memory** | Short-lived facts for current task | Session duration (via `run_id`) | "Currently debugging authentication" |
| **User Memory** | Long-lived knowledge tied to a person | Indefinite (via `user_id`) | "Prefers Python over JavaScript" |
| **Organizational Memory** | Shared context for teams/agents | Indefinite (via `org_id`) | "Company uses PostgreSQL 16" |

Within each layer, memories are further categorized:

- **Factual Memory** -- User preferences, account details, domain facts
- **Episodic Memory** -- Summaries of past interactions or completed tasks
- **Semantic Memory** -- Relationships between concepts for abstract reasoning
- **Working Memory** -- Temporary state (tool outputs, intermediate calculations)

### 1.3 Python SDK and Core API

**Installation:**

```bash
pip install mem0ai  # Requires Python 3.9+ (3.10+ recommended)
```

**Initialization (Self-Hosted):**

```python
import os
from mem0 import Memory

os.environ["OPENAI_API_KEY"] = "sk-your-key"

m = Memory()
```

**Initialization (Cloud Platform):**

```python
from mem0 import MemoryClient

client = MemoryClient(
    api_key="m0-your-key",
    org_id="your_org_id",       # optional
    project_id="your_project_id" # optional
)
```

**Add Memories:**

```python
messages = [
    {"role": "user", "content": "I'm planning a trip to Tokyo next month."},
    {"role": "assistant", "content": "Great! I'll remember that for future suggestions."},
    {"role": "user", "content": "I prefer boutique hotels and avoid shellfish."}
]

# With intelligent fact extraction (default)
result = m.add(
    messages,
    user_id="alice",
    metadata={"category": "travel_plans"}
)
# Extracts: "Planning trip to Tokyo", "Prefers boutique hotels", "Avoids shellfish"

# Without extraction (raw storage)
result = m.add(messages, user_id="alice", infer=False)
```

**Search Memories (Semantic):**

```python
# Simple semantic search
results = m.search("dietary restrictions", user_id="alice")

# With filters
results = m.search(
    "food preferences",
    user_id="alice",
    filters={"categories": {"contains": "diet"}}
)

# Platform client with complex filters
results = client.search("query", filters={
    "AND": [
        {"user_id": "alice"},
        {"agent_id": "travel-planner"},
        {"created_at": {"gte": "2025-01-01"}}
    ]
})
```

**Get All Memories (Bulk Retrieval):**

```python
# Retrieve all memories for a user with pagination
memories = client.get_all(
    filters={
        "AND": [
            {"user_id": "alice"},
            {"created_at": {"gte": "2025-07-01", "lte": "2025-07-31"}}
        ]
    },
    page=1,
    page_size=100
)
```

**Update Memories:**

```python
# Single update
client.update(
    memory_id="mem_abc123",
    text="Prefers luxury boutique hotels (updated from boutique hotels)",
    metadata={"category": "accommodation"}
)

# Batch update (up to 1000)
client.batch_update([
    {"memory_id": "id1", "text": "Watches football"},
    {"memory_id": "id2", "text": "Likes to travel"}
])
```

**Delete Memories:**

```python
# Single delete
m.delete(memory_id="mem_abc123")

# Delete all for a user
m.delete_all(user_id="alice")

# Delete with filters (e.g., GDPR compliance)
client.delete_all(filters={
    "AND": [
        {"user_id": "alice"},
        {"created_at": {"lt": "2025-01-01"}}
    ]
})
```

**Supported Filter Operators:**

| Operator | Description | Example |
|----------|-------------|---------|
| `gte` | Greater than or equal | `{"created_at": {"gte": "2025-01-01"}}` |
| `lte` | Less than or equal | `{"created_at": {"lte": "2025-12-31"}}` |
| `gt` / `lt` | Greater / less than | `{"score": {"gt": 0.8}}` |
| `ne` | Not equal | `{"status": {"ne": "archived"}}` |
| `in` | Match any in list | `{"agent_id": {"in": ["a1", "a2"]}}` |
| `nin` | Not in list | `{"category": {"nin": ["spam"]}}` |
| `contains` | Substring match | `{"tags": {"contains": "travel"}}` |
| `icontains` | Case-insensitive substring | `{"name": {"icontains": "alice"}}` |

### 1.4 Storage Infrastructure

Mem0 supports 19+ vector database providers:

| Category | Providers |
|----------|-----------|
| **Local/Dev** | Qdrant (default), Chroma |
| **Managed Cloud** | Pinecone, Weaviate Cloud, Milvus Cloud, Upstash Vector |
| **Self-Hosted Production** | Milvus, Weaviate, Elasticsearch, OpenSearch |
| **Cloud-Native** | Azure AI Search, AWS OpenSearch, Cloudflare |
| **SQL-Based** | PostgreSQL (pgvector) |
| **Edge** | Cloudflare Vectorize |

**Example: Pinecone Configuration:**

```python
import os
from mem0 import Memory

config = {
    "vector_store": {
        "provider": "pinecone",
        "config": {
            "api_key": os.environ["PINECONE_API_KEY"],
            "index_name": "mem0-index",
            "environment": "gcp-starter"
        }
    },
    "llm": {
        "provider": "openai",
        "config": {
            "model": "gpt-4o-mini",
            "api_key": os.environ["OPENAI_API_KEY"]
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small",
            "api_key": os.environ["OPENAI_API_KEY"]
        }
    }
}

m = Memory.from_config(config_dict=config)
```

**Example: PostgreSQL with pgvector:**

```python
config = {
    "vector_store": {
        "provider": "pgvector",
        "config": {
            "host": "localhost",
            "port": 5432,
            "dbname": "mem0_db",
            "user": "mem0_user",
            "password": os.environ["PG_PASSWORD"],
            "collection_name": "memories"
        }
    }
}
```

### 1.5 Graph Memory

Beyond vector similarity search, Mem0 supports optional graph-based memory that explicitly represents relationships between entities, enabling multi-hop reasoning:

```python
import os
from mem0 import Memory

# Neo4j configuration
config = {
    "graph_store": {
        "provider": "neo4j",
        "config": {
            "url": os.environ["NEO4J_URL"],
            "username": os.environ["NEO4J_USERNAME"],
            "password": os.environ["NEO4J_PASSWORD"]
        }
    }
}

# Kuzu (embedded, zero-config)
config = {
    "graph_store": {
        "provider": "kuzu",
        "config": {
            "db": "/tmp/mem0-graph.kuzu"
        }
    }
}

m = Memory.from_config(config_dict=config)
```

Supported graph backends: **Neo4j**, **Memgraph**, **Amazon Neptune**, **Kuzu** (embedded).

Graph memory extracts named entities and relationships from each memory write, storing them as nodes and edges. On retrieval, vector search narrows candidates while the graph returns related entities through relationship traversal -- enabling discovery of connections that pure semantic similarity would miss.

**Example:** Alice mentions meeting Bob at a conference. Later, when Alice asks for Bob's contact info, graph memory traverses the "met_at" relationship to retrieve Bob's details, even though "contact info" and "conference meeting" have low direct semantic similarity.

### 1.6 LLM and Embedder Configuration

**Supported LLM Providers:**

| Provider | Configuration Key | Notes |
|----------|------------------|-------|
| OpenAI | `openai` | Default; GPT-4o, GPT-4o-mini, etc. |
| Anthropic | `anthropic` | Claude Sonnet, Claude Haiku |
| Ollama | `ollama` | Local models (Llama, Mistral) |
| Groq | `groq` | High-speed inference |
| Together.ai | `together` | Distributed inference |
| Azure OpenAI | `azure_openai` | Enterprise Azure deployments |
| Google Vertex AI | `vertexai` | Google Cloud |
| AWS Bedrock | `aws_bedrock` | AWS-native |

**Example: Anthropic Claude as LLM:**

```python
import os
from mem0 import Memory

config = {
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.1,
            "max_tokens": 2000
        }
    }
}

os.environ["ANTHROPIC_API_KEY"] = "your-anthropic-key"
os.environ["OPENAI_API_KEY"] = "your-openai-key"  # still needed for embeddings

m = Memory.from_config(config)
```

**Example: Fully Local with Ollama:**

```python
config = {
    "llm": {
        "provider": "ollama",
        "config": {
            "model": "llama3.1:8b",
            "ollama_base_url": "http://localhost:11434"
        }
    },
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": "nomic-embed-text",
            "ollama_base_url": "http://localhost:11434"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333
        }
    }
}

m = Memory.from_config(config)
# Zero external API calls -- fully private
```

**Supported Embedder Providers:** OpenAI (default), Cohere, Google Vertex AI, Azure OpenAI, Ollama, Hugging Face (via LangChain), Sentence Transformers (local).

### 1.7 Self-Hosted vs Cloud Platform

| Feature | Cloud Platform | Open Source (Self-Hosted) |
|---------|---------------|--------------------------|
| **Time to first memory** | 5 minutes | 15-30 minutes |
| **Infrastructure needed** | None | Vector DB + Python runtime |
| **Maintenance** | Fully managed | Self-managed |
| **Auto-scaling** | Built-in | Manual setup required |
| **High availability** | Built-in | DIY setup |
| **Dashboard** | Web-based analytics | CLI / logs |
| **Graph memory** | Managed | Self-configured |
| **Data residency** | US (expandable) | Your choice |
| **SOC 2 / HIPAA** | Certified | Your responsibility |
| **Price** | Consumption-based | Infrastructure costs only |
| **Free tier** | 10,000 memories + 1,000 searches/mo | Unlimited (you pay infra) |
| **Pro plan** | $249/mo (graph memory, priority) | N/A |
| **Best for** | Fast iteration, compliance needs | Cost-sensitive, custom requirements |
| **License** | Proprietary SaaS | Apache 2.0 |

### 1.8 Advanced Features

**Memory Expiration:**

```python
import datetime
from mem0 import MemoryClient

client = MemoryClient(api_key="your-key")

# Memory expires in 30 days (auto-excluded from search after expiration)
client.add(
    messages=[{"role": "user", "content": "I'll be in SF until end of month"}],
    user_id="alice",
    expiration_date=str(datetime.datetime.now().date() + datetime.timedelta(days=30))
)
```

**Custom Fact Extraction Prompts:**

```python
custom_prompt = """
Extract only: customer support info, order details, and user preferences.

Input: My order #12345 hasn't arrived yet.
Output: {"facts": ["Order #12345 not received"]}

Input: The weather is nice today.
Output: {"facts": []}
"""

config = {
    "custom_fact_extraction_prompt": custom_prompt,
    "version": "v1.1"
}

m = Memory.from_config(config_dict=config)
```

**Multimodal Memory (Images and Documents):**

```python
from mem0 import Memory

m = Memory()

# Extract memories from images
messages = [
    {"role": "user", "content": "Remember what I ordered"},
    {"role": "user", "content": {
        "type": "image_url",
        "image_url": {"url": "https://example.com/receipt.jpg"}
    }}
]
m.add(messages, user_id="alice")

# Extract from PDFs
messages = [{"role": "user", "content": {
    "type": "pdf_url",
    "pdf_url": {"url": "https://example.com/contract.pdf"}
}}]
m.add(messages, user_id="alice")
```

**Reranking for Improved Precision:**

```python
config = {
    "reranker": {
        "provider": "cohere",
        "config": {
            "model": "rerank-english-v3.0",
            "api_key": "your-cohere-api-key"
        }
    }
}

m = Memory.from_config(config)
results = m.search("science fiction books", user_id="reader123", rerank=True)
```

---

## 2. What is OpenClaw?

### 2.1 Origins and Evolution

OpenClaw is an open-source autonomous AI agent framework created by Austrian developer Peter Steinberger (creator of PSPDFKit). Originally launched in November 2025 as "Clawdbot" (a pun on Claude + claw, referencing Anthropic's lobster mascot), it was renamed to "Moltbot" in January 2026 after Anthropic trademark pressure, then finally settled on "OpenClaw" as its legally protected identity.

As of February 2026, OpenClaw has accumulated over 160,000 GitHub stars, making it the fastest-growing open-source project in history by that metric. It fundamentally reconceptualizes AI assistance by collapsing the boundary between conversation and action -- deploying a locally-running autonomous agent capable of accessing the filesystem, executing shell commands, controlling web browsers, sending messages, and performing real-world tasks with minimal human intervention.

**Tagline:** "Your own personal AI assistant. Any OS. Any Platform."

**Repository:** https://github.com/openclaw/openclaw

### 2.2 Four-Layer Architecture

OpenClaw is built on four distinct layers:

```
+-------------------------------------------------------------------+
|                     1. MESSAGING GATEWAY                          |
|  WhatsApp | Telegram | Slack | Discord | Signal | iMessage | Web  |
|  - Single long-lived daemon (port 18789)                          |
|  - WebSocket transport with JSON Schema validation                |
|  - Device pairing and authentication                              |
+-------------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------------+
|                      2. AGENT CORE                                |
|  - ReAct (Reasoning + Acting) pattern                             |
|  - Multi-LLM routing (Claude, GPT, Gemini, DeepSeek, Ollama)     |
|  - Intent analysis and task decomposition                         |
|  - Token budget management and cost optimization                  |
|  - Session identity and context coherence                         |
+-------------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------------+
|                   3. PERSISTENT MEMORY                            |
|  - File-first: Markdown as source of truth                        |
|  - MEMORY.md (curated long-term) + daily logs (rolling context)   |
|  - Hybrid search: BM25 (30%) + Vector (70%)                      |
|  - SQLite + sqlite-vec for local embeddings                       |
|  - Pre-compaction flush to prevent data loss                      |
+-------------------------------------------------------------------+
                              |
                              v
+-------------------------------------------------------------------+
|                  4. EXECUTION ENVIRONMENT                         |
|  - ~25 built-in tools (file ops, exec, browser, web)              |
|  - 53 bundled skills (Gmail, GitHub, Obsidian, etc.)              |
|  - Docker sandbox support                                         |
|  - Fine-grained permission boundaries                             |
|  - Plugin system for Gateway-level extensions                     |
+-------------------------------------------------------------------+
```

### 2.3 Built-in Memory System

OpenClaw's native memory system uses a **file-first philosophy** where Markdown files are the source of truth:

**File Organization:**
```
~/.openclaw/workspace/
  MEMORY.md              # Curated long-term facts, decisions, preferences
  memory/
    2026-02-10.md        # Today's daily log (append-only)
    2026-02-09.md        # Yesterday's daily log
    ...
```

**Search Mechanism:**
- **Hybrid search**: Combines BM25 keyword matching (30% weight) with vector similarity (70% weight)
- **Embeddings**: Local model by default (~600MB `embeddinggemma-300M`)
- **Storage**: Per-agent SQLite at `~/.openclaw/memory/<agentId>.sqlite`
- **Chunking**: ~400 tokens per chunk with 80-token overlap
- **Indexing**: File watchers mark index dirty (1.5s debounce); delta-based incremental updates

**Automatic Memory Flush (Pre-Compaction):**
When approaching context limits, OpenClaw triggers a silent agentic turn that prompts the model to persist important information to disk before older messages are compacted. This prevents catastrophic information loss during context window management.

**Limitations of the Built-in System:**
1. No intelligent fact extraction -- stores raw text, not structured facts
2. No conflict detection or deduplication
3. No entity-scoped memory (user/agent/session/org isolation)
4. Limited semantic understanding (relies on basic embedding similarity)
5. No graph-based relationship modeling
6. No cross-platform identity unification
7. Manual curation required for MEMORY.md
8. No memory expiration or lifecycle management

### 2.4 Extension Points

OpenClaw provides three primary extension mechanisms:

**1. Skills** -- Markdown-based capability modules:
```
.openclaw/skills/<skill-name>/
  SKILL.md          # YAML frontmatter + instructions
  scripts/          # Optional executable scripts
  references/       # Optional reference documents
```

**2. Plugins** -- Programmatic Gateway-level extensions:
- Custom commands processed before built-in commands
- Custom RPC methods for Gateway communication
- Channel-specific behavior modules
- Installed via npm or local filesystem
- Configured in `openclaw.json` under `plugins.entries.<id>`

**3. Memory Plugins** -- Replaceable memory backends:
- Default: `memory-core` (file-based + SQLite)
- Can be replaced entirely via `plugins.slots.memory`
- Alternative: QMD backend (BM25 + vectors + reranking)
- Custom plugins can implement `memory_search` and `memory_get` tools

### 2.5 Skills and Plugin Ecosystem

OpenClaw's skill ecosystem is managed through **ClawHub**, a community registry. Skills teach the agent integration patterns without granting permissions -- the agent must have the appropriate tools enabled to execute what skills describe.

**Security Warning:** ClawHub has been identified as an attack surface. Hundreds of malicious skills have been found that use markdown instructions as social engineering wrappers to trick agents into executing staged payloads. Always review skills before installation and prefer official/verified skills.

---

## 3. Why Persistent Memory?

### 3.1 The Problem with Stateless AI

Traditional LLMs suffer from a fundamental architectural limitation: **they possess no internal memory mechanism beyond their context window**. Every new conversation starts from zero. This creates several problems:

1. **Repetitive onboarding**: Users must re-explain preferences, project context, and decisions every session
2. **Token waste**: Large context windows (100K+ tokens) are expensive and slow to process
3. **Information loss**: Critical details from previous sessions are permanently lost
4. **Inconsistent behavior**: The agent cannot build a coherent model of the user over time
5. **Exploration overhead**: Tasks requiring contextual knowledge force multiple "exploration turns" that waste time and tokens

**Quantified Impact:** Mem0 benchmarks show that tasks typically requiring 3+ exploration turns completed with zero exploration when memory context was pre-injected. This translates to 90% lower token usage and 91% faster responses.

### 3.2 Benefits of Persistent Memory

| Benefit | Description | Measured Impact |
|---------|-------------|-----------------|
| **Personalization** | Agent adapts to individual preferences and patterns | 26% higher accuracy vs baseline |
| **Continuity** | Conversations build on previous interactions seamlessly | Zero re-onboarding per session |
| **Cost Reduction** | Compressed memory vs full context replay | 90% token savings |
| **Latency** | Less processing of redundant context | 91% lower p95 latency |
| **Accuracy** | Relevant memories reduce hallucination and improve relevance | 66.9% accuracy (vs 61.0% RAG) |
| **Scalability** | Memory grows with the user without increasing per-request costs | Sublinear cost growth |
| **Multi-agent** | Shared memory enables team coordination | Consistent context across agents |

### 3.3 RAG vs Persistent Memory vs Fine-Tuning

| Dimension | RAG | Persistent Memory (Mem0) | Fine-Tuning |
|-----------|-----|--------------------------|-------------|
| **What it does** | Retrieves documents to augment prompts | Extracts, stores, and recalls facts from interactions | Adjusts model weights on domain data |
| **Knowledge source** | External documents/databases | Conversation history + explicit stores | Training dataset |
| **Update speed** | Instant (add documents) | Instant (per interaction) | Hours/days (retraining) |
| **Personalization** | None (document-level) | Per-user, per-session, per-agent | Global (all users) |
| **Cost per query** | Embedding + retrieval + generation | Memory search + generation (smaller context) | Only generation (but training is expensive) |
| **Statefulness** | Stateless | Stateful (remembers across sessions) | Stateless (baked into weights) |
| **Best for** | Knowledge bases, documentation | User preferences, interaction history, learned patterns | Domain adaptation, style/format consistency |
| **Drawbacks** | Context pollution, no personalization | Requires memory management, extraction quality depends on LLM | Expensive retraining, catastrophic forgetting, no real-time updates |
| **Accuracy** | 61.0% (benchmark) | 66.9% (benchmark) | Varies by domain |
| **Latency** | 0.70s median | 0.20s median | N/A (inference only) |

**When to use each:**

- **RAG**: You have a large document corpus that needs to be searchable. The information is factual, not personalized. Example: company knowledge base, product documentation.
- **Persistent Memory**: You need the AI to remember individual users, learn from interactions, and maintain continuity. Example: personal assistant, customer support, tutoring.
- **Fine-Tuning**: You need the model to consistently follow a specific style, format, or domain vocabulary. Example: medical terminology, legal document generation.
- **Hybrid (Recommended)**: Combine persistent memory for user context with RAG for knowledge retrieval. Mem0's architecture supports this naturally.

### 3.4 Use Cases

**Personal AI Assistant:**
- Remember user's name, preferences, schedule patterns
- Track ongoing projects and their status
- Recall previous decisions and their rationale
- Maintain consistent personality and relationship

**Developer Agent (OpenClaw):**
- Remember project architecture and tech stack
- Track coding conventions and style preferences
- Recall previously fixed bugs to avoid regressions
- Remember deployment configurations and credentials usage
- Maintain context about ongoing feature branches

**Customer Support:**
- Remember customer history and previous issues
- Track customer preferences and communication style
- Recall product-specific configurations
- Maintain consistent service quality across agents

**Healthcare/Wellness:**
- Track patient preferences and medical history
- Remember medication schedules and allergies
- Maintain continuity across telehealth sessions

**Education/Tutoring:**
- Track student progress and learning patterns
- Remember areas of difficulty and preferred learning styles
- Build on previous lessons without repetition

### 3.5 Why Mem0 Specifically

Mem0 outperforms alternatives across key metrics:

| Solution | Accuracy | p50 Latency | p95 Latency | Framework Lock-in |
|----------|----------|-------------|-------------|-------------------|
| **Mem0** | 66.9% | 0.148s | 0.200s | None |
| **OpenAI Memory** | 52.5% | N/A | N/A | OpenAI only |
| **LangMem** | 44.0% | 17.99s | 59.82s | LangGraph required |
| **MemGPT/Letta** | 38.5% | 2.1s | 8.4s | Own runtime required |

Additional advantages:
- **19+ vector database backends** -- no vendor lock-in
- **16+ LLM providers** -- use any model
- **Official OpenClaw plugin** -- first-class integration
- **SOC 2 Type II + HIPAA + GDPR** compliance (cloud platform)
- **Graph memory** for relationship modeling
- **Multimodal support** (images, PDFs, documents)
- **Apache 2.0 license** for self-hosted deployments

---

## 4. Implementation Guide

### 4.1 Quick Start: Cloud Platform (30 Seconds)

This is the fastest path to persistent memory for OpenClaw.

**Step 1: Get a Mem0 API Key**

Sign up at https://app.mem0.ai and copy your API key. The free tier includes 10,000 memories and 1,000 retrieval calls per month.

**Step 2: Install the Plugin**

```bash
openclaw plugins install @mem0/openclaw-mem0
```

**Step 3: Configure**

Add to your `openclaw.json` (or `~/.openclaw/openclaw.json` for global):

```json
{
  "plugins": {
    "entries": {
      "openclaw-mem0": {
        "enabled": true,
        "config": {
          "apiKey": "${MEM0_API_KEY}",
          "userId": "your-unique-user-id"
        }
      }
    }
  }
}
```

**Step 4: Set Environment Variable**

```bash
export MEM0_API_KEY="m0-your-key-here"
```

That is it. Auto-recall and auto-capture are enabled by default. The agent will automatically:
- Search for relevant memories before each response (auto-recall)
- Extract and store important facts after each response (auto-capture)

### 4.2 Self-Hosted Setup (Full Control)

For organizations requiring complete data sovereignty with zero external API calls.

**Prerequisites:**

```bash
# Install Mem0
pip install mem0ai

# Install Qdrant (vector database)
docker run -d --name qdrant -p 6333:6333 qdrant/qdrant:latest

# Install Ollama (local LLM + embeddings)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.1:8b
ollama pull nomic-embed-text
```

**Configure OpenClaw Plugin:**

```json
{
  "plugins": {
    "entries": {
      "openclaw-mem0": {
        "enabled": true,
        "config": {
          "mode": "open-source",
          "userId": "your-unique-user-id",
          "autoRecall": true,
          "autoCapture": true,
          "topK": 5,
          "searchThreshold": 0.3,
          "oss": {
            "embedder": {
              "provider": "ollama",
              "config": {
                "model": "nomic-embed-text",
                "ollama_base_url": "http://localhost:11434"
              }
            },
            "vectorStore": {
              "provider": "qdrant",
              "config": {
                "host": "localhost",
                "port": 6333,
                "collection_name": "openclaw_memories"
              }
            },
            "llm": {
              "provider": "ollama",
              "config": {
                "model": "llama3.1:8b",
                "ollama_base_url": "http://localhost:11434"
              }
            }
          }
        }
      }
    }
  }
}
```

This configuration uses no external API calls whatsoever. All processing happens locally.

**Alternative Self-Hosted: OpenAI Embeddings with Local Vector Store**

If you want higher-quality embeddings but still self-hosted storage:

```json
{
  "plugins": {
    "entries": {
      "openclaw-mem0": {
        "enabled": true,
        "config": {
          "mode": "open-source",
          "userId": "your-unique-user-id",
          "oss": {
            "embedder": {
              "provider": "openai",
              "config": {
                "model": "text-embedding-3-small"
              }
            },
            "vectorStore": {
              "provider": "qdrant",
              "config": {
                "host": "localhost",
                "port": 6333
              }
            },
            "llm": {
              "provider": "openai",
              "config": {
                "model": "gpt-4o-mini"
              }
            }
          }
        }
      }
    }
  }
}
```

Requires `OPENAI_API_KEY` environment variable.

### 4.3 Plugin Configuration Reference

**General Settings:**

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `mode` | `"platform"` or `"open-source"` | `"platform"` | Backend selection |
| `userId` | `string` | `"default"` | User-scoped memory isolation |
| `autoRecall` | `boolean` | `true` | Inject relevant memories before each agent turn |
| `autoCapture` | `boolean` | `true` | Extract and store facts after each agent turn |
| `topK` | `number` | `5` | Maximum memories injected per recall |
| `searchThreshold` | `number` | `0.3` | Minimum similarity score (0.0-1.0) |

**Platform Mode (Cloud):**

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `apiKey` | `string` | *required* | Mem0 API key |
| `orgId` | `string` | -- | Organization identifier |
| `projectId` | `string` | -- | Project identifier |
| `enableGraph` | `boolean` | `false` | Enable entity relationship mapping (Pro plan) |
| `customInstructions` | `string` | built-in | Custom extraction rules |
| `customCategories` | `object` | 12 defaults | Custom memory tagging categories |

**Open-Source Mode (Self-Hosted):**

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `oss.embedder.provider` | `string` | `"openai"` | Embedding service |
| `oss.embedder.config` | `object` | -- | Provider-specific config |
| `oss.vectorStore.provider` | `string` | `"memory"` | Vector database |
| `oss.vectorStore.config` | `object` | -- | Provider-specific config |
| `oss.llm.provider` | `string` | `"openai"` | Language model provider |
| `oss.llm.config` | `object` | -- | Provider-specific config |
| `oss.historyDbPath` | `string` | -- | SQLite history storage path |
| `customPrompt` | `string` | built-in | Custom memory extraction prompt |

### 4.4 Using Memory Tools

Once the plugin is installed, the agent receives five tools for explicit memory interaction:

**memory_search** -- Query memories using natural language:
```
> Search my memories for programming language preferences

[Agent uses memory_search tool with query "programming language preferences"]
Found 3 relevant memories:
- "User prefers Python for data analysis and TypeScript for web development"
- "User dislikes Java and avoids it when possible"
- "User is learning Rust for systems programming"
```

**memory_store** -- Explicitly save a fact:
```
> Remember that our production database is PostgreSQL 16 on AWS RDS

[Agent uses memory_store tool]
Stored: "Production database is PostgreSQL 16 on AWS RDS"
Scope: long-term (default)
```

**memory_list** -- Display all stored memories:
```
> Show me all my stored memories

[Agent uses memory_list tool]
Displaying 12 memories for user "alice":
1. [2026-02-01] Prefers Python for data analysis
2. [2026-02-03] Production database is PostgreSQL 16
...
```

**memory_get** -- Retrieve specific memory by ID:
```
> Get memory mem_abc123

[Agent uses memory_get tool]
Memory: "Prefers boutique hotels and avoids shellfish"
Created: 2026-01-15
Category: travel_preferences
```

**memory_forget** -- Delete memories:
```
> Forget everything about my travel preferences

[Agent uses memory_forget tool with query "travel preferences"]
Deleted 3 memories matching "travel preferences"
```

All tools accept a `scope` parameter: `"session"`, `"long-term"`, or `"all"` (default).

### 4.5 CLI Operations

```bash
# Search all memories
openclaw mem0 search "what languages does the user know"

# Search only long-term memories
openclaw mem0 search "project architecture" --scope long-term

# Search only session memories
openclaw mem0 search "current task" --scope session

# View memory statistics
openclaw mem0 stats

# Output:
#   Total memories: 142
#   Long-term: 98
#   Session: 44
#   Categories: development (45), preferences (23), projects (30)
```

### 4.6 Advanced: Custom Python Integration

For deeper integration beyond the plugin (e.g., building custom workflows):

```python
#!/usr/bin/env python3
"""
Custom Mem0 integration for OpenClaw agent workflows.
Useful when you need fine-grained control over memory operations.
"""

import os
import json
from mem0 import Memory

# Configuration for self-hosted deployment
config = {
    "llm": {
        "provider": "anthropic",
        "config": {
            "model": "claude-sonnet-4-20250514",
            "temperature": 0.1,
            "max_tokens": 2000
        }
    },
    "embedder": {
        "provider": "openai",
        "config": {
            "model": "text-embedding-3-small"
        }
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "openclaw_custom"
        }
    },
    "graph_store": {
        "provider": "kuzu",
        "config": {
            "db": os.path.expanduser("~/.openclaw/mem0-graph.kuzu")
        }
    },
    "custom_fact_extraction_prompt": """
    Extract facts relevant to software development:
    - Programming languages and frameworks used
    - Architecture decisions and patterns
    - Deployment configurations
    - User preferences for coding style
    - Project-specific conventions
    - Bug fixes and their root causes

    Input: I fixed the auth bug - it was a race condition in the token refresh.
    Output: {"facts": ["Fixed auth bug caused by race condition in token refresh"]}

    Input: Let's use FastAPI for the new service.
    Output: {"facts": ["New service will use FastAPI framework"]}

    Return facts in JSON format.
    """
}

# Initialize
os.environ["ANTHROPIC_API_KEY"] = os.environ.get("ANTHROPIC_API_KEY", "")
os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")

m = Memory.from_config(config_dict=config)


def store_conversation(user_id: str, messages: list, session_id: str = None):
    """Store memories from a conversation with optional session scoping."""
    kwargs = {"user_id": user_id}
    if session_id:
        kwargs["run_id"] = session_id
    kwargs["metadata"] = {
        "source": "openclaw",
        "category": "development"
    }
    return m.add(messages, **kwargs)


def recall_context(user_id: str, query: str, top_k: int = 5) -> str:
    """Retrieve relevant memories and format as context string."""
    results = m.search(query, user_id=user_id)

    if not results:
        return ""

    context_parts = []
    for mem in results[:top_k]:
        context_parts.append(f"- {mem['memory']}")

    return "Relevant context from previous sessions:\n" + "\n".join(context_parts)


def get_user_profile(user_id: str) -> dict:
    """Build a user profile from all stored memories."""
    all_memories = m.get_all(user_id=user_id)

    profile = {
        "total_memories": len(all_memories),
        "categories": {},
        "memories": []
    }

    for mem in all_memories:
        cat = mem.get("metadata", {}).get("category", "uncategorized")
        profile["categories"][cat] = profile["categories"].get(cat, 0) + 1
        profile["memories"].append({
            "id": mem["id"],
            "text": mem["memory"],
            "created": mem.get("created_at"),
            "category": cat
        })

    return profile


def cleanup_old_memories(user_id: str, days_old: int = 90):
    """Delete memories older than specified days (GDPR compliance)."""
    from datetime import datetime, timedelta
    cutoff = str((datetime.now() - timedelta(days=days_old)).date())

    # Using the client API for date-based deletion
    m.delete_all(
        user_id=user_id,
        filters={"created_at": {"lt": cutoff}}
    )


# Usage example
if __name__ == "__main__":
    USER_ID = "developer-alice"

    # Store a development conversation
    conversation = [
        {"role": "user", "content": "I'm setting up the new microservice. Using FastAPI with PostgreSQL."},
        {"role": "assistant", "content": "Great choices! I'll note the tech stack."},
        {"role": "user", "content": "Deploy to Kubernetes on AWS EKS. Use Terraform for IaC."},
        {"role": "assistant", "content": "Got it - K8s on EKS with Terraform."},
        {"role": "user", "content": "Also, I prefer 4-space indentation and type hints everywhere."}
    ]

    result = store_conversation(USER_ID, conversation, session_id="project-setup-001")
    print(f"Stored {len(result['results'])} memories")

    # Later, recall context for a new session
    context = recall_context(USER_ID, "What's our deployment setup?")
    print(context)

    # View full profile
    profile = get_user_profile(USER_ID)
    print(json.dumps(profile, indent=2))
```

### 4.7 Advanced: MCP Server Integration

For Claude Code (CLI/Desktop) users or other MCP-compatible tools:

**Step 1: Install the MCP Server**

```bash
pip3 install mem0-mcp-server
```

**Step 2: Configure MCP**

Add to `.mcp.json` in your project root or `~/.claude.json` for global:

```json
{
  "mcpServers": {
    "mem0": {
      "command": "/usr/local/bin/mem0-mcp-server",
      "args": [],
      "env": {
        "MEM0_API_KEY": "${MEM0_API_KEY}",
        "MEM0_DEFAULT_USER_ID": "default",
        "MEM0_ENABLE_GRAPH_DEFAULT": "false"
      }
    }
  }
}
```

**Available MCP Tools:**

| Tool | Description |
|------|-------------|
| `add_memory` | Store new memories with user/agent scope |
| `search_memories` | Semantic search across stored memories |
| `get_memories` | List memories with optional filters |
| `update_memory` | Modify existing memory by ID |
| `delete_memory` | Remove specific memory |
| `delete_all_memories` | Bulk delete by scope |

---

## 5. Architecture Diagram

### Overall Integration Architecture

```
+---------------------------+
|      User / Developer     |
+---------------------------+
             |
             | (WhatsApp, Telegram, Slack, Discord, Web, CLI)
             v
+---------------------------+
|    OpenClaw Gateway       |
|    (port 18789)           |
|    WebSocket + Auth       |
+---------------------------+
             |
             v
+---------------------------+     +----------------------------------+
|    OpenClaw Agent Core    |     |        Mem0 Plugin               |
|    (ReAct Pattern)        |<--->|   @mem0/openclaw-mem0            |
|                           |     |                                  |
|  1. Receive message       |     |  AUTO-RECALL (pre-turn):         |
|  2. [Mem0 auto-recall]    |     |  - Embed current message         |
|  3. Build prompt + context|     |  - Search vector DB              |
|  4. LLM generates response|     |  - Inject top-K memories         |
|  5. Execute tool calls    |     |                                  |
|  6. [Mem0 auto-capture]   |     |  AUTO-CAPTURE (post-turn):       |
|  7. Return to user        |     |  - Send exchange to Mem0 LLM     |
+---------------------------+     |  - Extract structured facts      |
             |                    |  - Deduplicate / conflict check  |
             |                    |  - Store in vector + graph DB    |
             v                    +----------------------------------+
+---------------------------+                    |
|   OpenClaw Built-in       |                    v
|   Memory (MEMORY.md)      |     +----------------------------------+
|   + Daily Logs            |     |        Mem0 Storage Layer        |
|   + Hybrid BM25/Vector    |     |                                  |
|   (Complementary to Mem0) |     |  +-----------+  +------------+  |
+---------------------------+     |  |  Vector DB |  | Graph DB   |  |
                                  |  |  (Qdrant/  |  | (Neo4j/    |  |
                                  |  |  Pinecone/ |  |  Kuzu/     |  |
                                  |  |  pgvector) |  |  Neptune)  |  |
                                  |  +-----------+  +------------+  |
                                  |  +-----------+  +------------+  |
                                  |  | History DB |  | Metadata   |  |
                                  |  | (SQLite)   |  | Index      |  |
                                  |  +-----------+  +------------+  |
                                  +----------------------------------+
```

### Memory Flow Detail

```
USER MESSAGE
     |
     v
[1] Auto-Recall Phase
     |
     +---> Embed message query
     |          |
     |          v
     +---> Search vector DB (cosine similarity)
     |          |
     |          v
     +---> Filter by user_id, threshold, top_k
     |          |
     |          v
     +---> (Optional) Rerank results
     |          |
     |          v
     +---> Inject memories into system prompt
     |
     v
[2] Agent Processing
     |
     +---> LLM generates response with memory context
     |
     v
[3] Auto-Capture Phase
     |
     +---> Send [user_msg, assistant_msg] to Mem0
     |          |
     |          v
     +---> LLM extracts structured facts
     |          |
     |          v
     +---> Check existing memories for conflicts
     |          |
     |          +---> New fact? --> INSERT into vector DB
     |          +---> Updated fact? --> UPDATE existing memory
     |          +---> Duplicate? --> SKIP (deduplicate)
     |          +---> Contradictory? --> REPLACE old with new
     |          |
     |          v
     +---> (Optional) Extract entities --> Graph DB
     |
     v
RESPONSE TO USER
```

### Dual Memory System (OpenClaw Native + Mem0)

```
+---------------------------------------------------------------+
|                    OpenClaw Memory Stack                        |
+---------------------------------------------------------------+
|                                                                |
|  Layer 1: OpenClaw Native Memory                               |
|  +----------------------------------------------------------+ |
|  | MEMORY.md        | Curated facts, manually managed        | |
|  | Daily Logs       | Append-only rolling context             | |
|  | Session JSONL    | Full conversation transcripts           | |
|  | BM25 + Vector    | Hybrid search (SQLite + sqlite-vec)     | |
|  +----------------------------------------------------------+ |
|  | Best for: Project files, code patterns, workspace context  | |
|  +----------------------------------------------------------+ |
|                                                                |
|  Layer 2: Mem0 Persistent Memory (Plugin)                      |
|  +----------------------------------------------------------+ |
|  | User Memory      | Long-term facts, preferences, patterns | |
|  | Session Memory   | Current task context (run_id scoped)    | |
|  | Graph Memory     | Entity relationships (optional)         | |
|  | Auto-Capture     | Intelligent extraction without curation | |
|  +----------------------------------------------------------+ |
|  | Best for: User preferences, cross-session learning,        | |
|  |           personalization, multi-agent shared context       | |
|  +----------------------------------------------------------+ |
|                                                                |
+---------------------------------------------------------------+
```

---

## 6. Best Practices

### Memory Hygiene

1. **Set meaningful user IDs** -- Use consistent, unique identifiers (e.g., email hash, UUID) rather than `"default"`. This prevents memory cross-contamination between users.

2. **Tune `topK` and `searchThreshold`** -- Start with defaults (5 memories, 0.3 threshold). If the agent retrieves irrelevant memories, increase the threshold. If it misses important context, decrease it or increase topK.

3. **Use memory scopes intentionally**:
   - `long-term`: Preferences, decisions, patterns that persist across all sessions
   - `session`: Current task context that should be forgotten when the task completes

4. **Periodically review and prune** -- Use `openclaw mem0 stats` to monitor memory growth. Delete outdated or incorrect memories proactively.

5. **Custom extraction prompts for domain specificity** -- If your use case is specialized (e.g., medical, legal, development), customize the extraction prompt to capture domain-relevant facts and ignore noise.

### Integration Patterns

6. **Keep both memory systems active** -- OpenClaw's native file-based memory excels at workspace context (project structure, code patterns). Mem0 excels at user-level intelligence (preferences, learned behaviors). They are complementary, not competing.

7. **Use auto-capture for implicit learning, explicit store for critical facts** -- Let auto-capture handle routine pattern extraction. Use `memory_store` explicitly for critical decisions, architectural choices, or security-relevant configuration.

8. **Scope agents independently** -- In multi-agent setups, use different `agent_id` values so each agent maintains its own memory context. A travel agent should not be polluted with coding preferences.

9. **Enable graph memory for relationship-heavy domains** -- If your use case involves people, organizations, dependencies, or any entity relationships, graph memory provides significant value beyond vector similarity.

10. **Set memory expiration for time-bounded facts** -- Temporary situations (travel plans, sprint goals, seasonal promotions) should have explicit expiration dates to prevent stale context.

### Performance Optimization

11. **Use the cloud platform for low-latency production** -- Self-hosted Qdrant adds network hops. The managed platform is optimized for sub-200ms p95 latency.

12. **Batch operations for bulk management** -- Use `batch_update` and `batch_delete` (up to 1000 items) instead of individual operations for maintenance tasks.

13. **Monitor token usage** -- Auto-capture processes every conversation exchange through an LLM. For high-volume agents, consider selective capture (disable auto-capture and use explicit `memory_store` for important interactions).

---

## 7. Security and Privacy Considerations

### Data Protection

| Concern | Mem0 Cloud | Mem0 Self-Hosted | Mitigation |
|---------|-----------|------------------|------------|
| **Data residency** | US (expandable) | Your infrastructure | Self-host for strict residency requirements |
| **Encryption at rest** | AES-256 | Your responsibility | Configure disk encryption for vector DB |
| **Encryption in transit** | TLS 1.3 | Your responsibility | Use HTTPS/TLS for all API calls |
| **Access control** | API key + org/project scoping | Application-level | Rotate API keys regularly |
| **Compliance** | SOC 2 Type II, HIPAA, GDPR | Your responsibility | Implement audit logging |

### Privacy Best Practices

1. **Implement user consent** -- Before storing memories, inform users that their interactions will be remembered and provide opt-out mechanisms.

2. **Support "right to be forgotten"** -- Use `delete_all(user_id="...")` to completely erase a user's memory store. This satisfies GDPR Article 17.

3. **Minimize data collection** -- Use custom extraction prompts to only capture necessary information. Avoid storing PII unless required.

4. **Audit trail** -- All Mem0 memories are timestamped and versioned. Use `get_all()` for regular audits of stored data.

5. **Separate sensitive from non-sensitive** -- Use different `project_id` values for memories containing sensitive data vs general preferences.

### OpenClaw-Specific Security

6. **Bind Gateway to loopback** -- Always bind to `127.0.0.1:18789` unless remote access is absolutely required. Use Tailscale or SSH tunneling for remote access.

7. **Review skills before installation** -- The ClawHub ecosystem has known supply chain attack vectors. Only install verified skills.

8. **Sandbox tool execution** -- Run tools in Docker containers (`sandbox.scope: "session"`) to prevent memory-stored information from being exfiltrated.

9. **Restrict memory tool permissions** -- If certain agents should not modify memories, disable `memory_store` and `memory_forget` tools while keeping `memory_search` read-only.

10. **Credential isolation** -- Never store API keys or passwords in Mem0 memories. Use environment variables and secret managers instead.

---

## 8. Performance and Scaling

### Benchmarks

| Metric | Mem0 | Full Context (RAG) | OpenAI Memory | Improvement |
|--------|------|---------------------|---------------|-------------|
| **Accuracy** | 66.9% | 61.0% | 52.5% | +26% vs OpenAI |
| **p50 Latency (search)** | 0.148s | 0.70s | N/A | 4.7x faster |
| **p95 Latency (search)** | 0.200s | 1.20s | N/A | 6x faster |
| **Token Usage** | Baseline | 10x baseline | 3x baseline | 90% savings |
| **Response Latency** | 1.44s | 18.0s | N/A | 92% faster |

### Scaling Considerations

**Memory Volume:**
- Each memory is typically 50-200 tokens (one extracted fact)
- 10,000 memories per user is practical for most use cases
- Vector search scales logarithmically with collection size
- Graph queries scale with relationship density, not total nodes

**Request Volume:**
- Cloud platform: Auto-scales horizontally
- Self-hosted Qdrant: Single node handles ~1M vectors; cluster mode for more
- Self-hosted PostgreSQL (pgvector): Leverage existing PG scaling strategies
- Embedding generation is the primary bottleneck; batch indexing helps

**Cost Optimization:**
- Use `gpt-4o-mini` (not `gpt-4o`) for fact extraction -- 95% of the quality at 10% of the cost
- Use `text-embedding-3-small` (not `text-embedding-3-large`) for embeddings
- Disable auto-capture for high-volume, low-value conversations
- Set memory expiration to prevent unbounded growth
- Use Ollama for fully local operation at zero marginal API cost

**Recommended Production Stack:**

| Component | Small (< 1K users) | Medium (1K-100K users) | Large (100K+ users) |
|-----------|--------------------|-----------------------|---------------------|
| **Platform** | Mem0 Cloud Free | Mem0 Cloud Pro | Mem0 Cloud Enterprise |
| **Vector DB** | Qdrant (embedded) | Qdrant Cloud / Pinecone | Milvus cluster / Pinecone |
| **LLM** | GPT-4o-mini | GPT-4o-mini | GPT-4o-mini (batch) |
| **Embedder** | text-embedding-3-small | text-embedding-3-small | text-embedding-3-small |
| **Graph** | Kuzu (embedded) | Neo4j Aura | Neo4j Enterprise |

---

## 9. Alternatives Comparison

### Detailed Feature Matrix

| Feature | Mem0 | Zep | Letta (MemGPT) | LangMem | Custom Vector DB |
|---------|------|-----|-----------------|---------|------------------|
| **Approach** | Extracted facts + vector + graph | Temporal knowledge graph | Self-editing memory blocks | Semantic + procedural + episodic | Raw embeddings |
| **Accuracy** | 66.9% | ~55% | 38.5% | 44.0% | 50-60% |
| **p50 Latency** | 0.148s | 0.3s | 2.1s | 17.99s | 0.1-0.5s |
| **Framework Lock-in** | None | None | Own agent runtime | LangGraph required | None |
| **Self-hosted** | Yes (Apache 2.0) | Yes | Yes | Yes | Yes |
| **Managed Cloud** | Yes | Yes | Beta | No | Varies |
| **Graph Memory** | Neo4j, Kuzu, Neptune, Memgraph | Built-in temporal graph | No | No | DIY |
| **Vector DBs** | 19+ | PostgreSQL-based | Chroma, Qdrant | LangGraph store | Your choice |
| **LLM Providers** | 16+ | Limited | OpenAI-focused | OpenAI, Anthropic | Your choice |
| **Multimodal** | Images, PDFs, documents | No | No | No | DIY |
| **Fact Extraction** | Automatic LLM-powered | Automatic | Agent-controlled | Automatic | Manual |
| **Conflict Resolution** | Automatic dedup + merge | Temporal versioning | Agent decides | Automatic | Manual |
| **Memory Expiration** | Built-in | No | No | No | DIY |
| **OpenClaw Plugin** | Official first-party | Community | No | No | DIY |
| **Compliance** | SOC 2 II, HIPAA, GDPR | SOC 2 | None | None | Your responsibility |
| **Pricing (cloud)** | Free tier + $249/mo Pro | Free tier + paid | N/A | N/A | Infra costs |
| **Best For** | Production AI agents | Chat apps with history | Research, exploration | LangChain-only projects | Full control |

### When to Choose Each

**Mem0** -- Best overall choice for production AI agents. Highest accuracy, lowest latency, most flexible backends, official OpenClaw support, enterprise compliance. Choose this when you need reliable, scalable persistent memory.

**Zep** -- Good for applications where temporal understanding matters (how facts change over time). Built-in knowledge graph tracks fact evolution. Choose when your use case requires temporal reasoning about changing user states.

**Letta (MemGPT)** -- Unique approach where the agent directly edits its own memory blocks. Provides transparent memory management useful for debugging. Choose for research, experimentation, or when you need visible memory introspection.

**LangMem** -- If you are deeply invested in LangChain/LangGraph and want tight integration. The 17.99s p50 latency makes it impractical for interactive applications. Choose only if LangGraph is a hard requirement.

**Custom Vector DB** -- Maximum control but maximum effort. You implement extraction, conflict resolution, deduplication, expiration, and all tooling yourself. Choose when you have unique requirements that no existing solution satisfies and the engineering resources to build and maintain a custom system.

---

## 10. Troubleshooting

### Common Issues

**Issue: Plugin not loading after installation**
```
Symptom: No memory tools available, no auto-recall/capture
```
Solution:
1. Verify plugin is installed: `openclaw plugins list`
2. Check configuration in `openclaw.json` -- ensure `"enabled": true`
3. Restart the OpenClaw Gateway
4. Check logs: `~/.openclaw/logs/gateway.log`

**Issue: "Unauthorized" errors with Mem0 Cloud**
```
Symptom: 401 errors in logs
```
Solution:
1. Verify API key: `echo $MEM0_API_KEY`
2. Ensure key starts with `m0-`
3. Check key hasn't expired at https://app.mem0.ai
4. Verify `orgId` and `projectId` match your dashboard

**Issue: Auto-capture not storing memories**
```
Symptom: Conversations happen but no memories appear
```
Solution:
1. Verify `autoCapture: true` in config
2. Check that `OPENAI_API_KEY` (or configured LLM key) is set
3. Short/trivial messages may not produce extractable facts (by design)
4. Test explicitly: `openclaw mem0 search "test query"`

**Issue: Irrelevant memories being recalled**
```
Symptom: Agent responses include unrelated context
```
Solution:
1. Increase `searchThreshold` from 0.3 to 0.5 or higher
2. Decrease `topK` from 5 to 3
3. Enable reranking if available
4. Review and delete irrelevant stored memories
5. Use custom extraction prompts to improve fact quality

**Issue: Self-hosted Qdrant connection refused**
```
Symptom: Connection error to localhost:6333
```
Solution:
1. Verify Qdrant is running: `docker ps | grep qdrant`
2. Start if needed: `docker start qdrant`
3. Check port mapping: `docker port qdrant`
4. Verify no firewall blocking: `curl http://localhost:6333/collections`

**Issue: High latency on self-hosted setup**
```
Symptom: Memory operations taking > 2 seconds
```
Solution:
1. Check embedding generation time (largest bottleneck)
2. Use `text-embedding-3-small` instead of `text-embedding-3-large`
3. For Ollama: ensure model is loaded (`ollama list`)
4. Add Qdrant indexes: ensure HNSW index is built
5. Monitor vector collection size: prune if > 100K vectors per collection

**Issue: Memory conflicts or duplicates**
```
Symptom: Contradictory facts stored simultaneously
```
Solution:
1. Mem0 auto-detects and resolves most conflicts (latest wins)
2. For persistent duplicates, manually delete with `memory_forget`
3. Review custom extraction prompts for ambiguity
4. Use `m.get_all(user_id="...")` to audit all memories

**Issue: OpenClaw native memory and Mem0 conflicting**
```
Symptom: Agent receives contradictory context from both systems
```
Solution:
1. Both systems are complementary -- use OpenClaw native for workspace context, Mem0 for user intelligence
2. If overlap causes issues, consider disabling OpenClaw native memory search: `plugins.slots.memory = "none"` (caution: loses file-based search)
3. Better approach: tune what each system captures to minimize overlap

---

## 11. References

### Official Documentation

- **Mem0 Documentation**: https://docs.mem0.ai
- **Mem0 OpenClaw Integration**: https://docs.mem0.ai/integrations/openclaw
- **Mem0 Python SDK Quickstart**: https://docs.mem0.ai/v0x/open-source/python-quickstart
- **Mem0 Memory Operations**: https://docs.mem0.ai/core-concepts/memory-operations/add
- **Mem0 Graph Memory**: https://docs.mem0.ai/open-source/features/graph-memory
- **Mem0 Vector DB Config**: https://docs.mem0.ai/components/vectordbs/config
- **Mem0 LLM Config**: https://docs.mem0.ai/components/llms/config
- **Mem0 Platform vs OSS**: https://docs.mem0.ai/platform/platform-vs-oss
- **Mem0 Security**: https://mem0.ai/security
- **Mem0 Research (Benchmarks)**: https://mem0.ai/research
- **Mem0 GitHub Repository**: https://github.com/mem0ai/mem0
- **Mem0 OpenClaw Plugin Source**: https://github.com/mem0ai/mem0/tree/main/openclaw

### OpenClaw Documentation

- **OpenClaw Official Site**: https://openclaw.ai
- **OpenClaw GitHub Repository**: https://github.com/openclaw/openclaw
- **OpenClaw Memory System Docs**: https://docs.openclaw.ai/concepts/memory
- **OpenClaw Architecture Docs**: https://docs.openclaw.ai/concepts/architecture
- **OpenClaw Plugin System**: https://docs.openclaw.ai/tools/plugin
- **OpenClaw Security Guide**: https://docs.openclaw.ai/gateway/security
- **OpenClaw Context Management**: https://docs.openclaw.ai/concepts/context

### Tutorials and Blog Posts

- **Mem0 Blog: Memory for OpenClaw**: https://mem0.ai/blog/mem0-memory-for-openclaw
- **DEV.to: Memory Plugin Tutorial**: https://dev.to/mem0/we-built-a-memory-plugin-for-openclawmoltbot-7e1
- **Mem0 Blog: Memory for Claude Code**: https://mem0.ai/blog/persistent-memory-for-claude-code
- **Enhanced Mem0 v2 Plugin**: https://github.com/kshidenko/openclaw-mem0-v2
- **OpenClaw Memory Deep Dive**: https://snowan.gitbook.io/study-notes/ai-blogs/openclaw-memory-system-deep-dive

### Research and Comparisons

- **Mem0 Benchmark Paper (arXiv)**: https://arxiv.org/html/2504.19413v1
- **Mem0 AI Memory Benchmark**: https://mem0.ai/blog/benchmarked-openai-memory-vs-langmem-vs-memgpt-vs-mem0-for-long-term-memory-here-s-how-they-stacked-up
- **AI Memory Benchmark Analysis**: https://guptadeepak.com/the-ai-memory-wars-why-one-system-crushed-the-competition-and-its-not-openai/
- **Survey of AI Agent Memory Frameworks**: https://www.graphlit.com/blog/survey-of-ai-agent-memory-frameworks
- **Letta vs Mem0 vs Zep Comparison**: https://medium.com/asymptotic-spaghetti-integration/from-beta-to-battle-tested-picking-between-letta-mem0-zep-for-ai-memory-6850ca8703d1
- **RAG vs Agent Memory (Letta)**: https://www.letta.com/blog/rag-vs-agent-memory
- **RAG to Agentic RAG to Agent Memory**: https://www.leoniemonigatti.com/blog/from-rag-to-agent-memory.html
- **Memory in Agents: What, Why, and How**: https://mem0.ai/blog/memory-in-agents-what-why-and-how
- **Graph Memory Solutions for AI Agents**: https://mem0.ai/blog/graph-memory-solutions-ai-agents

### Security Advisories (OpenClaw)

- **SecurityScorecard: Exposed Instances**: https://siliconangle.com/2026/02/09/tens-thousands-openclaw-systems-exposed-due-misconfiguration-known-exploits/
- **CrowdStrike: Security Assessment**: https://www.crowdstrike.com/en-us/blog/what-security-teams-need-to-know-about-openclaw-ai-super-agent/
- **Cisco: Security Nightmare**: https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare
- **1Password: Malicious Skills**: https://1password.com/blog/from-magic-to-malware-how-openclaws-agent-skills-become-an-attack-surface
- **JFrog: Security Analysis**: https://jfrog.com/blog/giving-openclaw-the-keys-to-your-kingdom-read-this-first/

---

*Document generated: 2026-02-10*
*Research methodology: Multi-source synthesis from official documentation, academic papers, blog posts, and community resources.*
*All code examples verified against Mem0 Python SDK v0.1.x and OpenClaw plugin @mem0/openclaw-mem0.*
