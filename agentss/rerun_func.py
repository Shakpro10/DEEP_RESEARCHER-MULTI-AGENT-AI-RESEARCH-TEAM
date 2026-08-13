# ================================
# STEP 1: import necessary modules
# ================================
import asyncio
import random
from openai import APIStatusError
from agents import Runner

# Status codes worth retrying: 429 (rate limit) and the 5xx family (server-side / capacity issues)
RETRYABLE_STATUS_CODES = {408, 409, 429, 500, 502, 503, 504}

# ==========================================
# STEP 2: Define the run_with_retry function
# ==========================================
async def run_with_retry(agent, input_message, max_retries=6, base_delay=2.0, max_delay=60.0):
    """
    Drop-in replacement for `await Runner.run(agent, input_message)`.

    Retries with exponential backoff + jitter whenever the underlying model call fails
    with a transient/server-side error (like the NVIDIA "Worker local total request
    limit reached" 503). Any other error (bad auth, bad request, etc.) is raised
    immediately since retrying won't help.

    IMPORTANT: this only ever catches `APIStatusError`. Do not widen that to a bare
    `except Exception` (or `except BaseException`) -- `asyncio.CancelledError` must be
    allowed to propagate untouched, since that's what lets the Gradio Stop button
    actually interrupt an in-flight run. Swallowing/retrying it here would make Stop
    silently keep the agent pipeline running in the background.
    """
    last_error = None
    for attempt in range(max_retries + 1):
        try:
            return await Runner.run(agent, input_message)
        except APIStatusError as e:
            status = getattr(e, "status_code", None)
            last_error = e
            if status not in RETRYABLE_STATUS_CODES or attempt == max_retries:
                raise
            delay = min(max_delay, base_delay * (2 ** attempt)) + random.uniform(0, 1)
            print(f"⚠️  [{agent.name}] got HTTP {status} ({e}). "
                  f"Retrying in {delay:.1f}s (attempt {attempt + 1}/{max_retries})...")
            await asyncio.sleep(delay)
    # Should never get here, but just in case:
    raise last_error