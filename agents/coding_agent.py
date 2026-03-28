import anthropic
import os
from dotenv import load_dotenv

from anthropic.types import ToolUseBlock
from pathlib import Path
from pydantic import BaseModel
from typing import Any
from config.anthropic_client import get_anthropic_client


load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    raise RuntimeError("ANTHROPIC_API_KEY not found in.env file")

client = get_anthropic_client()

class ReadArgs(BaseModel):
    """ Read a file from the filesystem. """
    path: str

def execute_read(args: ReadArgs)-> str:
    try:
        return Path(args.path).read_text()
    except Exception as e:
        return f"Error: {e}"
    
class WriteArgs(BaseModel):
    """ Write content to a file on the filesystem. """
    path: str
    content: str

class EditArgs(BaseModel):
    """ Edit a file by replacing exact text with new text. """
    path: str
    old_str: str
    new_str: str

class BashArgs(BaseModel):
    """ Execute a bash command and return the output. """
    command: str

def execute_write(args: WriteArgs) -> str:
    try:
        path = Path(args.path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(args.content)
        return f"Successfully wrote to {args.path}"
    except Exception as e:
        return f"Error: {e}"

def execute_edit(args: EditArgs) -> str:
    try:
        content = Path(args.path).read_text()
        if args.old_str not in content:
            return f"Error: text not found in {args.path}"
        updated = content.replace(args.old_str, args.new_str, 1)
        Path(args.path).write_text(updated)
        return f"Successfully edited {args.path}"
    except Exception as e:
        return f"Error: {e}"

def execute_bash(args: BashArgs) -> str:
    try:
        import subprocess
        result = subprocess.run(args.command, shell=False, capture_output=True, text=True) # type: ignore
        return result.stdout + result.stderr
    except Exception as e:
        return f"Error: {e}"

# Tool definition Clause user to know the tools exists

tools: list[dict[str, Any]] = [
    {"name": "read", "description": "Read a file from the filesystem.", "input_schema": ReadArgs.model_json_schema()},
    {"name": "write",
    "description": "Write content to a file on the filesystem. Both path and content are required — you must have the full file content ready before calling this tool.",
    "input_schema": WriteArgs.
    model_json_schema()},
    {"name": "edit", "description": "Edit a file by replacing exact text with new text.", "input_schema": EditArgs.model_json_schema()},
    {"name": "bash", "description": "Execute a bash command and return the output.", "input_schema": BashArgs.model_json_schema()},
]

# Send query with tools available

messages: list[dict[str, Any]] = []

while True:
    query = input("\nHow can I help you?: ").strip()
    if not query:
        continue
    if query.lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": query})

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8192, # increase to all enough room to create the script.
            tools=tools,  # type: ignore
            messages=messages  # type: ignore
        )

        if response.stop_reason == "end_turn":
            reply = next(block.text for block in response.content if block.type == "text")
            print(f"\nClaude: {reply}")
            messages.append({"role": "assistant", "content": reply})
            break

        tool_results = []
        for block in response.content:
            if not isinstance(block, ToolUseBlock):
                continue
            if block.name == "read":
                result = execute_read(ReadArgs.model_validate(block.input))  # type: ignore
            elif block.name == "write":
                try:
                    result = execute_write(WriteArgs.model_validate(block.input))  # type: ignore
                except Exception as e:
                    result = f"Error: {e} - you must provide both path and content when calling write."
            elif block.name == "edit":
                result = execute_edit(EditArgs.model_validate(block.input))  # type: ignore
            elif block.name == "bash":
                result = execute_bash(BashArgs.model_validate(block.input))  # type: ignore
            else:
                result = f"Error: unknown tool {block.name}"

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": result
            })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
