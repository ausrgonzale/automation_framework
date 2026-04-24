"""
===============================================================================
File: orchestration_agent.py

Location:
    automation_framework/orchestration/

Purpose:
    Class-based Orchestration Agent responsible for:

        - Accepting user requests
        - Normalizing intent
        - Building compact prompts for downstream agents
        - Enqueueing work items into Redis
        - Tracking job lifecycle state

Design Goals:

        - Production-ready structure
        - Minimal external coupling
        - Redis-backed queueing
        - Pluggable workflow execution
        - Clean logging and extensibility

This implementation aligns with the user story:

    As a QE Tester, I would like to have a single AI source to target my
    requests for work and not have to decide which agents should handle
    the request.

===============================================================================
"""

from __future__ import annotations

# asyncio already imported at top
import json
import os
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

sys.path.append(os.path.join(os.path.dirname(__file__), "../../scripts"))
try:
    import redis
except Exception:  # pragma: no cover - fallback path
    redis = None

from scripts.normalize_prompt import normalize_prompt

# =============================================================================
# Job Model
# =============================================================================


@dataclass
class Job:
    """
    Represents a unit of work placed on the Redis queue.
    """

    job_id: str
    task: str
    payload: Dict[str, Any]
    status: str = "queued"
    created_at: str = datetime.utcnow().isoformat()

    def to_json(self) -> str:
        return json.dumps(asdict(self))


# =============================================================================
# Queue Manager
# =============================================================================


class RedisQueueManager:
    """
    Handles Redis queue operations.

    Responsibilities:

        - Enqueue jobs
        - Dequeue jobs
        - Track job status
    """

    def __init__(self):
        self.host = os.getenv("REDIS_HOST", "localhost")
        self.port = int(os.getenv("REDIS_PORT", 6379))
        self.mode = "redis"
        self.client = None
        self.local_queue_dir = Path("changes") / "local_queue"
        self.local_queue_dir.mkdir(parents=True, exist_ok=True)

        if redis is None:
            self.mode = "local"
            return

        try:
            self.client = redis.Redis(
                host=self.host,
                port=self.port,
                decode_responses=True,
            )
            self.client.ping()
        except Exception:
            self.mode = "local"
            self.client = None

    def _queue_file(self, queue_name: str) -> Path:
        safe_name = queue_name.replace(":", "_")
        return self.local_queue_dir / f"{safe_name}.jsonl"

    def _status_file(self) -> Path:
        return self.local_queue_dir / "status.json"

    def _read_statuses(self) -> Dict[str, str]:
        path = self._status_file()
        if not path.exists():
            return {}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return {}

    def _write_statuses(self, statuses: Dict[str, str]) -> None:
        self._status_file().write_text(
            json.dumps(statuses),
            encoding="utf-8",
        )

    # -------------------------------------------------------------------------

    def enqueue(self, queue_name: str, job: Job) -> None:
        if self.mode == "redis" and self.client is not None:
            self.client.rpush(queue_name, job.to_json())
            self.set_status(job.job_id, job.status)
            return

        queue_file = self._queue_file(queue_name)
        with queue_file.open("a", encoding="utf-8") as f:
            f.write(job.to_json() + "\n")
        self.set_status(job.job_id, job.status)

    # -------------------------------------------------------------------------

    def dequeue(self, queue_name: str) -> dict[str, Any] | None:
        if self.mode == "redis" and self.client is not None:
            item = self.client.lpop(queue_name)
            if item is None:
                return None
            if isinstance(item, bytes):
                item = item.decode("utf-8")
            if isinstance(item, list):
                item = [i.decode("utf-8") if isinstance(i, bytes) else i for i in item]
            if isinstance(item, str):
                return json.loads(item)
            return None

        queue_file = self._queue_file(queue_name)
        if not queue_file.exists():
            return None

        lines = queue_file.read_text(encoding="utf-8").splitlines()
        if not lines:
            return None

        first = lines[0]
        remainder = lines[1:]
        queue_file.write_text(
            "\n".join(remainder) + ("\n" if remainder else ""),
            encoding="utf-8",
        )

        try:
            return json.loads(first)
        except Exception:
            return None

    # -------------------------------------------------------------------------

    def set_status(self, job_id: str, status: str) -> None:
        if self.mode == "redis" and self.client is not None:
            key = f"job:{job_id}:status"
            self.client.set(key, status)
            return

        statuses = self._read_statuses()
        statuses[job_id] = status
        self._write_statuses(statuses)

    # -------------------------------------------------------------------------

    def get_status(self, job_id: str) -> str | None:
        if self.mode == "redis" and self.client is not None:
            key = f"job:{job_id}:status"
            value = self.client.get(key)
            if value is None:
                return None
            if isinstance(value, str):
                return value
            return None

        statuses = self._read_statuses()
        return statuses.get(job_id)


