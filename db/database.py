import sqlite3
import json
import os
from typing import Dict, List, Optional
from config import config

class DatabaseManager:
    def __init__(self):
        self.db_path = config.DATABASE_PATH
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS contracts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    contract_type TEXT NOT NULL,
                    contract_name TEXT NOT NULL,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def save_contract(self, user_id: int, contract_type: str, contract_name: str, data: Dict) -> int:
        """Сохранение данных договора"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'INSERT INTO contracts (user_id, contract_type, contract_name, data) VALUES (?, ?, ?, ?)',
                (user_id, contract_type, contract_name, json.dumps(data, ensure_ascii=False))
            )
            return cursor.lastrowid
    
    def get_user_contracts(self, user_id: int) -> List[Dict]:
        """Получение всех договоров пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT id, contract_type, contract_name, created_at FROM contracts WHERE user_id = ? ORDER BY created_at DESC',
                (user_id,)
            )
            return [{'id': row[0], 'type': row[1], 'name': row[2], 'created_at': row[3]} for row in cursor.fetchall()]
    
    def get_contract_data(self, contract_id: int, user_id: int) -> Optional[Dict]:
        """Получение данных конкретного договора"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'SELECT data FROM contracts WHERE id = ? AND user_id = ?',
                (contract_id, user_id)
            )
            row = cursor.fetchone()
            return json.loads(row[0]) if row else None

db_manager = DatabaseManager()

