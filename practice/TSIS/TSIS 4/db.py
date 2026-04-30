import os
import json
try:
    import psycopg2
except ImportError:
    psycopg2 = None
from config import load_config

BASE_DIR = os.path.dirname(__file__)
LOCAL_LEADERBOARD_PATH = os.path.join(BASE_DIR, "leaderboard.json")

def _load_local_board():
    if os.path.exists(LOCAL_LEADERBOARD_PATH):
        try:
            with open(LOCAL_LEADERBOARD_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return []


def _save_local_board(board):
    with open(LOCAL_LEADERBOARD_PATH, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=2, ensure_ascii=False)


def get_connection():
    if psycopg2 is None:
        raise RuntimeError("psycopg2 is not installed")
    return psycopg2.connect(**load_config())

def save_score(username, score, level):
    board = _load_local_board()
    board.append({"username": username, "score": score, "level": level})
    board = sorted(board, key=lambda x: x["score"], reverse=True)[:10]
    _save_local_board(board)

    if psycopg2 is None:
        return board

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = cur.fetchone()[0]
        cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                    (player_id, score, level))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Save Error: {e}")
    return board

def get_top_10():
    if psycopg2 is None:
        data = _load_local_board()
        return [(entry["username"], entry["score"]) for entry in data[:10]]

    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT p.username, s.score, s.level_reached 
            FROM game_sessions s JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC LIMIT 10
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return rows
    except Exception as e:
        print(f"DB Leaderboard Error: {e}")
        data = _load_local_board()
        return [(entry["username"], entry["score"]) for entry in data[:10]]

def get_personal_best(username):
    if psycopg2 is None:
        data = _load_local_board()
        return max((entry["score"] for entry in data if entry["username"] == username), default=0)
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT MAX(score) FROM game_sessions s 
            JOIN players p ON s.player_id = p.id WHERE p.username = %s
        """, (username,))
        res = cur.fetchone()[0]
        cur.close()
        conn.close()
        return res if res else 0
    except Exception:
        return 0