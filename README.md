# Research//Manager

**Multi-source AI web research agent with a live-streaming Gradio UI, PDF/Word export, and email/push delivery — built on the OpenAI Agents SDK.**

Research//Manager takes a plain-language research question, plans a set of targeted web searches, runs them in parallel, synthesizes the results into a long-form markdown report, emails/pushes it to you, and lets you download the finished report as a **PDF** or **Word document** — all from a single dark-themed web page.

![System status](https://img.shields.io/badge/status-active-brightgreen) ![Python](https://img.shields.io/badge/python-3.11%2B-blue) ![Gradio](https://img.shields.io/badge/UI-Gradio-orange)

---

## ✨ Features

- **Multi-agent research pipeline** — a planner agent decomposes your query into targeted search terms, a search agent (backed by Tavily) executes them in parallel, and a writer agent synthesizes everything into a structured, 1000+ word markdown report.
- **Multi-provider model routing** — different agents run on different LLM providers/models: NVIDIA-hosted Nemotron models for planning and writing, Google Gemini for search summarization, and Llama 3.3 (via NVIDIA) for email drafting — all through the OpenAI-compatible `AsyncOpenAI` client.
- **Live streaming UI** — Gradio front end streams each pipeline stage ("Searches planned…", "Writing report…", etc.) to the page in real time, with a pulsing "Researching…" indicator.
- **Cooperative Stop button** — cancel a running query cleanly between pipeline steps without corrupting Gradio's task queue.
- **Automatic retries** — transient provider errors (HTTP 429/5xx) are retried with exponential backoff + jitter, without swallowing cancellation signals.
- **One-click export** — every finished report can be downloaded as a **PDF** or a **.docx** Word document, generated on the fly from the markdown output.
- **Delivery on completion** — the finished report is emailed via SMTP, or sent as a Pushover push notification, depending on configuration.
- **Local tracing** — every run is traced (agent/LLM/tool spans, timings, hierarchy) to a local `traces.json5` file instead of OpenAI's hosted trace dashboard, so no extra API key or network call is required for observability.

---

## 🖥️ Demo

**Query:**

> *"Top Defence companies in Nigeria specializing in armoured vehicles in 2026"*

The app streamed live status updates while researching, then rendered the full report inline and exposed **Download as PDF** / **Download as Word** buttons:

| Query & landing page                                                             | Rendered report + downloads                                                                       |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------- |
| Enter a question, hit **Investigate**, or pick one of the example prompts | Full markdown report renders in the page; PDF/DOCX export buttons appear once the report is ready |

A screen recording of a full run is included at [`generated_outputs/generated_report_vid.mp4`](generated_outputs/generated_report_vid.mp4), alongside the actual generated files from that run:

- [`generated_outputs/research_report_ea6c8a11.pdf`](generated_outputs/research_report_ea6c8a11.pdf)
- [`generated_outputs/research_report_ea6c8a11.docx`](generated_outputs/research_report_ea6c8a11.docx)
- [`generated_outputs/query.txt`](generated_outputs/query.txt) — the exact query used

The generated report includes an executive summary, methodology, market landscape, individual company deep-dives (DICON, Dyon X-Shield, Innoson, Imperium Industries, Proforce Defence, Epail Nigeria), a product portfolio matrix, SWOT analysis, a 2027–2032 outlook, stakeholder recommendations, and a references section.

---

## 🏗️ Architecture

```
User query
   │
   ▼
Gradio UI (app.py)
   │  streams status updates
   ▼
ResearchManager.run()  (research_manager.py)
   │
   ├── 1. plan_searches()   → planner_agent   (Nemotron 3 Super 120B)
   ├── 2. perform_searches()→ search_agent    (Gemini 3.1 Flash-Lite + Tavily web_search tool)
   ├── 3. write_report()    → writer_agent    (Nemotron 3 Ultra 550B)
   └── 4. send_email()      → email_agent     (Llama 3.3 70B) → SMTP or Pushover
   │
   ▼
report_export.py → builds PDF (fpdf2) and DOCX (python-docx) from the markdown report
   │
   ▼
Gradio DownloadButtons (PDF / Word)
```

Every agent call goes through `run_with_retry()` (`rerun_func.py`), which retries on transient provider errors (`408/409/429/500/502/503/504`) with exponential backoff, while still letting `asyncio.CancelledError` propagate so the Stop button works.

Tracing is handled by a custom `LocalFileTraceProcessor` in `research_manager.py`, which replaces the SDK's default (hosted) trace processor so runs are logged locally instead of requiring an OpenAI tracing API key.

---

## 📁 Project structure

```
Research_Agent_openAI_SDK/
├── app.py                     # Gradio UI, event wiring, streaming, download buttons
├── research_manager.py        # Orchestrates the 4-step research pipeline + local tracing
├── agentss/                   # Agent definitions (named to avoid colliding with the
│   │                          #   installed `agents` package — see Known Issues below)
│   ├── planner_agent.py       # Plans N web searches for a given query
│   ├── search_agent.py        # Executes a single search via the web_search tool
│   ├── writer_agent.py        # Synthesizes search results into a full markdown report
│   ├── email_agent.py         # Converts the report into an HTML email and sends it
│   └── rerun_func.py          # run_with_retry() — retry/backoff wrapper around Runner.run()
├── tools/
│   ├── web_search.py          # Tavily-backed @function_tool used by search_agent
│   ├── report_export.py       # Markdown → PDF / DOCX conversion + Gradio download callback
│   └── messenger.py           # SMTP email sending + Pushover push notifications
├── css_styles/
│   └── styles.py               # CSS, JS, example queries, header HTML for the Gradio UI
├── generated_outputs/          # Sample run artifacts (PDF, DOCX, query, screen recording)
├── traces.json5                 # Local JSONL trace log (created at runtime)
├── requirements.txt
├── .env                          # Local secrets (not committed — see below)
└── README.md
```

> **Note:** the local agent package is named `agentss/` (not `agents/`) specifically to avoid shadowing the installed `openai-agents` SDK, which is itself imported as top-level `agents`. See [Known Issues](#-known-issues--gotchas) for details.

---

## ⚙️ Setup

### 1. Clone and create an environment

```bash
git clone https://github.com/Shakpro10/DEEP_RESEARCHER-MULTI-AGENT-AI-RESEARCH-TEAM.git
cd Research_Agent_openAI_SDK
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

Core dependencies: `gradio`, `openai`, `openai-agents`, `pydantic`, `python-dotenv`, `tavily-python`, `requests`, `python-docx`, `fpdf2`.

### 3. Configure environment variables

Create a `.env` file in the project root:

```env
# LLM providers
NVIDIA_API_KEY_1=your_nvidia_api_key
GOOGLE_API_KEY=your_gemini_api_key

# Web search
TAVILY_API_KEY=your_tavily_api_key

# Delivery method — set USE_EMAIL=false to use Pushover instead of SMTP
USE_EMAIL=true

# SMTP (used when USE_EMAIL=true)
EMAIL_ADDRESS=you@example.com
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_APP_PASSWORD=your_app_password

# Pushover (used when USE_EMAIL=false)
PUSHOVER_USER=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token

# Optional
HOW_MANY_SEARCHES=5
```

### 4. Run the app

```bash
python app.py
```

Gradio will start a local server (default `http://127.0.0.1:7860`). Open it in your browser, type a research question (or pick one of the example prompts), and click **Investigate**.

---

## 🧭 Usage

1. Enter a research question, e.g. *"Top AI companies in Nigeria in 2026"*, or click one of the example prompts.
2. Click **Investigate** (or press Enter). The button swaps for a **Stop** button and a pulsing "Researching…" indicator appears.
3. Status updates stream live as the pipeline plans searches, executes them, and writes the report.
4. Once complete, the full markdown report renders in the page, an email/push notification is sent, and **Download as PDF** / **Download as Word** buttons appear.
5. Click **Stop** at any point to cooperatively cancel the current run between pipeline steps.

---

## 🐛 Known issues & gotchas

These were hit and resolved during development — documented here for anyone extending the project:

1. **Local package name collision with the SDK.** The `openai-agents` package installs itself as top-level `agents`. A local folder also named `agents/` shadows it, since the script directory is searched first on `sys.path`. **Fix:** the local package is named `agentss/`, and its own submodules are imported absolutely (e.g. `from tools.web_search import web_search`) rather than via relative imports, which also avoids `ImportError: attempted relative import beyond top-level package` when a module tries to `from ..tools import ...` from a top-level package with no parent.
2. **`openai` 2.45.0+ breaking change.** OpenAI added a new *required* field, `cache_write_tokens`, to `InputTokensDetails`. `openai-agents` versions prior to the fix (released in [openai/openai-agents-python#3773](https://github.com/openai/openai-agents-python/issues/3773)) construct that object with only `cached_tokens`, causing every run to fail immediately with a `pydantic.ValidationError` — independent of model or provider. **Fix:** upgrade to `openai-agents >= 0.19.4` (or pin `openai==2.44.0` as a stopgap).
3. **Gradio task cancellation vs. cooperative cancellation.** Using Gradio's built-in `cancels=[...]` task cancellation left the Stop button's queue bookkeeping inconsistent across repeated runs. The app instead passes a fresh `asyncio.Event` into `ResearchManager.run()` each run, which checks it between pipeline steps — this can't interrupt a model call already in flight, but always leaves the UI in a consistent state afterward.

---

## 🛠️ Tech stack

- **Orchestration:** [OpenAI Agents SDK](https://openai.github.io/openai-agents-python/) (`openai-agents`)
- **UI:** [Gradio](https://www.gradio.app/) (Blocks API, streaming generators, queued events)
- **LLM providers:** NVIDIA NIM (Nemotron, Llama 3.3), Google Gemini — all via the OpenAI-compatible `AsyncOpenAI` client
- **Web search:** [Tavily](https://tavily.com/) Search API
- **Document export:** [`python-docx`](https://python-docx.readthedocs.io/) and [`fpdf2`](https://pyfpdf.github.io/fpdf2/)
- **Delivery:** SMTP (`smtplib`) or [Pushover](https://pushover.net/)
- **Validation:** [Pydantic](https://docs.pydantic.dev/)

---

## 📄 License

MIT License

Copyright (c) 2026 Shakiru Sikiru

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## 🙋 Acknowledgements

Built on the OpenAI Agents SDK research-agent pattern, extended with a production-style local trace processor, cooperative cancellation, multi-provider model routing, and one-click PDF/Word export.