# =============================================================================
# Intent Router
# =============================================================================


class IntentRouter:
    """
    Converts user input into structured intent.
    """

    def parse(self, request: str) -> Dict[str, Any]:

        request_lower = request.lower()

        intent: Dict[str, Any] = {
            "source": "jira",
            "story_ids": [],
            "test_type": "manual",
            "execute": False,
        }

        if "automated" in request_lower:
            intent["test_type"] = "automated"

        if "execute" in request_lower:
            intent["execute"] = True

        # Very simple story ID detection pattern
        words = request.split()

        for word in words:
            if "-" in word:
                intent["story_ids"].append(word.strip())

        return intent


# =============================================================================
# Prompt Builder
# =============================================================================


class PromptBuilder:
    """
    Builds compact machine-readable prompts for downstream agents.
    """

    def build_generation_prompt(
        self,
        stories: List[str],
        test_type: str,
        execute: bool,
    ) -> Dict[str, Any]:

        return {
            "task": "generate_testcases",
            "stories": stories,
            "test_type": test_type,
            "execute": execute,
        }


# =============================================================================
# Orchestration Agent
# =============================================================================


class OrchestrationAgent:
    """
    Primary entry point for the automation framework.

    Responsibilities:

        - Accept user request
        - Normalize request intent
        - Build compact prompt
        - Create job
        - Send job to Redis queue
        - Return job metadata
    """

    DEFAULT_QUEUE = "queue:generation"

    # -------------------------------------------------------------------------

    def __init__(self):
        self._run_environment_healthcheck()
        self.router = IntentRouter()
        self.prompt_builder = PromptBuilder()
        self.queue_manager = RedisQueueManager()

    def _run_environment_healthcheck(self):
        import os
        import subprocess

        script_path = os.path.join(
            os.path.dirname(__file__), "../../scripts/environment_healthcheck.sh"
        )
        print(f"[OrchestrationAgent] Running environment health check: {script_path}")
        result = subprocess.run(["bash", script_path], capture_output=True, text=True)
        if result.returncode != 0:
            print("[OrchestrationAgent] Environment health check failed:")
            print(result.stdout)
            print(result.stderr)
            raise RuntimeError("Environment health check failed. See output above.")
        print("[OrchestrationAgent] Environment health check passed.")

    # -------------------------------------------------------------------------

    def handle_request(self, user_request: str) -> dict[str, Any]:
        """
        Main orchestration workflow.
        """
        intent = self.router.parse(user_request)
        prompt_dict = self.prompt_builder.build_generation_prompt(
            stories=intent["story_ids"],
            test_type=intent["test_type"],
            execute=intent["execute"],
        )
        # Normalize the prompt using the shared script
        norm_result = normalize_prompt(
            prompt=json.dumps(prompt_dict, separators=(",", ":")),
            output_format="json",
            no_explanation=True,
            use_inst_tags=False,
            system_prompt=None,
        )
        # Attach normalized prompt and generation params to payload
        prompt_dict["normalized_prompt"] = norm_result["prompt"]
        prompt_dict["generation_params"] = norm_result["generation_params"]
        job = self._create_job(prompt_dict)
        self.queue_manager.enqueue(self.DEFAULT_QUEUE, job)
        return {
            "job_id": job.job_id,
            "queue": self.DEFAULT_QUEUE,
            "status": job.status,
        }

    # -------------------------------------------------------------------------

    def get_job_status(self, job_id: str) -> str | None:
        return self.queue_manager.get_status(job_id)

    # -------------------------------------------------------------------------

    def _create_job(self, payload: dict[str, Any]) -> Job:
        job_id = self._generate_job_id()
        return Job(
            job_id=job_id,
            task=payload.get("task", "unknown"),
            payload=payload,
        )

    # -------------------------------------------------------------------------

    @staticmethod
    def _generate_job_id() -> str:

        return f"JOB-{uuid.uuid4()}"


# =============================================================================
# Example CLI Execution
# =============================================================================


if __name__ == "__main__":

    agent = OrchestrationAgent()
    response = agent.handle_request(
        "Connect to Jira and create automated test cases for AUTH-123 and execute tests"
    )
    print("Job submitted:")
    print(json.dumps(response, indent=2))
