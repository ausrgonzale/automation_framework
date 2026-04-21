"""
Orchestration script for end-to-end test case generation workflow.
Reads user stories from CSV, normalizes them, generates test cases via agent/service,
and writes results to Excel output.
"""

import argparse
import csv
import json
import os
from datetime import datetime

import yaml

from ai.utils.story_normalizer import StoryNormalizer
from repositories.csv_repository import CsvRepository
from services.testcase_generation_service import TestcaseGenerationService


def get_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the orchestration script.
    """
    parser = argparse.ArgumentParser(
        description="Orchestrate test case generation from Excel or Jira user stories."
    )
    parser.add_argument(
        "--source",
        choices=["excel", "jira"],
        default="excel",
        help="Source of user stories: 'excel' for CSV, 'jira' for JSON.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Path to input file (CSV or JSON). Overrides default for source.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Directory to write generated output files. Defaults to exceltmp/ or sibling of input.",
    )
    return parser.parse_args()


def read_user_stories_excel(csv_path: str) -> list[dict]:
    """
    Read user stories from a CSV file and return as a list of dicts.
    """
    with open(csv_path, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]


def read_user_stories_jira(json_path: str) -> list[dict]:
    """
    Read user stories from a JSON file and return as a list of dicts.
    """
    with open(json_path) as f:
        return json.load(f)


def main() -> None:
    """
    Main orchestration function for test case generation.
    Reads input, normalizes, generates, and writes test cases.
    """
    args = get_args()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Load config.yaml
    config_path = os.path.join(os.path.dirname(__file__), "../config/config.yaml")
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Determine input path
    if args.input:
        input_path = args.input
    elif args.source == "excel":
        input_path = (
            config.get("excel", {}).get("input_path")
            or "testdata/userstories/excel/user_stories_excel.csv"
        )
    else:
        input_path = (
            config.get("jira", {}).get("input_path")
            or "testdata/userstories/jira/user_stories_jira.json"
        )

    input_dir = os.path.dirname(input_path)

    # Determine output directory
    if args.output_dir:
        output_dir = args.output_dir
    elif args.source == "excel":
        output_dir = config.get("excel", {}).get("output_dir") or os.path.join(
            input_dir, "exceltmp"
        )
    else:
        output_dir = config.get("jira", {}).get("output_dir") or os.path.join(
            input_dir, "exceltmp"
        )
    os.makedirs(output_dir, exist_ok=True)

    # Determine output file name
    if args.source == "excel":
        output_path = os.path.join(output_dir, f"generated_testcases_{timestamp}.csv")
        user_stories = read_user_stories_excel(input_path)
        source_type = "Excel"
    else:
        output_path = os.path.join(
            output_dir, f"generated_testcases_jira_{timestamp}.csv"
        )
        user_stories = read_user_stories_jira(input_path)
        source_type = "Jira"

    # Normalize stories
    normalized_stories = [StoryNormalizer.normalize(story) for story in user_stories]

    # Initialize repository for CSV output
    repo = CsvRepository(output_path)
    service = TestcaseGenerationService(repo)

    # Generate and save test cases for each story, passing user_story_id
    for idx, story in enumerate(normalized_stories):
        prompt = StoryNormalizer.to_prompt(story)
        user_story_id = str(story.get("id") or "")
        # Pass index for unique Test ID
        testcases = service.generate_testcases(
            prompt, user_story_id=user_story_id, extra_fields=story, testcase_index=idx
        )
        repo.save(testcases, source=source_type)

    print(f"\nTest cases written to {output_path}")


if __name__ == "__main__":
    main()
