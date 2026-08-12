"""
src/utils/helpers.py
────────────────────
Small, project-wide utility functions that don't belong to any single agent
or tool but are useful across the codebase.

Categories:
  - Text / string formatting
  - Severity / classification normalisation
  - Safe JSON parsing
  - Retry / resilience
  - Logging shortcuts
  - State introspection helpers
"""

import json
import logging
import time
import functools
from typing import Any, Callable, Optional, TypeVar

logger = logging.getLogger("genesis")

F = TypeVar("F", bound=Callable[..., Any])


# ── Text helpers ──────────────────────────────────────────────────────────────

def truncate(text: str, max_chars: int = 300, suffix: str = "…") -> str:
    """Truncate a string to *max_chars*, appending *suffix* if cut.

    Useful when logging long situation descriptions or LLM prompts without
    flooding the log file.

    >>> truncate("hello world", 5)
    'hello…'
    """
    if len(text) <= max_chars:
        return text
    return text[:max_chars].rstrip() + suffix


def slugify(text: str) -> str:
    """Convert arbitrary text into a lowercase, hyphen-separated slug.

    Used to build stable human-readable identifiers (e.g. thread IDs,
    file names) from free-form situation descriptions.

    >>> slugify("Severe Flooding in Assam, India!")
    'severe-flooding-in-assam-india'
    """
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)   # remove punctuation
    text = re.sub(r"[\s_]+", "-", text)    # whitespace/underscore → hyphen
    text = re.sub(r"-{2,}", "-", text)     # collapse multiple hyphens
    return text.strip("-")


def clean_llm_json(raw: str) -> str:
    """Strip markdown code fences that some LLMs wrap around JSON output.

    Example input:  ```json\n{"key": "value"}\n```
    Example output: {"key": "value"}
    """
    raw = raw.strip()
    if raw.startswith("```"):
        # Remove the opening fence (```json or ```)
        raw = raw.split("\n", 1)[-1]
        # Remove the closing fence
        if raw.endswith("```"):
            raw = raw[: raw.rfind("```")]
    return raw.strip()


# ── Safe parsing ──────────────────────────────────────────────────────────────

def safe_parse_json(raw: str, fallback: Optional[dict] = None) -> dict:
    """Parse a JSON string, returning *fallback* (default: {}) on any error.

    Prevents a single malformed LLM response from crashing the pipeline —
    callers can check for sentinel keys like ``"error": True`` in the fallback
    if they need to detect the failure downstream.

    >>> safe_parse_json('{"passed": true}')
    {'passed': True}
    >>> safe_parse_json("not json", fallback={"error": True})
    {'error': True}
    """
    if fallback is None:
        fallback = {}
    try:
        cleaned = clean_llm_json(raw)
        return json.loads(cleaned)
    except (json.JSONDecodeError, ValueError):
        logger.warning("safe_parse_json: could not parse response — returning fallback")
        return fallback


# ── Severity helpers ──────────────────────────────────────────────────────────

SEVERITY_ORDER = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def normalise_severity(raw: str) -> str:
    """Normalise a free-form severity string to the canonical set.

    The LLM occasionally returns "HIGH" or "High " — this ensures the rest of
    the pipeline always receives one of: low | medium | high | critical.

    >>> normalise_severity("HIGH")
    'high'
    >>> normalise_severity("extreme")   # unknown → 'high' as a safe default
    'high'
    """
    normalised = raw.strip().lower()
    if normalised in SEVERITY_ORDER:
        return normalised
    logger.warning("normalise_severity: unknown value %r — defaulting to 'high'", raw)
    return "high"


def is_severe(severity: str, threshold: str = "high") -> bool:
    """Return True if *severity* is at or above *threshold*.

    >>> is_severe("critical", threshold="high")
    True
    >>> is_severe("low", threshold="medium")
    False
    """
    return SEVERITY_ORDER.get(severity, 0) >= SEVERITY_ORDER.get(threshold, 0)


# ── Retry decorator ───────────────────────────────────────────────────────────

def with_retry(
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
) -> Callable[[F], F]:
    """Decorator: retry a function up to *max_attempts* times with exponential back-off.

    Used on any external HTTP call (Overpass, OSRM, Nominatim) so a transient
    timeout never crashes the pipeline.

    Usage::

        @with_retry(max_attempts=3, delay_seconds=1.0, exceptions=(requests.Timeout,))
        def call_external_api(): ...
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            wait = delay_seconds
            last_exc: Exception = RuntimeError("No attempts made")
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt < max_attempts:
                        logger.warning(
                            "%s failed (attempt %d/%d): %s — retrying in %.1fs",
                            func.__name__, attempt, max_attempts, exc, wait,
                        )
                        time.sleep(wait)
                        wait *= backoff
                    else:
                        logger.error(
                            "%s failed after %d attempts: %s",
                            func.__name__, max_attempts, exc,
                        )
            raise last_exc
        return wrapper  # type: ignore[return-value]
    return decorator


# ── State / dict helpers ──────────────────────────────────────────────────────

def get_nested(data: dict, *keys: str, default: Any = None) -> Any:
    """Safely retrieve a deeply nested value from a dict without raising KeyError.

    >>> get_nested({"a": {"b": 42}}, "a", "b")
    42
    >>> get_nested({"a": {}}, "a", "b", default="missing")
    'missing'
    """
    for key in keys:
        if not isinstance(data, dict):
            return default
        data = data.get(key, default)
        if data is default:
            return default
    return data


def flatten_plan_to_text(plan: dict) -> str:
    """Join the three plan phases into a single readable string.

    Convenient for logging, evals, or passing a plan summary to another LLM
    without having to reconstruct the three-field structure everywhere.
    """
    parts = []
    for phase in ("immediate", "short_term", "recovery"):
        value = plan.get(phase, "").strip()
        if value:
            label = phase.replace("_", " ").title()
            parts.append(f"[{label}] {value}")
    return "\n".join(parts) if parts else "No plan content."


def state_summary(state: dict) -> str:
    """Return a one-line summary of a GenesisState for logging / debugging.

    Keeps log lines short while still capturing the key decision points.
    """
    situation  = truncate(state.get("situation", ""), 80)
    alert      = state.get("alert_info", {})
    dtype      = alert.get("disaster_type", "unknown")
    severity   = alert.get("severity", "unknown")
    passed     = state.get("quality_result", {}).get("passed")
    retries    = state.get("retry_count", 0)
    approved   = state.get("approved")

    qa_str  = "✓" if passed else ("✗" if passed is False else "—")
    app_str = {True: "approved", False: "rejected", None: "pending"}.get(approved, "pending")

    return (
        f"[{dtype}/{severity}] qa={qa_str} retries={retries} "
        f"approval={app_str} | {situation}"
    )


# ── Logging setup ─────────────────────────────────────────────────────────────

def configure_logging(level: str = "INFO") -> None:
    """Configure the root 'genesis' logger with a clean format.

    Call once from ``main.py`` or the FastAPI startup event.  Individual
    modules obtain their logger via ``logging.getLogger('genesis')``.
    """
    numeric = getattr(logging, level.upper(), logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
            datefmt="%H:%M:%S",
        )
    )
    root = logging.getLogger("genesis")
    root.setLevel(numeric)
    if not root.handlers:
        root.addHandler(handler)
