import os
import sys

# Ensure scripts/ is on the path for import
sys.path.insert(
    0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../scripts"))
)
from scripts.normalize_prompt import normalize_prompt


def test_normalize_prompt_basic():
    result = normalize_prompt("Summarize this.")
    assert "prompt" in result
    assert "generation_params" in result
    assert "No reasoning or commentary" in result["prompt"]
    assert result["generation_params"]["temperature"] == 0.0
    assert result["generation_params"]["num_predict"] == 80


def test_normalize_prompt_inst_tags():
    result = normalize_prompt("Summarize this.", use_inst_tags=True)
    assert result["prompt"].startswith("[INST]")


def test_normalize_prompt_custom_system():
    result = normalize_prompt(
        "Summarize this.", system_prompt="Only answer in Spanish."
    )
    assert "Only answer in Spanish." in result["prompt"]


def test_normalize_prompt_output_format():
    result = normalize_prompt("Summarize this.", output_format="text")
    assert "JSON format" not in result["prompt"]


def test_normalize_prompt_no_explanation_false():
    result = normalize_prompt("Summarize this.", no_explanation=False)
    assert "No reasoning or commentary" not in result["prompt"]
