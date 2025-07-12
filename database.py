import sqlite3
import os

DB_DIR = "db"
DB_NAME = "contracts.db"
DB_PATH = os.path.join(DB_DIR, DB_NAME)


def init_db():
    """Инициализирует базу данных и создает таблицу, если она не существует."""
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        """CREATE TABLE IF NOT EXISTS contracts
                 (user_id INTEGER,
                  contract_type TEXT,
                  contract_name TEXT,
                  contract_name_en TEXT,
                  date TEXT,
                  agent TEXT,
                  agent_en TEXT,
                  principal TEXT,
                  principal_en TEXT,
                  reward TEXT,
                  reward_en TEXT,
                  agent_details TEXT,
                  principal_details TEXT,
                  subagent TEXT,
                  subagent_en TEXT,
                  subagent_details TEXT,
                  subject TEXT,
                  subject_en TEXT,
                  supplier TEXT,
                  supplier_en TEXT,
                  purchaser TEXT,
                  purchaser_en TEXT,
                  supply_items TEXT,
                  price TEXT,
                  delivery TEXT,
                  responsibility TEXT,
                  poruchenie_subject TEXT,
                  poruchenie_deadline TEXT,
                  report_works TEXT,
                  report_amount TEXT,
                  PRIMARY KEY (user_id, contract_name))"""
    )
    conn.commit()
    conn.close()


def save_contract_data(user_id, data):
    """Сохраняет или обновляет данные контракта для пользователя."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Используем 'REPLACE' для вставки или обновления записи
    # Убедимся, что все возможные ключи из user_data присутствуют
    fields = [
        "contract_type",
        "contract_name",
        "contract_name_en",
        "date",
        "agent",
        "agent_en",
        "principal",
        "principal_en",
        "reward",
        "reward_en",
        "agent_details",
        "principal_details",
        "subagent",
        "subagent_en",
        "subagent_details",
        "subject",
        "subject_en",
        "supplier",
        "supplier_en",
        "purchaser",
        "purchaser_en",
        "supply_items",
        "price",
        "delivery",
        "responsibility",
        "poruchenie_subject",
        "poruchenie_deadline",
        "report_works",
        "report_amount",
    ]

    # Создаем словарь с данными для вставки, используя None для отсутствующих ключей
    insert_data = {"user_id": user_id}
    for field in fields:
        insert_data[field] = data.get(field)

    columns = ", ".join(insert_data.keys())
    placeholders = ", ".join([f":{key}" for key in insert_data.keys()])

    # Используем INSERT OR REPLACE для атомарной вставки или обновления
    query = f"INSERT OR REPLACE INTO contracts ({columns}) VALUES ({placeholders})"

    c.execute(query, insert_data)
    conn.commit()
    conn.close()
