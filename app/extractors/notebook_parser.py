import nbformat
import re

class NotebookParser:
    def __init__(self):
        pass

    def parse_notebook(self, file_path):
        """
        Parses a Jupyter notebook (.ipynb) or Databricks source file (.py with # COMMAND)
        """
        if file_path.endswith('.ipynb'):
            return self._parse_ipynb(file_path)
        elif file_path.endswith('.py'):
            return self._parse_py_notebook(file_path)
        else:
            return {"error": "Unsupported file format"}

    def _parse_ipynb(self, file_path):
        metadata = {
            "markdown_cells": [],
            "code_cells": [],
            "imports": [],
            "spark_calls": []
        }
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)
                
            for cell in nb.cells:
                if cell.cell_type == 'markdown':
                    metadata["markdown_cells"].append(cell.source)
                elif cell.cell_type == 'code':
                    metadata["code_cells"].append(cell.source)
                    self._analyze_code_cell(cell.source, metadata)
                    
            return metadata
        except Exception as e:
            return {"error": str(e)}

    def _parse_py_notebook(self, file_path):
        """
        Parses a Databricks Python notebook exported as source.
        Separated by '# COMMAND ----------'
        """
        metadata = {
            "markdown_cells": [],
            "code_cells": [],
            "imports": [],
            "spark_calls": []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by Databricks command separator
            cells = content.split('# COMMAND ----------')
            
            for cell in cells:
                cell = cell.strip()
                if not cell:
                    continue
                    
                # Check if it's a magic markdown cell
                if cell.startswith('# MAGIC %md') or cell.startswith('%md'):
                    # Clean up magic syntax
                    clean_md = re.sub(r'^# MAGIC %md', '', cell, flags=re.MULTILINE)
                    clean_md = re.sub(r'^# MAGIC ', '', clean_md, flags=re.MULTILINE)
                    clean_md = re.sub(r'^%md', '', clean_md, flags=re.MULTILINE)
                    metadata["markdown_cells"].append(clean_md.strip())
                else:
                    # Assume code cell
                    metadata["code_cells"].append(cell)
                    self._analyze_code_cell(cell, metadata)
                    
            return metadata
        except Exception as e:
             return {"error": str(e)}

    def _analyze_code_cell(self, code, metadata):
        """
        Simple heuristic analysis of code cells
        """
        # Detect imports
        import_matches = re.findall(r'^(?:from|import)\s+([a-zA-Z0-9_.]+)', code, re.MULTILINE)
        for imp in import_matches:
            if imp not in metadata["imports"]:
                metadata["imports"].append(imp)

        # Detect Spark calls
        if 'spark.read' in code:
            metadata["spark_calls"].append("spark.read")
        if 'spark.sql' in code:
            metadata["spark_calls"].append("spark.sql")
        if 'write' in code and ('save' in code or 'saveAsTable' in code):
             metadata["spark_calls"].append("spark.write")
