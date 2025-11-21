class SummaryGenerator:
    def __init__(self):
        pass

    def generate_console_summary(self, analysis_results):
        """
        Generates a text summary for the console.
        """
        lines = ["--- ANALYSIS SUMMARY ---"]
        
        total_files = len(analysis_results)
        lines.append(f"Files Analyzed: {total_files}")
        
        for file_name, metadata in analysis_results.items():
            lines.append(f"\nFile: {file_name}")
            if "tables_detected" in metadata:
                lines.append(f"  Tables: {', '.join(metadata['tables_detected'])}")
            if "spark_calls" in metadata:
                lines.append(f"  Spark Calls: {', '.join(metadata['spark_calls'])}")
            if "error" in metadata:
                lines.append(f"  Error: {metadata['error']}")
                
        return "\n".join(lines)
