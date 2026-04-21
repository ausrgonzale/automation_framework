import csv
import json
import os
import tempfile

import pytest

from repositories.csv_repository import CsvRepository

TEMPLATE_HEADER = ["id", "title", "steps", "expected_result", "priority"]
FIELD_MAPPING = {
    "Excel": {
        "id": "id",
        "title": "title",
        "steps": "steps",
        "expected_result": "expected_result",
        "priority": "priority",
    }
}


@pytest.fixture
def temp_paths():
    with tempfile.TemporaryDirectory() as tmpdir:
        template_path = os.path.join(tmpdir, "template.csv")
        mapping_path = os.path.join(tmpdir, "mapping.json")
        output_path = os.path.join(tmpdir, "output.csv")
        # Write template
        with open(template_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(TEMPLATE_HEADER)
        # Write mapping
        with open(mapping_path, "w") as f:
            json.dump(FIELD_MAPPING, f)
        yield output_path, template_path, mapping_path


def test_init_writes_header(temp_paths):
    output_path, template_path, mapping_path = temp_paths
    CsvRepository(output_path, template_path, mapping_path)
    with open(output_path) as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == TEMPLATE_HEADER


def test_save_appends_rows(temp_paths):
    output_path, template_path, mapping_path = temp_paths
    repo = CsvRepository(output_path, template_path, mapping_path)
    testcases = [
        {
            "id": 1,
            "title": "T1",
            "steps": "S1",
            "expected_result": "E1",
            "priority": "High",
        },
        {
            "id": 2,
            "title": "T2",
            "steps": "S2",
            "expected_result": "E2",
            "priority": "Low",
        },
    ]
    repo.save(testcases, source="Excel")
    with open(output_path) as f:
        reader = list(csv.reader(f))
        assert reader[0] == TEMPLATE_HEADER
        assert reader[1] == ["1", "T1", "S1", "E1", "High"]
        assert reader[2] == ["2", "T2", "S2", "E2", "Low"]


def test_save_handles_missing_fields(temp_paths):
    output_path, template_path, mapping_path = temp_paths
    repo = CsvRepository(output_path, template_path, mapping_path)
    testcases = [{"id": 3, "title": "T3"}]  # missing fields
    repo.save(testcases, source="Excel")
    with open(output_path) as f:
        reader = list(csv.reader(f))
        assert reader[1][0] == "3"
        assert reader[1][1] == "T3"
        # missing fields should be empty strings
        assert reader[1][2:] == ["", "", ""]
