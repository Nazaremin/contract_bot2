import os
from dataclasses import dataclass

@dataclass
class Config:
    BOT_TOKEN: str = os.getenv('BOT_TOKEN', '76')
    DATABASE_PATH: str = 'db/contracts.db'
    TEMPLATES_PATH: str = 'templates'
    OUTPUT_PATH: str = 'output'
    ADMIN_USER_ID: int = int(os.getenv('ADMIN_USER_ID', '0'))

config = Config()

