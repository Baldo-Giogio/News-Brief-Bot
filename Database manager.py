import asyncio
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import sqlite3
from dataclasses import dataclass

logging.basicConfig (
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger (__name__)

#Initialize the data type of the various sections of the output
@dataclass
class DatabaseManager:
    def __init__(self, db_path: str = "news_bot.db")
    self.db_path = db_path
    self.init_database()

    def init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()


        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                selected_topics TEXT,
                notif_time TEXT,
                tts_enab BOOLEAN DEFAULT 0
                )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS news_cahce(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT,
            articles TEXT,
            date TEXT,
            summary TEXT,
            )
        ''')

        conn.commit()
        conn.close()

    def add_user(self, user_id: int, username: str):
        conn = sqliute3.conect(self.db_path)
        cursor = conn.cursor()
        cursor.execute ('''
            INSERT OR REPLACE INTO users(user_id, user_name, selected_topics, notif_time, tts_enab)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, username, "", "09:00", FALSE))
        conn.commit()
        conn.close()

    def update_user_topics(self, user_id: int, topics: List[str]):
        conn =  sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        topics_json = json.dumps(topics)
         cursor.execute('UPDATE users SET selected_topics = ? WHERE user_id = ?', (topics_json, user_id))
        conn.commit()
        conn.close()

    def get_user_topics(self, user_id: int) -> List[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute ('SELECT selected_topics FROM users WHERE user_id = ?', (user_id))
        result = cursor.fetchone()
        conn.close

        if result and reslut[0]:
            return json.loads(results[0])
        return[]

    def toggle_tts(self, user_id: int) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT tts_enab FROM users WHERE user_id =?',(user_id))
        curr = cursor.fetchone()[0]
        new_val = not curr
        cursor.execute('UPDATE tts_enab = ? WHERE yser_id = ?', (new_val, user_id))
        conn.commit()
        conn.close()
        return new_val

    
