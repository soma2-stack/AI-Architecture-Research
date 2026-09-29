"""Small explicit defaults; no hidden environment-dependent behavior."""
DEFAULT_TODAY = "2026-01-01"
DEFAULT_STORE_NAME = "tasks.json"
DEFAULT_LIMIT = 100
MAX_TITLE_LENGTH = 120
MAX_DESCRIPTION_LENGTH = 1000


def validate_text_length(value, maximum, label):
    text = str(value)
    if len(text) > maximum:
        raise ValueError(f"{label} is too long")
    return text


def clamp_limit(value):
    amount = int(value)
    return max(0, min(amount, DEFAULT_LIMIT))


def default_preferences():
    return {"hide_done": False}


def path_for(name, root=None):
    from pathlib import Path
    base = Path(root) if root is not None else Path.cwd()
    return base / name
