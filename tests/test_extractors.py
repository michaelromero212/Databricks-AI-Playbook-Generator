import pytest
from app.extractors.sql_extractor import SQLExtractor
from app.extractors.notebook_parser import NotebookParser

def test_sql_extractor_tables(sample_sql_content):
    extractor = SQLExtractor()
    metadata = extractor.extract_metadata(sample_sql_content)
    
    assert "bronze_users" in metadata["tables_detected"]
    assert "bronze_orders" in metadata["tables_detected"]
    assert "silver_users" in metadata["creates"]

def test_sql_extractor_transformations(sample_sql_content):
    extractor = SQLExtractor()
    metadata = extractor.extract_metadata(sample_sql_content)
    
    assert len(metadata["transformations"]) > 0
    assert "SELECT" in metadata["transformations"][0]

def test_notebook_parser_py(tmp_path, sample_notebook_content):
    parser = NotebookParser()
    
    # Create a temporary file
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test_notebook.py"
    p.write_text(sample_notebook_content)
    
    metadata = parser.parse_notebook(str(p))
    
    assert "pyspark.sql.functions" in metadata["imports"]
    assert "spark.read" in metadata["spark_calls"]
    assert "spark.write" in metadata["spark_calls"]
