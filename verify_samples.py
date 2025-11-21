import sys
import os
import glob

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.extractors.sql_extractor import SQLExtractor
from app.extractors.notebook_parser import NotebookParser

def verify_samples():
    print("Verifying Sample Data...")
    
    sql_extractor = SQLExtractor()
    nb_parser = NotebookParser()
    
    base_dir = "data/samples"
    datasets = ["retail_small", "fintech_large"]
    
    for dataset in datasets:
        print(f"\n--- Checking Dataset: {dataset} ---")
        path = os.path.join(base_dir, dataset)
        
        # Find all relevant files recursively
        files = glob.glob(f"{path}/**/*", recursive=True)
        
        for file_path in files:
            if os.path.isdir(file_path):
                continue
                
            if file_path.endswith(".sql"):
                print(f"Parsing SQL: {os.path.basename(file_path)}")
                meta = sql_extractor.parse_file(file_path)
                print(f"  Tables: {meta.get('tables_detected', [])}")
                print(f"  Creates: {meta.get('creates', [])}")
                
            elif file_path.endswith(".ipynb") or file_path.endswith(".py"):
                print(f"Parsing Notebook/Script: {os.path.basename(file_path)}")
                # Simple check for py files to see if they are scripts or notebooks
                if file_path.endswith(".py") and "inventory_check.py" in file_path:
                     # Treat as script/notebook
                     pass
                
                meta = nb_parser.parse_notebook(file_path)
                print(f"  Imports: {meta.get('imports', [])}")
                print(f"  Spark Calls: {meta.get('spark_calls', [])}")

if __name__ == "__main__":
    verify_samples()
