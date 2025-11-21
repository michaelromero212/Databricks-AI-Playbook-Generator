import streamlit as st
import os
import sys
import yaml
import json

# Add project root to path so we can import app modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from app.extractors.sql_extractor import SQLExtractor
from app.extractors.notebook_parser import NotebookParser
from app.extractors.py_analyzer import PyAnalyzer
from app.generators.diagram_generator import DiagramGenerator
from app.generators.playbook_generator import PlaybookGenerator
from app.generators.summary_generator import SummaryGenerator
from app.ui.components import set_page_config, header, card

# Initialize components
sql_extractor = SQLExtractor()
notebook_parser = NotebookParser()
py_analyzer = PyAnalyzer()
diagram_generator = DiagramGenerator()
playbook_generator = PlaybookGenerator()
summary_generator = SummaryGenerator()

def main():
    set_page_config()
    header()

    # Sidebar for inputs
    with st.sidebar:
        st.header("Project Inputs")
        
        # File Uploads
        uploaded_files = st.file_uploader(
            "Upload Artifacts (SQL, Python, Notebooks)", 
            accept_multiple_files=True,
            type=['sql', 'py', 'ipynb', 'yaml']
        )
        
        project_info_text = st.text_area(
            "Or Paste Project Info (YAML/Text)", 
            height=200,
            placeholder="client: ACME Corp\nobjective: ..."
        )
        
        generate_btn = st.button("Generate Playbook")
        
        st.markdown("---")
        load_sample_btn = st.button("Load Fintech Sample (Large)")

    # Initialize variables
    analysis_results = {}
    project_info = {}
    run_generation = False

    if load_sample_btn:
        with st.spinner("Loading Fintech Large Sample..."):
            import glob
            base_dir = os.path.join(os.path.dirname(__file__), '../../data/samples/fintech_large')
            
            # Load Project Info
            info_path = os.path.join(base_dir, "project_info.yaml")
            if os.path.exists(info_path):
                with open(info_path, 'r') as f:
                    project_info = yaml.safe_load(f)
            
            # Load Files
            files = glob.glob(f"{base_dir}/**/*", recursive=True)
            for file_path in files:
                if os.path.isdir(file_path):
                    continue
                
                file_name = os.path.basename(file_path)
                
                if file_name.endswith('.sql'):
                    analysis_results[file_name] = sql_extractor.parse_file(file_path)
                elif file_name.endswith('.ipynb'):
                    analysis_results[file_name] = notebook_parser.parse_notebook(file_path)
                elif file_name.endswith('.py'):
                     with open(file_path, 'r') as f:
                        content = f.read()
                     if "# COMMAND" in content:
                         analysis_results[file_name] = notebook_parser.parse_notebook(file_path)
                     else:
                         analysis_results[file_name] = py_analyzer.analyze_script(file_path)
            
            run_generation = True
            st.success("Sample Data Loaded!")

    if generate_btn and (uploaded_files or project_info_text):
        run_generation = True
        # ... (existing processing logic will be moved/adapted below)

    if run_generation:
        with st.spinner("Generating Playbook..."):
            if not analysis_results: # Only process uploads if not already loaded from sample
                # 1. Process Inputs
                # Parse Project Info
                if project_info_text:
                    try:
                        project_info = yaml.safe_load(project_info_text)
                    except:
                        project_info = {"raw_text": project_info_text}
                
                # Process Files
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        file_name = uploaded_file.name
                        content = uploaded_file.read().decode("utf-8")
                        
                        temp_path = f"temp_{file_name}"
                        with open(temp_path, "w") as f:
                            f.write(content)
                            
                        if file_name.endswith('.sql'):
                            analysis_results[file_name] = sql_extractor.parse_file(temp_path)
                        elif file_name.endswith('.ipynb') or file_name.endswith('.py'):
                            if file_name.endswith('.ipynb'):
                                 analysis_results[file_name] = notebook_parser.parse_notebook(temp_path)
                            else:
                                 if "# COMMAND" in content:
                                     analysis_results[file_name] = notebook_parser.parse_notebook(temp_path)
                                 else:
                                     analysis_results[file_name] = py_analyzer.analyze_script(temp_path)
                        elif file_name.endswith('.yaml') or file_name.endswith('.yml'):
                            try:
                                project_info.update(yaml.safe_load(content))
                            except:
                                pass
                        
                        os.remove(temp_path)

            # 2. Generate Diagram
            mermaid_code = diagram_generator.generate_mermaid(analysis_results)
            
            # 3. Generate Playbook
            playbook_md = playbook_generator.generate_playbook(project_info, analysis_results, mermaid_code)
            
            # 4. Generate Summary
            summary_text = summary_generator.generate_console_summary(analysis_results)
            
            # --- Display Results ---
            
            # Tabs
            tab1, tab2, tab3 = st.tabs(["Playbook", "Architecture", "Analysis Data"])
            
            with tab1:
                st.markdown(playbook_md)
                st.download_button(
                    label="Download Playbook (.md)",
                    data=playbook_md,
                    file_name="playbook.md",
                    mime="text/markdown"
                )
                
            with tab2:
                st.markdown(f"```mermaid\n{mermaid_code}\n```")
                st.info("Copy the Mermaid code above into a Mermaid live editor or Markdown viewer to see the diagram.")
                
            with tab3:
                st.text(summary_text)
                st.json(analysis_results)
                st.download_button(
                    label="Download Analysis (.json)",
                    data=json.dumps(analysis_results, indent=2),
                    file_name="sql_analysis.json",
                    mime="application/json"
                )

    elif generate_btn and not run_generation:
         st.warning("Please upload files or provide project info.")

if __name__ == "__main__":
    main()
