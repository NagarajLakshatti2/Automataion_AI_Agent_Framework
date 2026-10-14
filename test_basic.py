"""
Basic test script to verify JeshlaAIAgent functionality.
"""
from config.settings import settings
from core.llm import get_llm_provider
from core.agents import AgentOrchestrator
from core.planner import TaskPlanner
from core.tools import FileOperations, CodeParser


def test_settings():
    """Test configuration loading."""
    print("Testing settings...")
    print(f"  LLM Provider: {settings.LLM_PROVIDER}")
    print(f"  Project Root: {settings.AI_PROJECT_ROOT}")
    print("  [OK] Settings loaded successfully\n")


def test_llm():
    """Test LLM provider initialization."""
    print("Testing LLM provider...")
    try:
        llm = get_llm_provider()
        print(f"  Provider: {llm.get_provider_name()}")
        print(f"  Model: {llm.get_model_name()}")
        print("  [OK] LLM provider initialized successfully\n")
    except Exception as e:
        print(f"  [ERROR] {str(e)}\n")


def test_agents():
    """Test agent initialization."""
    print("Testing agents...")
    try:
        orchestrator = AgentOrchestrator()
        agents = orchestrator.list_agents()
        print(f"  Available agents: {len(agents)}")
        for agent in agents:
            print(f"    - {agent['name']}")
        print("  [OK] Agents initialized successfully\n")
    except Exception as e:
        print(f"  [ERROR] {str(e)}\n")


def test_planner():
    """Test task planner."""
    print("Testing task planner...")
    try:
        planner = TaskPlanner()
        print("  [OK] Task planner initialized successfully\n")
    except Exception as e:
        print(f"  [ERROR] {str(e)}\n")


def test_tools():
    """Test core tools."""
    print("Testing core tools...")
    try:
        file_ops = FileOperations()
        code_parser = CodeParser()
        print("  [OK] File operations initialized")
        print("  [OK] Code parser initialized")
        print("  [OK] Core tools initialized successfully\n")
    except Exception as e:
        print(f"  [ERROR] {str(e)}\n")


def main():
    """Run all tests."""
    print("=" * 50)
    print("JeshlaAIAgent - Basic Functionality Test")
    print("=" * 50 + "\n")

    test_settings()
    test_llm()
    test_agents()
    test_planner()
    test_tools()

    print("=" * 50)
    print("Test Complete")
    print("=" * 50)


if __name__ == "__main__":
    main()
