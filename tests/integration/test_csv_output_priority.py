import csv
import os
import tempfile

from repositories.csv_repository import CsvRepository


def test_csv_repository_priority_column():
    # Setup: create a temp CSV output file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmpfile:
        output_path = tmpfile.name

    # Use the real template and mapping from the repo
    repo = CsvRepository(
        file_path=output_path,
        template_path="templates/testcase_output_template.csv",
        mapping_path="templates/field_mapping.json",
    )

    # Minimal testcase with priority field, using correct mapping keys for 'Excel'
    testcase = {
        "Story ID": "TC1",
        "Summary": "Priority Output",
        "Description": "Step 1",
        "Acceptance Criteria": "Should work",
        "Related": "",
        "Priority": "Critical",
        "Language": "Python",
        "Tool": "Playwright",
    }
    repo.save([testcase], source="Excel")

    # Read back the CSV and check for Priority column and value
    with open(output_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 1
        assert "Priority" in rows[0]
        assert rows[0]["Priority"] == "Critical"

    os.remove(output_path)
