import os
import time
from typing import Any

import httpx
import runpod

LORAX_URL = os.getenv("LORAX_URL", "http://127.0.0.1:80")

def wait_for_lorax(timeout: int = 900, poll_interval: float = 2.0) -> None:
    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            response = httpx.get(f"{LORAX_URL}/health", timeout=5)

            if response.status_code == 200:
                return

        except httpx.HTTPError:
            pass

        time.sleep(poll_interval)

    raise RuntimeError("LoRAX did not become ready before timeout")

wait_for_lorax()

def handler(job: dict[str, Any]) -> dict[str, Any]:
    payload = job.get("input") or {}

    prompt = payload["prompt"]

    parameters = {
        "max_new_tokens": payload.get("max_new_tokens", 2000),
        "temperature": payload.get("temperature", 0.6),
        "top_p": payload.get("top_p", 0.9),
        "top_k": payload.get("top_k", 50)
    }

    body: dict[str, Any] = {
        "inputs": prompt,
        "parameters": parameters,
    }

    if adapter_id := payload.get("adapter_id"):
        body["adapter_id"] = adapter_id

    response = httpx.post(
        f"{LORAX_URL}/generate", json=body, timeout=300
    )

    response.raise_for_status()

    return response.json()

runpod.serverless.start({"handler": handler})