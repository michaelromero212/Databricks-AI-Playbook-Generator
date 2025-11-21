import re

class SQLExtractor:
    def __init__(self):
        pass

    def extract_metadata(self, sql_content):
        """
        Parses SQL content to identify tables, transformations, and logic.
        """
        metadata = {
            "tables_detected": [],
            "transformations": [],
            "ctes": [],
            "creates": []
        }

        # Normalize content
        sql_content = sql_content.strip()

        # 1. Detect Tables (FROM/JOIN)
        # Regex to find table names after FROM or JOIN
        # Handles: FROM table, JOIN table, FROM db.table
        table_pattern = re.compile(r'\b(FROM|JOIN)\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
        matches = table_pattern.findall(sql_content)
        for match in matches:
            table_name = match[1]
            if table_name.lower() not in ["select", "where", "group", "order", "limit"]:
                if table_name not in metadata["tables_detected"]:
                    metadata["tables_detected"].append(table_name)

        # 2. Detect Transformations (SELECT statements)
        # Simple heuristic: grab the first few lines of a SELECT statement
        select_pattern = re.compile(r'(SELECT\s+.*?(?:FROM|$))', re.IGNORECASE | re.DOTALL)
        select_matches = select_pattern.findall(sql_content)
        for match in select_matches:
             # Clean up whitespace and truncate for summary
            clean_match = " ".join(match.split()).strip()
            if len(clean_match) > 200:
                clean_match = clean_match[:200] + "..."
            metadata["transformations"].append(clean_match)

        # 3. Detect CREATE statements (Target tables)
        create_pattern = re.compile(r'CREATE\s+(?:OR\s+REPLACE\s+)?(?:TABLE|VIEW)\s+([a-zA-Z0-9_.]+)', re.IGNORECASE)
        create_matches = create_pattern.findall(sql_content)
        for match in create_matches:
             metadata["creates"].append(match)

        return metadata

    def parse_file(self, file_path):
        with open(file_path, 'r') as f:
            content = f.read()
        return self.extract_metadata(content)
