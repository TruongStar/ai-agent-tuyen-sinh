from pathlib import Path

def test_project_structure():
    assert Path("main.py").exists()
    assert Path("app/core/agent_controller.py").exists()
    assert Path("app/tools/knowledge_base.py").exists()
