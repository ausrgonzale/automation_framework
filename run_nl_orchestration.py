import argparse
import time

from ai.agents.orchestration_agent import OrchestrationAgent


def parse_natural_language_command(command: str):

    import re

    result = {
        "test_type": None,
        "description": command,
        "app_name": None,
        "url": None,
        "output_path": None,
    }

    # Test type extraction
    if "unit" in command:
        result["test_type"] = "unit"
    elif "playwright" in command:
        result["test_type"] = "playwright"
    elif "e2e" in command or "end-to-end" in command:
        result["test_type"] = "e2e"

    # URL extraction (first http/https URL)
    url_match = re.search(r"https?://\S+", command)
    if url_match:
        result["url"] = url_match.group(0)

    # Improved App name extraction: look for 'Application' or 'app' after the URL, and exclude numbers/ports
    app_name = None
    if result["url"]:
        # Find everything after the URL
        after_url = command.split(result["url"], 1)[1]
        app_match = re.search(
            r"([A-Za-z][\w\- ]+?)(?: Application| app)", after_url, re.IGNORECASE
        )
        if app_match:
            app_name = app_match.group(1).strip()
    else:
        # Fallback: look for 'Application' or 'app' anywhere
        app_match = re.search(
            r"([A-Za-z][\w\- ]+?)(?: Application| app)", command, re.IGNORECASE
        )
        if app_match:
            app_name = app_match.group(1).strip()
    result["app_name"] = app_name

    # Output path extraction
    if "Place test case under" in command:
        after_place = command.split("Place test case under", 1)[1]
        result["output_path"] = after_place.strip().split()[0]

    return result


def summarize_request(request: str) -> str:
    """
    Simple rule-based summarizer: keeps actionable clauses, drops context/filler.
    """
    import re

    # Define action verbs (expandable)
    action_verbs = [
        "generate",
        "create",
        "build",
        "write",
        "get",
        "produce",
        "test",
        "use",
        "save",
        "place",
        "output",
        "go",
        "visit",
        "buy",
        "purchase",
        "order",
        "fetch",
        "collect",
        "retrieve",
        "acquire",
        "find",
        "shop",
        "bring",
        "obtain",
        "run",
        "execute",
        "start",
        "stop",
        "deploy",
        "install",
        "remove",
        "delete",
        "update",
        "upgrade",
    ]

    # Patterns for extracting time/quantity constraints
    time_constraint_patterns = [
        (
            r"run (?:in|within|under|less than) (\d+) ?(seconds|second|s|minutes|minute|ms|milliseconds)",
            lambda m: f"run < {m.group(1)}{m.group(2)[0]}",
        ),
        (
            r"complete (?:in|within|under|less than) (\d+) ?(seconds|second|s|minutes|minute|ms|milliseconds)",
            lambda m: f"complete < {m.group(1)}{m.group(2)[0]}",
        ),
    ]

    # Split into clauses by ',', 'and', 'then', '.', or ';'
    clauses = re.split(r",| and | then |\. |;", request)
    summary = []
    for clause in clauses:
        clause = clause.strip()
        # Normalize time/quantity constraints
        for pat, fmt in time_constraint_patterns:
            m = re.search(pat, clause, re.IGNORECASE)
            if m:
                summary.append(fmt(m))
                break
        else:
            # Extract action verb and its object, keep relevant adverbs/adjectives
            words = clause.split()
            if not words:
                continue
            for i, word in enumerate(words):
                if word.lower() in action_verbs:
                    # Include the verb and everything after (object, relevant modifiers)
                    action_phrase = " ".join(words[i:])
                    # Only keep adverbs/adjectives if they are time/quantity/condition related
                    # e.g., 'quickly', 'while raining', 'in under 10 seconds'
                    # For now, keep the full phrase, but could be further refined
                    summary.append(action_phrase)
                    break
    # Fallback: if nothing matched, return the original
    if not summary:
        return request.strip()
    return ", ".join(summary)


def main():
    parser = argparse.ArgumentParser(
        description="Natural language orchestration entry point"
    )
    parser.add_argument(
        "command", nargs="?", help="Natural language command to process"
    )
    parser.add_argument(
        "--file",
        type=str,
        help="File containing natural language commands (one per line)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and summarize only, without submitting to orchestration.",
    )
    args = parser.parse_args()

    commands = []
    if args.command:
        commands.append(args.command)
    elif args.file:
        with open(args.file) as f:
            commands = [line.strip() for line in f if line.strip()]
    else:
        print("Please provide a command or a file with commands.")
        return

    agent = None

    if not args.dry_run:
        agent = OrchestrationAgent()

    for command in commands:
        print(f"\nProcessing: {command}")
        summarized = summarize_request(command)
        print(f"Summarized: {summarized}")
        parsed = parse_natural_language_command(summarized)
        print(f"Parsed: {parsed}")
        start = time.perf_counter()

        if args.dry_run:
            response = {
                "status": "dry_run",
                "submitted": False,
            }
        else:
            try:
                response = agent.handle_request(summarized)  # type: ignore[union-attr]
            except Exception as exc:
                end = time.perf_counter()
                print(f"Submission failed: {exc}")
                print(f"Transaction time: {end - start:.2f} seconds")
                continue

        end = time.perf_counter()
        print(f"Orchestration response: {response}")

        if not args.dry_run and isinstance(response, dict):
            job_id = response.get("job_id")
            if isinstance(job_id, str):
                status = agent.get_job_status(job_id)  # type: ignore[union-attr]
                print(f"Job status: {status}")

        print(f"Transaction time: {end - start:.2f} seconds")
        print(
            f"(Result would be written to: {parsed.get('output_path', '[default location]')})"
        )


if __name__ == "__main__":
    main()
