import re

class PyAnalyzer:
    def __init__(self):
        pass

    def analyze_script(self, file_path):
        """
        Analyzes a standard Python script (.py) for ETL logic.
        """
        metadata = {
            "functions": [],
            "classes": [],
            "imports": [],
            "spark_calls": [],
            "docstrings": []
        }

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Detect Functions
            func_pattern = re.compile(r'def\s+([a-zA-Z0-9_]+)\s*\(', re.MULTILINE)
            metadata["functions"] = func_pattern.findall(content)

            # Detect Classes
            class_pattern = re.compile(r'class\s+([a-zA-Z0-9_]+)', re.MULTILINE)
            metadata["classes"] = class_pattern.findall(content)

            # Detect Imports
            import_pattern = re.compile(r'^(?:from|import)\s+([a-zA-Z0-9_.]+)', re.MULTILINE)
            metadata["imports"] = list(set(import_pattern.findall(content)))

            # Detect Spark Logic
            if 'spark.read' in content:
                metadata["spark_calls"].append("spark.read")
            if 'spark.sql' in content:
                metadata["spark_calls"].append("spark.sql")
            if 'write' in content:
                metadata["spark_calls"].append("spark.write")

            # Extract Docstrings (naive approach)
            docstring_pattern = re.compile(r'"""(.*?)"""', re.DOTALL)
            metadata["docstrings"] = [d.strip() for d in docstring_pattern.findall(content)]

            return metadata

        except Exception as e:
            return {"error": str(e)}
