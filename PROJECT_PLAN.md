# JeshlaAIAgent - Advanced Agentic AI Code Assistant

Build an advanced agentic AI code assistant modeled after Devin with three main sections: Chat (conversational interface), Plan (task planning and breakdown), and Agent (specialized agent management), using only free modules (Streamlit, LangChain, ChromaDB, Ollama, etc.).

## Summary
Build "JeshlaAIAgent" - an advanced agentic AI code assistant modeled after Devin with three main sections: **Chat** (conversational interface for natural language interactions), **Plan** (task planning, breakdown, and execution tracking), and **Agent** (specialized agent management and coordination). All built using free, open-source modules (Streamlit, LangChain, ChromaDB, Ollama, OpenRouter free tier, etc.).

## Project Structure
```
JeshlaAIAgent/
├── .env                          # API keys and configuration
├── requirements.txt              # Python dependencies (all free modules)
├── README.md                     # Project documentation
├── config/
│   ├── __init__.py
│   ├── settings.py              # Configuration management
│   └── prompts.py               # System prompts for different tasks
├── core/
│   ├── __init__.py
│   ├── llm/
│   │   ├── __init__.py
│   │   ├── base.py              # Base LLM interface
│   │   ├── ollama_provider.py   # Ollama (free, local)
│   │   ├── openrouter_provider.py  # OpenRouter (free tier)
│   │   └── google_provider.py   # Google AI Studio (free tier)
│   ├── planner/
│   │   ├── __init__.py
│   │   ├── task_planner.py      # Task decomposition and planning
│   │   ├── plan_executor.py     # Plan execution engine
│   │   └── plan_tracker.py      # Track plan progress
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── agent_orchestrator.py  # Agent coordination
│   │   ├── code_generator.py    # Code generation agent
│   │   ├── code_converter.py    # Code conversion agent
│   │   ├── code_reviewer.py     # Code review agent
│   │   ├── file_agent.py        # File operations agent
│   │   ├── git_agent.py         # Git operations agent
│   │   ├── test_agent.py        # Testing agent
│   │   ├── debug_agent.py       # Debugging agent
│   │   └── refactor_agent.py    # Code refactoring agent
│   └── tools/
│       ├── __init__.py
│       ├── file_ops.py          # File reading/writing tools
│       ├── git_ops.py           # Git operations tools
│       ├── test_runner.py       # Test execution tools
│       ├── code_parser.py       # Code parsing utilities
│       ├── debugger.py          # Debugging tools
│       └── search.py            # Code search tools
├── rag/
│   ├── __init__.py
│   ├── indexer.py               # Codebase indexing
│   ├── vector_store.py          # Vector database (ChromaDB - free)
│   └── retriever.py             # Context retrieval
├── ui/
│   ├── __init__.py
│   ├── app.py                   # Main Streamlit application
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── chat.py              # Chat page
│   │   ├── plan.py              # Plan page
│   │   └── agents.py            # Agents page
│   ├── components/
│   │   ├── __init__.py
│   │   ├── chat_interface.py    # Chat UI component
│   │   ├── plan_viewer.py       # Plan display and management
│   │   ├── agent_status.py      # Agent status dashboard
│   │   ├── code_editor.py       # Code display/editing
│   │   ├── file_browser.py      # File tree component
│   │   ├── terminal.py          # Terminal output display
│   │   └── settings_panel.py    # LLM provider settings
│   └── styles/
│       └── custom.css           # Custom styling
├── utils/
│   ├── __init__.py
│   ├── logger.py                # Logging configuration
│   └── helpers.py               # Utility functions
└── tests/
    ├── __init__.py
    ├── test_llm.py
    ├── test_agents.py
    └── test_rag.py
```

## Architecture Overview

### Three Main Sections (Devin-like)

#### 1. Chat Section
- Natural language conversation interface
- Direct agent execution from chat
- Code syntax highlighting in responses
- Streaming responses for real-time feedback
- Message history with search
- Context-aware responses using RAG

