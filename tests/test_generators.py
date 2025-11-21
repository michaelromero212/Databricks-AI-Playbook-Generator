import pytest
from app.generators.diagram_generator import DiagramGenerator
from app.generators.playbook_generator import PlaybookGenerator

def test_diagram_generator():
    generator = DiagramGenerator()
    analysis_results = {
        "file1.sql": {
            "tables_detected": ["bronze_table"],
            "creates": ["silver_table"]
        },
        "file2.py": {
            "tables_detected": ["silver_table"],
            "creates": ["gold_table"]
        }
    }
    
    mermaid = generator.generate_mermaid(analysis_results)
    
    assert "flowchart TD" in mermaid
    assert "bronze_table" in mermaid
    assert "silver_table" in mermaid
    assert "gold_table" in mermaid
    assert "-->" in mermaid

def test_playbook_generator_mock():
    # Test without API key (mock mode)
    generator = PlaybookGenerator()
    # Force client to None to ensure mock usage even if env var is set
    generator.client = None
    
    project_info = {"client": "TestCorp"}
    analysis_results = {}
    diagram = "graph TD; A-->B;"
    
    playbook = generator.generate_playbook(project_info, analysis_results, diagram)
    
    assert "TestCorp" in playbook
    assert "Mock" in playbook or "mock" in playbook
