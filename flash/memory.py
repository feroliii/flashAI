import sqlite3
from pathlib import Path

from flash.providers import Message

class MemoryStore:
    def __init__(self, db_path: str = "data/flash.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        self.connection = sqlite3.connect(self.db_path)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS facts(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL UNIQUE,
                create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.connection.commit()

    def add_message(self, role: str, content: str) -> None:
        self.connection.execute(
            "INSERT INTO messages (role, content) VALUES (?, ?)",
            (role, content),
        )

        self.connection.commit()

    def get_recent_messages(self, limit: int = 20) -> list[Message]:
        rows = self.connection.execute("""
            SELECT role, content
            FROM (
                SELECT id, role, content
                FROM messages
                ORDER BY id DESC
                LIMIT ?
            )
            ORDER BY id ASC
        """,
        (limit,),
        ).fetchall()

        return [
            {"role": role, "content": content}
            for role, content in rows
        ]

    def add_fact(self, content: str) -> None:
        content = content.strip()

        if not content:
            raise ValueError("O fato não pode estar vazio.")

        self.connection.execute(
            "INSERT OR IGNORE INTO facts (content) VALUES (?)",
            (content,),
        )

        self.connection.commit()

    def get_facts(self) -> list[tuple[int, str]]:
        rows = self.connection.execute(
            "SELECT id, content FROM facts ORDER BY id"
        ).fetchall()

        return rows

    def delete_fact(self, fact_id: int) -> bool:
        cursor = self.connection.execute(
            "DELETE FROM facts WHERE id = ?",
            (fact_id,),
        )

        self.connection.commit()

        return cursor.row > 0

    def close(self) -> None:
        self.connection.close()