#### 2. Plan Section
- Task decomposition and planning
- Visual plan display with progress tracking
- Plan editing and approval workflow
- Step-by-step execution with status updates
- Plan history and versioning
- Dependency management between tasks

#### 3. Agent Section
- Agent dashboard showing all available agents
- Agent status and activity monitoring
- Agent configuration and capabilities
- Agent orchestration and coordination
- Agent performance metrics
- Manual agent triggering

## Implementation Steps

### Phase 1: Project Setup & Configuration
1. **Initialize project structure**
   - Create directory structure as above
   - Set up `.env` file with provided API keys
   - Create `requirements.txt` with FREE dependencies:
     - streamlit (UI)
     - python-dotenv (config)
     - requests (HTTP)
     - langchain (agent framework - free)
     - langchain-community (free community tools)
     - chromadb (vector database - free)
     - sentence-transformers (embeddings - free)
     - gitpython (git operations - free)
     - pytest (testing - free)
     - tree-sitter (code parsing - free)
     - tree-sitter-languages (language parsers - free)
     - rich (terminal formatting - free)
     - pyyaml (config - free)

2. **Configuration management**
   - Create `config/settings.py` to load environment variables
   - Implement LLM provider switching logic
   - Create `config/prompts.py` with system prompts for different tasks
   - Add project root configuration for AI_PROJECT_ROOT

### Phase 2: LLM Provider Layer (All Free)
3. **Base LLM interface** (`core/llm/base.py`)
   - Define abstract base class with methods: `generate()`, `chat()`, `stream()`
   - Standardize message format across providers
   - Support function calling for agent tool use

4. **Ollama provider** (`core/llm/ollama_provider.py`)
   - Implement HTTP client for Ollama API (free, local)
   - Support streaming responses
   - Handle model selection (qwen2.5-coder:7b default)
   - Support function calling

5. **OpenRouter provider** (`core/llm/openrouter_provider.py`)
   - Implement HTTP client for OpenRouter API (free tier)
   - Support model selection (nvidia/nemotron-3-super-120b-a12b:free default)
   - Handle API authentication
   - Support function calling

6. **Google AI Studio provider** (`core/llm/google_provider.py`)
   - Implement HTTP client for Google AI Studio API (free tier)
   - Support Gemini models
   - Handle API authentication with provided key
   - Support function calling

### Phase 3: Planning System (Devin-like)
7. **Task planner** (`core/planner/task_planner.py`)
   - Decompose user requests into actionable tasks
   - Identify dependencies between tasks
   - Estimate task complexity
   - Generate step-by-step plan
   - Use LLM for intelligent planning

8. **Plan executor** (`core/planner/plan_executor.py`)
   - Execute plan steps sequentially
   - Handle task dependencies
   - Retry failed tasks with alternative approaches
   - Provide real-time progress updates
   - Support plan pausing and resuming

9. **Plan tracker** (`core/planner/plan_tracker.py`)
   - Track plan execution status
   - Store plan history
   - Generate execution reports
   - Support plan versioning
   - Provide plan statistics

### Phase 4: Core Tools (All Free)
10. **File operations tools** (`core/tools/file_ops.py`)
    - Implement file reading, writing, listing
    - Support directory traversal
    - Handle file encoding detection
    - Safe operations with backup/undo

11. **Git operations tools** (`core/tools/git_ops.py`)
    - Use gitpython library (free)
    - Implement: status, diff, commit, branch operations, history
    - Handle git repository detection
    - Generate intelligent commit messages

12. **Test runner tools** (`core/tools/test_runner.py`)
    - Implement test discovery and execution
    - Support pytest, unittest frameworks (free)
    - Parse and display test results
    - Generate test reports

13. **Code parser utilities** (`core/tools/code_parser.py`)
    - Use tree-sitter (free) for language-agnostic parsing
    - Extract functions, classes, imports
    - Support multiple languages (Python, Java, JS, TS, C++, Go, Rust, etc.)
    - Build AST for code analysis

