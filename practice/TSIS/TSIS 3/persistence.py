import json, os

BASE_DIR = os.path.dirname(__file__)
SETTINGS_PATH = os.path.join(BASE_DIR, "settings.json")
LEADERBOARD_PATH = os.path.join(BASE_DIR, "leaderboard.json")

DEFAULTS = {"sound": True, "car_color": "default", "difficulty": "normal"}

def _load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return default


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_settings():
    d = _load_json(SETTINGS_PATH, {})
    for k, v in DEFAULTS.items():
        d.setdefault(k, v)
    return d


def save_settings(s):
    _save_json(SETTINGS_PATH, s)


def load_leaderboard():
    return _load_json(LEADERBOARD_PATH, [])


def save_score(name, score, distance, coins):
    board = load_leaderboard()
    board.append({"name": name, "score": score, "distance": distance, "coins": coins})
    board = sorted(board, key=lambda x: x["score"], reverse=True)[:10]
    _save_json(LEADERBOARD_PATH, board)
    return board