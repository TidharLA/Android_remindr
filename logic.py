import re
import sqlite3
from datetime import datetime
from pathlib import Path


class MemoryStore:
    def __init__(self, db_path: str = "memories.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self._create()

    def _create(self) -> None:
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT NOT NULL UNIQUE,
                location TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
            """
        )
        self.conn.commit()

    def save(self, item: str, location: str) -> None:
        item = normalize_text(item)
        location = normalize_text(location)
        cur = self.conn.cursor()
        cur.execute(
            """
            INSERT INTO memories(item, location, created_at)
            VALUES (?,?,?)
            ON CONFLICT(item) DO UPDATE SET
                location=excluded.location,
                created_at=excluded.created_at
            """,
            (item, location, datetime.utcnow().isoformat()),
        )
        self.conn.commit()

    def retrieve_and_delete(self, item: str):
        item = normalize_text(item)
        cur = self.conn.cursor()
        cur.execute("SELECT id, location FROM memories WHERE item=? LIMIT 1", (item,))
        row = cur.fetchone()
        if not row:
            return None
        rid, location = row
        cur.execute("DELETE FROM memories WHERE id=?", (rid,))
        self.conn.commit()
        return location

    def list_all(self):
        cur = self.conn.cursor()
        cur.execute("SELECT item, location FROM memories ORDER BY created_at DESC")
        return cur.fetchall()

    def close(self):
        self.conn.close()


def normalize_text(text: str) -> str:
    t = text.strip().lower()
    t = re.sub(r"\s+", " ", t)
    return t


def parse_store(text: str):
    t = normalize_text(text)
    pattern = r"^i\s+(?:put|placed|kept|left)\s+(?:the\s+)?(.+?)\s+(?:in|on|at)\s+(?:the\s+)?(.+)$"
    match = re.match(pattern, t)
    if match:
        item = match.group(1).strip(" .!?")
        loc = match.group(2).strip(" .!?")
        if item and loc:
            return item, loc
    return None


def parse_query(text: str):
    t = normalize_text(text)
    patterns = [
        r"^where\s+is\s+(?:the\s+|my\s+)?(.+?)\??$",
        r"^where\s+are\s+(?:the\s+|my\s+)?(.+?)\??$",
    ]
    for pattern in patterns:
        match = re.match(pattern, t)
        if match:
            item = match.group(1).strip(" .!?")
            if item:
                return item
    return None


def process_text(text: str, store: MemoryStore) -> str:
    store_cmd = parse_store(text)
    if store_cmd:
        item, loc = store_cmd
        store.save(item, loc)
        return f"Saved: {item} -> {loc}"

    query_item = parse_query(text)
    if query_item:
        loc = store.retrieve_and_delete(query_item)
        if loc is None:
            return f"No memory found for '{query_item}'."
        return f"{query_item} is in {loc}. Removed from list."

    return "Not understood. Try: 'I put X in Y' or 'Where is X?'"

