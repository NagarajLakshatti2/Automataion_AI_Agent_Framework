# JeshlaAIAgent - Complete Setup & Execution Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Project Structure Diagram](#project-structure-diagram)
3. [End-to-End Architecture Flow](#end-to-end-architecture-flow)
4. [Prerequisites](#prerequisites)
5. [Installation Guide](#installation-guide)
6. [IDE Setup](#ide-setup)
7. [Execution Guide](#execution-guide)
8. [Configuration](#configuration)
9. [Troubleshooting](#troubleshooting)
10. [Development Workflow](#development-workflow)

---

## Project Overview

JeshlaAIAgent is an advanced agentic AI code assistant built with free, open-source modules. It provides three main interfaces:
- **Chat**: Natural language conversation with AI
- **Plan**: AI-powered task planning and execution
- **Agents**: Specialized agents for code operations

---

## Project Structure Diagram

```
JeshlaAIAgent/
│
├── .env                          # Environment configuration (API keys, settings)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── SETUP_GUIDE.md                # This file - Complete setup guide
├── test_basic.py                 # Basic functionality test
│
├── config/                       # Configuration Layer
│   ├── __init__.py
│   ├── settings.py              # Settings management (loads .env)
│   └── prompts.py               # System prompts for all agents
│
├── core/                         # Core Business Logic
│   ├── __init__.py
│   │
│   ├── llm/                     # LLM Provider Layer
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract base interface
│   │   ├── ollama_provider.py   # Ollama (local, free)
│   │   ├── openrouter_provider.py  # OpenRouter (cloud, free tier)
│   │   └── google_provider.py   # Google AI Studio (cloud, free tier)
│   │
│   ├── planner/                 # Planning System
│   │   ├── __init__.py
│   │   ├── task_planner.py      # AI-powered task decomposition
│   │   ├── plan_executor.py     # Execute plans step-by-step
│   │   └── plan_tracker.py      # Track plan history & stats
│   │
│   ├── agents/                  # Agent Layer
│   │   ├── __init__.py
│   │   ├── agent_orchestrator.py  # Coordinate all agents
│   │   ├── code_generator.py    # Generate code from NL
│   │   ├── code_converter.py    # Convert between languages
│   │   ├── code_reviewer.py     # Review code quality
│   │   ├── file_agent.py        # File operations
│   │   ├── git_agent.py         # Git operations
│   │   ├── test_agent.py        # Test generation & execution
│   │   ├── debug_agent.py       # Debugging assistance
│   │   └── refactor_agent.py    # Code refactoring
│   │
│   └── tools/                   # Core Tools
│       ├── __init__.py
│       ├── file_ops.py          # File read/write/list
│       ├── git_ops.py           # Git status/commit/branch
│       ├── test_runner.py       # Pytest/unittest execution
│       ├── code_parser.py       # Multi-language parsing
│       ├── debugger.py          # Error analysis
│       └── search.py            # Code search (keyword/regex)
│
├── rag/                         # RAG (Retrieval-Augmented Generation)
│   ├── __init__.py
│   ├── indexer.py               # Index codebase for search
│   ├── vector_store.py          # ChromaDB vector storage
│   └── retriever.py             # Context retrieval
│
├── ui/                          # Streamlit UI Layer
│   ├── __init__.py
│   ├── app.py                   # Main application entry point
│   │
│   ├── pages/                   # Page implementations
│   │   ├── __init__.py
│   │   ├── chat.py              # Chat page (integrated in app.py)
│   │   ├── plan.py              # Plan page (integrated in app.py)
│   │   └── agents.py            # Agents page (integrated in app.py)
│   │
│   ├── components/              # Reusable UI components
│   │   ├── __init__.py
│   │   ├── chat_interface.py    # Chat UI component
│   │   ├── plan_viewer.py       # Plan display & execution
│   │   ├── agent_status.py      # Agent dashboard
│   │   ├── code_editor.py       # Code display with syntax highlighting
│   │   ├── file_browser.py      # File tree browser
│   │   ├── settings_panel.py    # Settings configuration
│   │   └── terminal.py         # Terminal output display
│   │
│   └── styles/
│       └── custom.css           # Custom styling (if needed)
│
├── utils/                       # Utility Functions
│   ├── __init__.py
│   ├── logger.py                # Logging configuration
│   └── helpers.py               # Helper functions
│
└── tests/                       # Test Files
    ├── __init__.py
    ├── test_llm.py              # LLM provider tests
    ├── test_agents.py           # Agent tests
    └── test_rag.py              # RAG tests
```

---

## End-to-End Architecture Flow

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                    (Streamlit Web UI)                        │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │  Chat    │  │  Plan    │  │  Agents  │                  │
│  │ Section  │  │ Section  │  │ Section  │                  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘                  │
└───────┼─────────────┼─────────────┼────────────────────────┘
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LOGIC                          │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │           Agent Orchestrator                       │    │
│  │  - Routes tasks to appropriate agents              │    │
│  │  - Manages agent coordination                     │    │
│  └────────────────────┬───────────────────────────────┘    │
│                       │                                     │
│       ┌───────────────┼───────────────┐                    │
│       ▼               ▼               ▼                    │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐                 │
│  │ Planner │   │  Agents │   │   RAG   │                 │
│  └────┬────┘   └────┬────┘   └────┬────┘                 │
│       │             │             │                         │
└───────┼─────────────┼─────────────┼────────────────────────┘
        │             │             │
        ▼             ▼             ▼
┌─────────────────────────────────────────────────────────────┐
│                    CORE LAYER                                 │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ LLM Provider │  │   Tools      │  │   Config     │     │
│  │ - Ollama     │  │ - File Ops   │  │ - Settings    │     │
│  │ - OpenRouter │  │ - Git Ops    │  │ - Prompts     │     │
│  │ - Google     │  │ - Test Runner│  │              │     │
│  └──────────────┘  │ - Code Parser│  └──────────────┘     │
│                    │ - Debugger   │                        │
│                    │ - Search     │                        │
│                    └──────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

### Detailed Flow Diagram

```
USER INPUT
    │
    ▼
┌──────────────────┐
│ Streamlit UI     │
│ (Chat/Plan/Agent)│
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Route to Appropriate Handler        │
│                                      │
│ Chat → Chat Interface Component      │
│ Plan → Plan Viewer Component         │
│ Agent → Agent Status Component       │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Agent Orchestrator                  │
│                                      │
│ - Determine agent type               │
│ - Initialize agent                   │
│ - Execute task                       │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Specialized Agent Execution          │
│                                      │
│ [Code Generator]                    │
│ [Code Converter]                    │
│ [Code Reviewer]                     │
│ [File Agent]                        │
│ [Git Agent]                         │
│ [Test Agent]                        │
│ [Debug Agent]                       │
│ [Refactor Agent]                    │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Tool Layer (if needed)               │
│                                      │
│ - File Operations                    │
│ - Git Operations                     │
│ - Test Execution                     │
│ - Code Parsing                       │
│ - Debugging                          │
│ - Search                            │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ LLM Provider Layer                  │
│                                      │
│ - Ollama (local)                    │
│ - OpenRouter (cloud)                 │
│ - Google AI Studio (cloud)          │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ RAG Layer (optional context)         │
│                                      │
│ - Codebase Indexer                   │
│ - Vector Store (ChromaDB)           │
│ - Context Retriever                  │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Response Generation                 │
│                                      │
│ - Format response                    │
│ - Add code blocks                    │
│ - Include context                    │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│ Display in UI                       │
│                                      │
│ - Chat message                       │
│ - Plan status                       │
│ - Agent result                       │
└──────────────────────────────────────┘
```

---

## Prerequisites

### System Requirements

**Minimum Requirements:**
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **RAM**: 8GB (16GB recommended for Ollama)
- **Storage**: 5GB free space
- **Python**: 3.8 or higher (3.10+ recommended)

**For Ollama (Local LLM):**
- **RAM**: 16GB recommended
- **GPU**: NVIDIA GPU with CUDA support (optional but recommended)
- **Storage**: Additional 10GB for model files

### Software Requirements

1. **Python 3.8+**
   - Download from https://www.python.org/downloads/
   - Install with "Add to PATH" option

2. **Git** (optional, for version control)
   - Download from https://git-scm.com/downloads

3. **Ollama** (if using local LLM)
   - Download from https://ollama.ai/download
   - Models: qwen2.5-coder:7b (or other supported models)

### Python Dependencies

All dependencies are listed in `requirements.txt`:

```
streamlit>=1.28.0              # Web UI
python-dotenv>=1.0.0           # Configuration
pyyaml>=6.0                    # YAML parsing
requests>=2.31.0               # HTTP requests
langchain>=0.1.0               # Agent framework
langchain-community>=0.0.10    # Community tools
chromadb>=0.4.0                # Vector database
sentence-transformers>=2.2.0   # Embeddings
gitpython>=3.1.40              # Git operations
tree-sitter>=0.20.0            # Code parsing
tree-sitter-languages>=1.8.0   # Language parsers
pytest>=7.4.0                  # Testing
rich>=13.0.0                   # Terminal formatting
pygments>=2.16.0               # Syntax highlighting
watchdog>=3.0.0                # File watching
tiktoken>=0.5.0                # Token counting
```

### API Keys (Optional)

Only needed if using cloud LLM providers:

**OpenRouter (Free Tier):**
- Sign up at https://openrouter.ai/
- Get API key from https://openrouter.ai/keys
- Free tier available with rate limits

**Google AI Studio (Free Tier):**
- Sign up at https://aistudio.google.com/
- Get API key from https://aistudio.google.com/app/apikey
- Free tier available with rate limits

**Ollama (Local, Free):**
- No API key required
- Runs locally on your machine
- Requires Ollama installation

---

## Installation Guide

### Step 1: Clone or Download the Project

```bash
# If using Git
git clone <repository-url>
cd Agentic_Automation_Framework

# Or download and extract the ZIP file
# Navigate to the extracted directory
cd Agentic_Automation_Framework
```

### Step 2: Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

Copy the example `.env` file (or create one):

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

Edit `.env` file with your configuration:

```env
# LLM Provider Selection (ollama, openrouter, or google)
LLM_PROVIDER=ollama

# Ollama Configuration (if using Ollama)
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_URL=http://localhost:11434/api/chat

# OpenRouter Configuration (if using OpenRouter)
OPENROUTER_API_KEY=your-openrouter-api-key
OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b:free

# Google AI Studio Configuration (if using Google)
GOOGLE_AI_STUDIO_KEY=your-google-api-key
GOOGLE_MODEL=gemini-pro

# Project Root (your codebase directory)
AI_PROJECT_ROOT=D:/PlayWrightDemoGradle

# RAG Settings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

### Step 5: Install Ollama (If Using Local LLM)

**Windows:**
1. Download Ollama from https://ollama.ai/download
2. Run the installer
3. Open terminal and verify: `ollama --version`

**macOS:**
```bash
brew install ollama
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Download Model:**
```bash
ollama pull qwen2.5-coder:7b
```

**Start Ollama Server:**
```bash
ollama serve
```

### Step 6: Verify Installation

Run the basic test:

```bash
python test_basic.py
```

Expected output:
```
==================================================
JeshlaAIAgent - Basic Functionality Test
==================================================

Testing settings...
  LLM Provider: ollama
  Project Root: D:/PlayWrightDemoGradle
  [OK] Settings loaded successfully

Testing LLM provider...
  Provider: ollama
  Model: qwen2.5-coder:7b
  [OK] LLM provider initialized successfully

Testing agents...
  Available agents: 8
    - CodeGeneratorAgent
    - CodeConverterAgent
    - CodeReviewerAgent
    - FileAgent
    - GitAgent
    - TestAgent
    - DebugAgent
    - RefactorAgent
  [OK] Agents initialized successfully

Testing task planner...
  [OK] Task planner initialized successfully

Testing core tools...
  [OK] File operations initialized
  [OK] Code parser initialized
  [OK] Core tools initialized successfully

==================================================
Test Complete
==================================================
```

---

## IDE Setup

### IntelliJ IDEA / PyCharm Setup

#### 1. Open Project
- File → Open → Select `Agentic_Automation_Framework` folder
- Select "Open as Project"

#### 2. Configure Python Interpreter
- File → Settings → Project → Python Interpreter
- Click "Add Interpreter" → "Add Local Interpreter"
- Select "Virtual Environment"
- Browse to your venv folder
- Select the Python executable

#### 3. Install Dependencies
- Terminal → Run: `pip install -r requirements.txt`

#### 4. Configure Run Configuration
- Run → Edit Configurations
- Click "+" → Python
- Name: "JeshlaAIAgent"
- Script path: `ui/app.py`
- Working directory: Project root
- Environment variables: Click folder icon → Load from `.env`

#### 5. Run the Application
- Click the green "Run" button
- Or press Shift+F10

#### 6. Debugging
- Set breakpoints by clicking line numbers
- Click the "Debug" button (bug icon)
- Or press Shift+F9

### Visual Studio Code Setup

#### 1. Open Project
- File → Open Folder → Select `Agentic_Automation_Framework`

#### 2. Install Python Extension
- Extensions → Search "Python"
- Install "Python" by Microsoft

#### 3. Select Python Interpreter
- Press Ctrl+Shift+P
- Type "Python: Select Interpreter"
- Choose your virtual environment (venv)

#### 4. Install Dependencies
- Terminal → Run: `pip install -r requirements.txt`

#### 5. Configure Launch Settings
- Create `.vscode/launch.json`:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "JeshlaAIAgent",
            "type": "python",
            "request": "launch",
            "program": "ui/app.py",
            "cwd": "${workspaceFolder}",
            "envFile": "${workspaceFolder}/.env",
            "console": "integratedTerminal"
        }
    ]
}
```

#### 6. Run the Application
- Press F5
- Or click "Run and Debug" in sidebar

#### 7. Debugging
- Set breakpoints by clicking line numbers
- Press F5 to start debugging
- Use F10 (step over), F11 (step into), Shift+F11 (step out)

---

## Execution Guide

### Method 1: Command Line

```bash
# Activate virtual environment
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Run the application
streamlit run ui/app.py
```

The application will open at: `http://localhost:8501`

### Method 2: IntelliJ / PyCharm

1. Open the project
2. Configure Python interpreter (see IDE Setup)
3. Right-click `ui/app.py`
4. Select "Run 'app'"
5. Application opens in browser

### Method 3: VS Code

1. Open the project
2. Select Python interpreter (see IDE Setup)
3. Press F5 or click "Run and Debug"
4. Application opens in browser

### Method 4: Create Desktop Shortcut

**Windows:**
Create a batch file `run.bat`:
```batch
@echo off
cd /d "C:\path\to\Agentic_Automation_Framework"
call venv\Scripts\activate
streamlit run ui/app.py
```

**macOS/Linux:**
Create a shell script `run.sh`:
```bash
#!/bin/bash
cd /path/to/Agentic_Automation_Framework
source venv/bin/activate
streamlit run ui/app.py
```

Make it executable:
```bash
chmod +x run.sh
```

---

## Configuration

### LLM Provider Selection

Edit `.env` file:

```env
# Option 1: Ollama (Local, Free)
LLM_PROVIDER=ollama
OLLAMA_MODEL=qwen2.5-coder:7b

# Option 2: OpenRouter (Cloud, Free Tier)
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your-api-key
OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b:free

# Option 3: Google AI Studio (Cloud, Free Tier)
LLM_PROVIDER=google
GOOGLE_AI_STUDIO_KEY=your-api-key
GOOGLE_MODEL=gemini-pro
```

### Project Root Configuration

Set your project directory:

```env
AI_PROJECT_ROOT=/path/to/your/project
```

This is the directory that agents will work with for file operations, git operations, etc.

### RAG Configuration

Adjust chunking parameters for performance:

```env
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500          # Size of code chunks
CHUNK_OVERLAP=50        # Overlap between chunks
```

---

## Troubleshooting

### Issue: "Module not found" Error

**Solution:**
```bash
# Ensure virtual environment is activated
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue: Ollama Connection Failed

**Solution:**
```bash
# Check if Ollama is running
ollama --version

# Start Ollama server
ollama serve

# Verify model is downloaded
ollama list

# Pull model if needed
ollama pull qwen2.5-coder:7b
```

### Issue: API Key Errors

**Solution:**
- Verify API key in `.env` file
- Check if you have sufficient quota on OpenRouter/Google
- Try switching to Ollama (no API key needed)

### Issue: Port 8501 Already in Use

**Solution:**
```bash
# Run on different port
streamlit run ui/app.py --server.port 8502
```

### Issue: Memory Errors with Large Codebases

**Solution:**
- Reduce `CHUNK_SIZE` in `.env`
- Use a smaller embedding model
- Limit the number of files indexed
- Close other applications to free RAM

### Issue: Slow Response Times

**Solution:**
- Use Ollama for faster local inference
- Reduce RAG context size
- Use a smaller model
- Disable RAG if not needed

---

## Development Workflow

### Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_llm.py

# Run with verbose output
pytest tests/ -v

# Run with coverage
pytest tests/ --cov
```

### Adding New Agents

1. Create new agent file in `core/agents/`
2. Inherit from existing agent pattern
3. Implement `execute()` method
4. Register in `agent_orchestrator.py`
5. Add system prompt in `config/prompts.py`

### Adding New LLM Providers

1. Create provider file in `core/llm/`
2. Inherit from `BaseLLMProvider`
3. Implement required methods
4. Add to `get_llm_provider()` in `core/llm/__init__.py`

### Debugging

**With Logging:**
```python
from utils.logger import get_logger

logger = get_logger(__name__)
logger.info("Debug message")
```

**With IDE Debugger:**
- Set breakpoints in code
- Run in debug mode
- Inspect variables in debug panel

### Code Structure Best Practices

- Follow existing code patterns
- Add docstrings to functions
- Use type hints
- Handle errors gracefully
- Add tests for new features

---

## Quick Start Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file configured
- [ ] Ollama installed (if using local LLM)
- [ ] Ollama model downloaded (`ollama pull qwen2.5-coder:7b`)
- [ ] Ollama server running (`ollama serve`)
- [ ] Basic test passed (`python test_basic.py`)
- [ ] Application runs (`streamlit run ui/app.py`)

---

## Support & Resources

### Documentation
- README.md - Project overview
- SETUP_GUIDE.md - This file
- Code comments - Inline documentation

### External Resources
- Streamlit Docs: https://docs.streamlit.io/
- LangChain Docs: https://python.langchain.com/
- ChromaDB Docs: https://docs.trychroma.com/
- Ollama Docs: https://github.com/ollama/ollama

### Community
- Open issues on GitHub repository
- Check existing issues for solutions
- Contribute improvements

---

## Next Steps

1. **Explore the UI**: Navigate through Chat, Plan, and Agents sections
2. **Try Chat**: Ask code-related questions
3. **Create a Plan**: Enter a complex task and generate a plan
4. **Use Agents**: Manually trigger specific agents
5. **Customize**: Modify prompts, add agents, or change LLM providers
6. **Integrate**: Connect to your own codebase via `AI_PROJECT_ROOT`

---

**Happy Coding with JeshlaAIAgent! 🤖**
