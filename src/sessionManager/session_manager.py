import sqlite3
import os
from file_manager.fileManager import FileManager

class SessionManager:
    """Class to manage user sessions."""
    
    def __init__(self, db_path: str = "data/sys_file/session_dir/sessions.db"):
        self.db_path = db_path
        self.file_manager = FileManager()
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize the database if it doesn't exist."""
        if not os.path.exists(self.db_path):
            self.file_manager.ensure_directory_exists(self.db_path)
            self.connection = sqlite3.connect(self.db_path)
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE sessions (
                    user_id TEXT PRIMARY KEY,
                    last_ticker TEXT,
                    last_action TEXT,
                    last_threshold REAL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.connection.commit()
        else:
            self.connection = sqlite3.connect(self.db_path)
    
    def save_session(self, user_id: str, last_ticker: str, last_action: str, last_threshold: float):
        """
        Save or update the user's session.

        Args:
            user_id (str): Unique user identifier.
            last_ticker (str): Last stock ticker analyzed.
            last_action (str): Last action performed.
            last_threshold (float): Last threshold set.
        """
        cursor = self.connection.cursor()
        cursor.execute("""
            INSERT INTO sessions (user_id, last_ticker, last_action, last_threshold)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                last_ticker = excluded.last_ticker,
                last_action = excluded.last_action,
                last_threshold = excluded.last_threshold,
                timestamp = CURRENT_TIMESTAMP
        """, (user_id, last_ticker, last_action, last_threshold))
        self.connection.commit()
    
    def load_session(self, user_id: str):
        """
        Load the user's last session.

        Args:
            user_id (str): Unique user identifier.

        Returns:
            dict: User's session data or None if no session exists.
        """
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM sessions WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if row:
            return {
                "user_id": row[0],
                "last_ticker": row[1],
                "last_action": row[2],
                "last_threshold": row[3],
                "timestamp": row[4]
            }
        return None