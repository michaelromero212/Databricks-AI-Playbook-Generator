import sys
import os
import glob
import yaml
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extractors.sql_extractor import SQLExtractor
from app.extractors.notebook_parser import NotebookParser
from app.extractors.py_analyzer import PyAnalyzer
from app.generators.diagram_generator import DiagramGenerator
from app.generators.playbook_generator import PlaybookGenerator

def test_fintech_large():
    print("Testing Fintech Large Dataset...")
    
    # Initialize components
    sql_extractor = SQLExtractor()
    notebook_parser = NotebookParser()
    py_analyzer = PyAnalyzer()
    diagram_generator = DiagramGenerator()
    playbook_generator = PlaybookGenerator()
    
    base_dir = "data/samples/fintech_large"
    analysis_results = {}
    project_info = {}
    
    # 1. Parse Project Info
    info_path = os.path.join(base_dir, "project_info.yaml")
    if os.path.exists(info_path):
        with open(info_path, 'r') as f:
            project_info = yaml.safe_load(f)
            print(f"Loaded Project Info: {project_info.get('client')}")

    # 2. Process Files
    files = glob.glob(f"{base_dir}/**/*", recursive=True)
    for file_path in files:
        if os.path.isdir(file_path):
            continue
            
        file_name = os.path.basename(file_path)
        print(f"Processing: {file_name}")
        
        if file_name.endswith('.sql'):
            analysis_results[file_name] = sql_extractor.parse_file(file_path)
        elif file_name.endswith('.ipynb'):
            analysis_results[file_name] = notebook_parser.parse_notebook(file_path)
        elif file_name.endswith('.py'):
            # Check if it's a notebook export or script
            with open(file_path, 'r') as f:
                content = f.read()
            if "# COMMAND" in content:
                analysis_results[file_name] = notebook_parser.parse_notebook(file_path)
            else:
                analysis_results[file_name] = py_analyzer.analyze_script(file_path)

    # 3. Generate Diagram
    print("\nGenerating Diagram...")
    mermaid_code = diagram_generator.generate_mermaid(analysis_results)
    print(f"Mermaid Code Length: {len(mermaid_code)}")

    # 4. Generate Playbook
    print("\nGenerating Playbook...")
    playbook_md = playbook_generator.generate_playbook(project_info, analysis_results, mermaid_code)
    
    # Save outputs
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/fintech_large_playbook.md", "w") as f:
        f.write(playbook_md)
        
    with open(f"{output_dir}/fintech_large_diagram.mermaid", "w") as f:
        f.write(mermaid_code)
        
    print(f"\nSuccess! Outputs saved to {output_dir}/")
    print("-" * 30)
    print("Preview of Playbook:")
    print(playbook_md[:500])
    print("...")

if __name__ == "__main__":
    test_fintech_large()
