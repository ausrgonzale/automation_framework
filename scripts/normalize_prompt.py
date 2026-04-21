import argparse
import json
from typing import Optional


def normalize_prompt(
    prompt: str,
    output_format: str = "json",
    no_explanation: bool = True,
    use_inst_tags: bool = False,
    system_prompt: Optional[str] = None,
) -> dict:
    """
    Normalize a prompt for LLM usage with constraints.
    Returns a dict with 'prompt' and 'generation_params'.
    """
    constraints = []
    if no_explanation:
        constraints.append(
            "No reasoning or commentary. Return only the requested output."
        )
    if output_format == "json":
        constraints.append("Output strict JSON only with keys: summary, key_points.")

    # Compose system prompt
    sys_prompt = system_prompt or " ".join(constraints)
    if use_inst_tags:
        prompt = f"[INST] {sys_prompt} {prompt} [/INST]"
    else:
        prompt = f"{sys_prompt}\n{prompt}"

    # Generation parameters (can be extended)
    generation_params = {
        "temperature": 0.0,
        "num_predict": 80,
        "stop": ["Question:", "User:"],
    }

    return {"prompt": prompt, "generation_params": generation_params}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Normalize a prompt for LLM usage.")
    parser.add_argument("prompt", type=str, help="The raw prompt to normalize.")
    parser.add_argument("--output-format", type=str, default="json")
    parser.add_argument("--no-explanation", action="store_true")
    parser.add_argument("--use-inst-tags", action="store_true")
    parser.add_argument("--system-prompt", type=str, default=None)
    args = parser.parse_args()

    result = normalize_prompt(
        args.prompt,
        output_format=args.output_format,
        no_explanation=args.no_explanation,
        use_inst_tags=args.use_inst_tags,
        system_prompt=args.system_prompt,
    )
    print(json.dumps(result, indent=2))