14. **Debugging tools** (`core/tools/debugger.py`)
    - Implement breakpoint setting
    - Step-through debugging
    - Variable inspection
    - Error analysis and suggestions

15. **Search tools** (`core/tools/search.py`)
    - Advanced code search (semantic and keyword)
    - Regular expression search
    - Cross-file reference finding
    - Symbol search

### Phase 5: Agent Layer (Devin-like Agents)
16. **Agent orchestrator** (`core/agents/agent_orchestrator.py`)
    - Coordinate multiple agents
    - Route tasks to appropriate agents
    - Handle agent communication
    - Manage agent state
    - Implement agent handoff

17. **Code generation agent** (`core/agents/code_generator.py`)
    - Generate code from natural language
    - Multi-language support (Python, Java, JS, TS, C++, Go, Rust, etc.)
    - Context-aware generation using RAG
    - Support for different coding styles

18. **Code conversion agent** (`core/agents/code_converter.py`)
    - Convert code between languages
    - Preserve logic and structure
    - Handle language-specific idioms
    - Validate converted code

19. **Code review agent** (`core/agents/code_reviewer.py`)
    - Analyze code for bugs, security issues
    - Suggest improvements
    - Check best practices
    - Generate review reports

20. **File operations agent** (`core/agents/file_agent.py`)
    - Read, edit, create files
    - Intelligent file path suggestions
    - Safe operations with confirmation
    - Bulk operations support

21. **Git operations agent** (`core/agents/git_agent.py`)
    - Perform git operations
    - Generate commit messages
    - Analyze changes
    - Suggest git workflows

22. **Testing agent** (`core/agents/test_agent.py`)
    - Generate test cases from code
    - Run tests and analyze results
    - Suggest fixes for failing tests
    - Test coverage analysis

23. **Debugging agent** (`core/agents/debug_agent.py`)
    - Analyze errors and stack traces
    - Suggest fixes
    - Identify root causes
    - Generate debugging strategies

24. **Refactoring agent** (`core/agents/refactor_agent.py`)
    - Identify refactoring opportunities
    - Apply automated refactoring
    - Improve code quality
    - Maintain functionality

### Phase 6: RAG/Vector Search Layer (Free ChromaDB)
25. **Codebase indexer** (`rag/indexer.py`)
    - Walk project directory
    - Parse code files using tree-sitter
    - Extract and chunk code snippets
    - Generate embeddings using sentence-transformers (free)
    - Handle incremental indexing

26. **Vector store** (`rag/vector_store.py`)
    - Use ChromaDB (free, open-source) for vector storage
    - Implement indexing and search
    - Handle metadata (file path, language, function name)
    - Support persistent storage

27. **Context retriever** (`rag/retriever.py`)
    - Retrieve relevant code snippets based on query
    - Rank by relevance
    - Format context for LLM
    - Hybrid search (semantic + keyword)

### Phase 7: UI Layer - Chat Section (Streamlit - Free)
28. **Main application** (`ui/app.py`)
    - Streamlit app entry point
    - Multi-page navigation (Chat, Plan, Agents)
    - Session state management
    - Sidebar for settings

29. **Chat page** (`ui/pages/chat.py`)
    - Chat interface page
    - Message display with syntax highlighting
    - Input field with multi-line support
    - Agent selection in chat
    - Quick actions toolbar

30. **Chat interface component** (`ui/components/chat_interface.py`)
    - Chat UI with message history
    - Code syntax highlighting
    - Streaming response display
    - Markdown rendering
    - Copy code buttons
    - Message actions (edit, regenerate, copy)

### Phase 8: UI Layer - Plan Section (Devin-like)
31. **Plan page** (`ui/pages/plan.py`)
    - Plan management page
    - Create new plans
    - View plan history
    - Execute plans
    - Plan editing interface

