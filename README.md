# JeshlaAIAgent

An advanced agentic AI code assistant modeled after Devin, ChatGPT, and Claude. Built with free, open-source modules including Streamlit, LangChain, ChromaDB, and Ollama.

## Features

### Three Main Sections

#### 1. Chat Section
- Natural language conversation interface
- Direct code generation, conversion, and review
- Context-aware responses using RAG (Retrieval-Augmented Generation)
- Streaming responses for real-time feedback
- Message history with search and filtering
- Multi-turn conversations with context
- Code syntax highlighting

#### 2. Plan Section
- Automatic task decomposition using AI
- Visual plan display with progress tracking
- Step-by-step execution with live updates
- Plan approval workflow
- Plan editing and reordering
- Dependency management between tasks
- Plan history and versioning
- Execution logs and terminal output

#### 3. Agent Section
- Dashboard showing all specialized agents
- Real-time agent status monitoring
- Agent activity feed
- Manual agent triggering
- Agent configuration and capabilities
- Agent performance metrics
- Agent orchestration and coordination

## Specialized Agents

- **Code Generator**: Generate code from natural language in multiple languages
- **Code Converter**: Convert code between programming languages
- **Code Reviewer**: Analyze code for bugs, security issues, and best practices
- **File Agent**: Read, write, and manage files
- **Git Agent**: Perform git operations (status, commit, branch, etc.)
- **Test Agent**: Generate and run tests
- **Debug Agent**: Analyze errors and provide debugging strategies
- **Refactor Agent**: Identify and apply code refactoring improvements

## Supported LLM Providers

- **Ollama** (Free, Local): Use local models like qwen2.5-coder:7b
- **OpenRouter** (Free Tier): Access to various models including nvidia/nemotron-3-super-120b-a12b:free
- **Google AI Studio** (Free Tier): Access to Gemini models

## Supported Programming Languages

Python, Java, JavaScript, TypeScript, C++, C, Go, Rust, Ruby, PHP, Swift, Kotlin, Scala, C#, and more.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd Agentic_Automation_Framework
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys and configuration
```

4. (Optional) Install Ollama for local LLM:
```bash
# Visit https://ollama.ai for installation instructions
ollama pull qwen2.5-coder:7b
```

## Configuration

Edit the `.env` file to configure:

```env
# LLM Provider Selection (ollama, openrouter, or google)
LLM_PROVIDER=ollama

# Ollama Configuration
OLLAMA_MODEL=qwen2.5-coder:7b
OLLAMA_URL=http://localhost:11434/api/chat

# OpenRouter Configuration
OPENROUTER_API_KEY=your-api-key
OPENROUTER_MODEL=nvidia/nemotron-3-super-120b-a12b:free

# Google AI Studio Configuration
GOOGLE_AI_STUDIO_KEY=your-api-key
GOOGLE_MODEL=gemini-pro

# Project Root
AI_PROJECT_ROOT=/path/to/your/project

# RAG Settings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

## Usage

### Start the Application

```bash
streamlit run ui/app.py
```

The application will open in your browser at `http://localhost:8501`

### Using the Chat Section

1. Navigate to the "Chat" tab
2. Type your question or request in the chat input
3. View the AI response with code syntax highlighting
4. Continue the conversation by asking follow-up questions

### Using the Plan Section

1. Navigate to the "Plan" tab
2. Enter your goal or task description
3. Click "Generate Plan" to create a step-by-step plan
4. Review the plan and click "Execute Plan" to run it
5. Monitor progress in real-time

### Using the Agents Section

1. Navigate to the "Agents" tab
2. View all available agents and their capabilities
3. Select an agent and provide a task description
4. Click "Execute" to run the agent
5. View the results

## Project Structure

```
JeshlaAIAgent/
├── config/              # Configuration and prompts
├── core/
│   ├── llm/            # LLM provider implementations
│   ├── planner/        # Task planning and execution
│   ├── agents/         # Specialized agents
│   └── tools/          # Core tools (file ops, git, etc.)
├── rag/                # RAG implementation (ChromaDB)
├── ui/                 # Streamlit UI
│   ├── pages/         # Page implementations
│   └── components/    # UI components
├── utils/              # Utility functions
└── tests/              # Test files
```

## Architecture

### LLM Layer
- Abstract base interface for all providers
- Implementations for Ollama, OpenRouter, and Google AI Studio
- Support for streaming responses
- Function calling support

### Planning System
- Task decomposition using AI
- Dependency management
- Plan execution engine
- Plan tracking and history

### Agent Layer
- Agent orchestrator for coordination
- 8 specialized agents for different tasks
- Agent communication and handoff
- State management

### RAG Layer
- Codebase indexing with tree-sitter
- Vector storage with ChromaDB
- Semantic search with sentence-transformers
- Context retrieval for LLM

### Tools Layer
- File operations (read, write, list)
- Git operations (status, commit, branch)
- Test execution (pytest, unittest)
- Code parsing (multi-language)
- Debugging tools
- Code search

## Development

### Running Tests

```bash
pytest tests/
```

### Adding New Agents

1. Create a new agent class in `core/agents/`
2. Inherit from a base pattern (similar to existing agents)
3. Implement the `execute` method
4. Register the agent in `agent_orchestrator.py`

### Adding New LLM Providers

1. Create a new provider class in `core/llm/`
2. Inherit from `BaseLLMProvider`
3. Implement required methods (generate, chat, stream)
4. Add provider initialization in `get_llm_provider()`

## Free Modules Used

- **Streamlit** - Web UI framework
- **LangChain** - Agent framework
- **ChromaDB** - Vector database
- **Sentence-Transformers** - Embeddings
- **Ollama** - Local LLM
- **OpenRouter** - Cloud LLM (free tier)
- **Google AI Studio** - Cloud LLM (free tier)
- **GitPython** - Git operations
- **Tree-sitter** - Code parsing
- **Pytest** - Testing
- **Rich** - Terminal formatting
- **PyYAML** - Configuration

## Troubleshooting

### Ollama Connection Issues
- Ensure Ollama is running: `ollama serve`
- Check the URL in `.env` matches your Ollama setup
- Verify the model is downloaded: `ollama list`

### API Key Issues
- Verify your API keys are correct in `.env`
- Check your API rate limits for OpenRouter and Google AI Studio

### RAG Indexing Slow
- Indexing large codebases can take time
- Consider incremental indexing for large projects
- Adjust `CHUNK_SIZE` in `.env` for performance

### Memory Issues
- Large codebases may require more RAM for embeddings
- Consider using a smaller embedding model
- Limit the number of files indexed

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Inspired by Devin, ChatGPT, and Claude
- Built with amazing open-source tools
- Powered by free LLM providers

## Support

For issues and questions, please open an issue on the repository.
"# Automataion_AI_Agent_Framework" 
