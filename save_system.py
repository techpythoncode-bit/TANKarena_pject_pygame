import json
import os

SAVE_FILE = 'save_data.json'


def _load_all():
    """Load full save dictionary. Returns defaults if file missing/corrupt."""
    data = {"highest_unlocked_level": 1, "username": None}
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                file_data = json.load(f)
                if isinstance(file_data, dict):
                    data.update(file_data)
        except (json.JSONDecodeError, OSError):
            pass
    return data


def _save_all(data):
    """Write full save dictionary atomically where possible."""
    # ensure keys exist
    out = {
        "highest_unlocked_level": max(1, int(data.get("highest_unlocked_level", 1))),
        "username": data.get("username") or None,
    }
    with open(SAVE_FILE, 'w') as f:
        json.dump(out, f)


def load_progress():
    """Return highest unlocked level, default 1."""
    return _load_all().get('highest_unlocked_level', 1)


def save_progress(level):
    """Update highest unlocked level, preserving other fields."""
    data = _load_all()
    try:
        level = int(level)
    except Exception:
        level = data.get('highest_unlocked_level', 1)
    # never decrease progress
    data['highest_unlocked_level'] = max(data.get('highest_unlocked_level', 1), level)
    _save_all(data)


def load_username():
    """Return saved username or None if not set."""
    name = _load_all().get('username')
    if isinstance(name, str) and name.strip():
        return name.strip()
    return None


def save_username(username):
    """Save username, preserving other fields."""
    data = _load_all()
    if isinstance(username, str):
        username = username.strip()
    data['username'] = username or None
    _save_all(data)