32. **Plan viewer component** (`ui/components/plan_viewer.py`)
    - Display plan steps with status
    - Progress indicators
    - Step details and logs
    - Plan approval workflow
    - Plan editing capabilities

33. **Terminal component** (`ui/components/terminal.py`)
    - Display execution logs
    - Show command outputs
    - Error highlighting
    - Expandable/collapsible sections
    - Log filtering

### Phase 9: UI Layer - Agent Section (Devin-like)
34. **Agents page** (`ui/pages/agents.py`)
    - Agent dashboard
    - Agent status overview
    - Agent configuration
    - Agent performance metrics

35. **Agent status component** (`ui/components/agent_status.py`)
    - Display all agents with status
    - Agent activity feed
    - Agent capabilities
    - Manual agent triggering
    - Agent health checks

### Phase 10: Shared UI Components
36. **Code editor component** (`ui/components/code_editor.py`)
    - Display code with syntax highlighting
    - Edit code inline
    - Copy/download functionality
    - Line numbers
    - Minimap

37. **File browser component** (`ui/components/file_browser.py`)
    - Display project file tree
    - Select files for analysis
    - Show file contents
    - File search
    - Breadcrumb navigation

38. **Settings panel component** (`ui/components/settings_panel.py`)
    - LLM provider selection
    - Model selection
    - API key management
    - Project root configuration
    - Theme settings

39. **Custom styling** (`ui/styles/custom.css`)
    - Modern, clean interface
    - Dark/light theme support
    - Responsive design
    - Devin-like aesthetics

### Phase 11: Integration & Testing
40. **Utility functions** (`utils/`)
    - Logging setup with rich formatting
    - Helper functions for common tasks
    - Error handling utilities

41. **Integration**
    - Connect all components
    - Test end-to-end workflows
    - Error handling and user feedback
    - Performance optimization

42. **Testing**
    - Unit tests for LLM providers
    - Unit tests for agents
    - Unit tests for RAG components
    - Integration tests
    - E2E tests for workflows

## Files to Create
- `requirements.txt` - Python dependencies (all free)
- `.env` - Environment configuration
- `config/settings.py` - Configuration management
- `config/prompts.py` - System prompts
- `core/llm/base.py` - Base LLM interface
- `core/llm/ollama_provider.py` - Ollama implementation (free)
- `core/llm/openrouter_provider.py` - OpenRouter implementation (free tier)
- `core/llm/google_provider.py` - Google AI Studio implementation (free tier)
- `core/planner/task_planner.py` - Task decomposition
- `core/planner/plan_executor.py` - Plan execution
- `core/planner/plan_tracker.py` - Plan tracking
- `core/agents/agent_orchestrator.py` - Agent coordination
- `core/agents/code_generator.py` - Code generation agent
- `core/agents/code_converter.py` - Code conversion agent
- `core/agents/code_reviewer.py` - Code review agent
- `core/agents/file_agent.py` - File operations agent
- `core/agents/git_agent.py` - Git operations agent
- `core/agents/test_agent.py` - Testing agent
- `core/agents/debug_agent.py` - Debugging agent
- `core/agents/refactor_agent.py` - Refactoring agent
- `core/tools/file_ops.py` - File operations tools
- `core/tools/git_ops.py` - Git operations tools
- `core/tools/test_runner.py` - Test execution tools
- `core/tools/code_parser.py` - Code parsing utilities
- `core/tools/debugger.py` - Debugging tools
- `core/tools/search.py` - Search tools
- `rag/indexer.py` - Codebase indexing
- `rag/vector_store.py` - Vector database (ChromaDB - free)
- `rag/retriever.py` - Context retrieval
- `ui/app.py` - Main Streamlit app
- `ui/pages/chat.py` - Chat page
- `ui/pages/plan.py` - Plan page
- `ui/pages/agents.py` - Agents page
- `ui/components/chat_interface.py` - Chat UI
- `ui/components/plan_viewer.py` - Plan display
- `ui/components/agent_status.py` - Agent dashboard
- `ui/components/code_editor.py` - Code display
- `ui/components/file_browser.py` - File tree
- `ui/components/terminal.py` - Terminal output
- `ui/components/settings_panel.py` - Settings UI
- `ui/styles/custom.css` - Custom styling
- `utils/logger.py` - Logging configuration
- `utils/helpers.py` - Utility functions
- `tests/` - Test files
- `README.md` - Documentation

