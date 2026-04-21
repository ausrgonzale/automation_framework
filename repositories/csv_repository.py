import csv
import json
from pathlib import Path
from typing import Any, Dict, List


class CsvRepository:
    """
    Repository for writing test cases to a CSV file using a template and field mapping.
    """

    def __init__(
        self,
        file_path: str = "testcases.csv",
        template_path: str = "templates/testcase_output_template.csv",
        mapping_path: str = "templates/field_mapping.json",
    ) -> None:
        """
        Initialize CsvRepository with output file, template, and mapping.
        """
        self.file_path: str = file_path
        self.output_columns: List[str]
        self.field_mapping: Dict[str, Dict[str, str]]
        # Load output columns from template
        template_file = Path(template_path)
        if not template_file.exists():
            raise FileNotFoundError(f"Output template not found: {template_path}")
        with open(template_file, newline="") as f:
            reader = csv.reader(f)
            self.output_columns = next(reader)
        # Load field mapping
        mapping_file = Path(mapping_path)
        if not mapping_file.exists():
            raise FileNotFoundError(f"Field mapping not found: {mapping_path}")
        with open(mapping_file) as f:
            self.field_mapping = json.load(f)
        # Write header immediately if file does not exist
        if not Path(self.file_path).exists():
            with open(self.file_path, mode="w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.output_columns)

    def save(self, testcases: List[Dict[str, Any]], source: str = "Excel") -> None:
        """
        Save a list of test cases to the CSV file using the correct mapping for the source.
        """
        mapping: Dict[str, str] = self.field_mapping.get(source, {})
        with open(self.file_path, mode="a", newline="") as f:
            writer = csv.writer(f)
            for testcase in testcases:
                row: List[str] = []
                for col in self.output_columns:
                    norm_field: str | None = None
                    for k, v in mapping.items():
                        if v == col:
                            norm_field = k
                            break
                    if norm_field is not None:
                        val = testcase.get(col, testcase.get(norm_field, ""))
                    else:
                        val = testcase.get(col, "")
                    if isinstance(val, list):
                        val = ",".join(str(x) for x in val)
                    row.append(val if val is not None else "")
                writer.writerow(row)
