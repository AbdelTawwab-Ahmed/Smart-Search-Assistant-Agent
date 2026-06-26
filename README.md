# Smart Research Assistant

> An **autonomous research agent** powered by LangChain that researches topics, performs calculations, and generates structured reports—demonstrating production-grade GenAI patterns.


## 🎯 Overview

A terminal-based AI agent that autonomously:
- **Research** topics using multi-turn conversations
- **Calculate** complex math problems with tool-calling
- **Reverse text & manipulate strings** on demand
- **Generate formatted markdown reports** with structured insights
- **Maintain conversation memory** across sessions

Built to showcase **LangChain Week 1 fundamentals** in a real-world workflow.


## ⚙️ Core Technologies

- **LangChain** — agentic AI framework & LCEL chains
- **Gemini 2.5 Flash** — LLM backbone
- **Python 3.9+** — implementation language
- **Structured Output Parsing** — JSON & markdown generation


## 🚀 Quick Start

```bash
git clone https://github.com/AbdelTawwab-Ahmed/Smart-Research-Assistant.git
cd Smart-Research-Assistant

pip install -r requirements.txt
export GOOGLE_API_KEY="your-key-here"

python main.py
```


## 📁 Project Structure


        ├── main.py              # Terminal interface & agent orchestration

        ├── tools/               # Custom research & calculation tools

        ├── agents/              # Agent definitions & memory handling

        ├── reports/             # Generated markdown summaries

        └── requirements.txt     # Dependencies



## ✨ Features

✅ Conversation memory (session persistence)  
✅ Multi-tool agent loops (research, math, text ops)  
✅ LCEL chain composition  
✅ Structured JSON/Markdown output parsing  
✅ Production-ready error handling  

## 📚 What You'll Learn

- Tool-calling agentic loops
- Prompt engineering & system messages
- Output parsers (JSON, structured)
- ReAct reasoning patterns
- LangGraph integration

---

**Portfolio piece for:** AI Engineers, LLM builders, GenAI practitioners  
**Built with:** LangChain, Gemini API, Python