## Verification
- [x] Install dependencies: `pip install -r requirements.txt`
- [x] Run Streamlit app: `streamlit run ui/app.py`
- [x] Test Chat section:
  - [x] Send natural language queries
  - [x] Test code generation for multiple languages
  - [x] Test code conversion between languages
  - [x] Test code review functionality
  - [x] Verify streaming responses
  - [x] Test message history
- [x] Test Plan section:
  - [x] Create a plan from user request
  - [x] Approve and execute plan
  - [x] Track plan progress
  - [x] Edit plan steps
  - [x] View plan history
- [x] Test Agent section:
  - [x] View all available agents
  - [x] Check agent status
  - [x] Manually trigger agents
  - [x] View agent activity feed
  - [x] Configure agent settings
- [x] Test LLM provider switching (Ollama, OpenRouter, Google)
- [x] Test file operations (read, write, list)
- [x] Test git operations (status, diff, commit)
- [x] Test test generation and execution
- [x] Test debugging agent
- [x] Test refactoring agent
- [x] Test RAG - index a codebase and query it
- [x] Verify responsive UI and dark/light themes
- [x] Run unit tests: `pytest tests/`
- [x] End-to-end workflow test

## Key Features (Devin-like)

### Chat Section
- Natural language interface for all tasks
- Direct code generation, conversion, review
- Context-aware responses using RAG
- Streaming responses for real-time feedback
- Message history with search and filtering
- Multi-turn conversations with context
- Code syntax highlighting and copy buttons
- Agent selection from chat

### Plan Section
- Automatic task decomposition
- Visual plan display with progress tracking
- Step-by-step execution with live updates
- Plan approval workflow
- Plan editing and reordering
- Dependency management
- Plan history and versioning
- Execution logs and terminal output
- Plan statistics and analytics

### Agent Section
- Dashboard showing all specialized agents
- Real-time agent status monitoring
- Agent activity feed
- Manual agent triggering
- Agent configuration and capabilities
- Agent performance metrics
- Agent orchestration and coordination
- Agent health checks

## All Free Modules Used
- **Streamlit** - Web UI framework (free, open-source)
- **LangChain** - Agent framework (free, open-source)
- **ChromaDB** - Vector database (free, open-source)
- **Sentence-Transformers** - Embeddings (free, open-source)
- **Ollama** - Local LLM (free, open-source)
- **OpenRouter** - Cloud LLM (free tier available)
- **Google AI Studio** - Cloud LLM (free tier available)
- **GitPython** - Git operations (free, open-source)
- **Tree-sitter** - Code parsing (free, open-source)
- **Pytest** - Testing (free, open-source)
- **Rich** - Terminal formatting (free, open-source)
- **PyYAML** - Configuration (free, open-source)

## Risks/Considerations
- **Local LLM requirement**: Ollama requires local installation and sufficient system resources (RAM/GPU)
- **API rate limits**: OpenRouter and Google AI Studio free tiers have rate limits
- **Context window**: Need to manage context size for large codebases - implement chunking
- **Security**: File operations need safeguards to prevent accidental deletion - implement confirmation dialogs
- **Performance**: RAG indexing can be slow for large codebases - implement incremental indexing
- **Code parsing**: Tree-sitter may not support all languages - fallback to regex for unsupported languages
- **State management**: Streamlit session state needs careful handling for complex workflows
- **Error handling**: Need robust error handling for API failures and network issues
- **Plan complexity**: Complex tasks may generate very large plans - implement plan summarization
- **Agent coordination**: Multiple agents working together may have conflicts - implement conflict resolution
