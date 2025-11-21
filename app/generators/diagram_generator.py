class DiagramGenerator:
    def __init__(self):
        pass

    def generate_mermaid(self, analysis_results):
        """
        Generates a Mermaid flowchart based on analysis results.
        """
        diagram_lines = ["flowchart TD"]
        
        # Add nodes and edges based on detected tables and transformations
        # This is a simplified logic. In a real app, we'd connect inputs to outputs.
        
        tables = set()
        for file_name, metadata in analysis_results.items():
            if "tables_detected" in metadata:
                for table in metadata["tables_detected"]:
                    tables.add(table)
            if "creates" in metadata:
                for table in metadata["creates"]:
                    tables.add(table)

        # Create a simple flow: Source -> Process -> Target
        # Since we don't have full lineage, we'll just list detected tables
        # and connect them sequentially for the demo or try to infer relationships.
        
        # Heuristic: If we have "raw" tables and "silver" tables, connect them.
        bronze_tables = [t for t in tables if "raw" in t.lower() or "bronze" in t.lower()]
        silver_tables = [t for t in tables if "silver" in t.lower() or "clean" in t.lower()]
        gold_tables = [t for t in tables if "gold" in t.lower() or "agg" in t.lower()]
        
        # Add nodes
        for t in bronze_tables:
            diagram_lines.append(f'    {self._clean_id(t)}["{t} (Bronze)"]')
        for t in silver_tables:
            diagram_lines.append(f'    {self._clean_id(t)}["{t} (Silver)"]')
        for t in gold_tables:
            diagram_lines.append(f'    {self._clean_id(t)}["{t} (Gold)"]')
            
        # Add edges (Naive)
        if bronze_tables and silver_tables:
            for b in bronze_tables:
                for s in silver_tables:
                    diagram_lines.append(f'    {self._clean_id(b)} --> {self._clean_id(s)}')
                    
        if silver_tables and gold_tables:
            for s in silver_tables:
                for g in gold_tables:
                    diagram_lines.append(f'    {self._clean_id(s)} --> {self._clean_id(g)}')

        # If no clear lineage, just list them
        if len(diagram_lines) == 1:
             for i, table in enumerate(tables):
                 diagram_lines.append(f'    node{i}["{table}"]')

        return "\n".join(diagram_lines)

    def _clean_id(self, text):
        """Removes special characters for Mermaid IDs"""
        return "".join(c for c in text if c.isalnum())
