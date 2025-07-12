import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import config
from handlers import common, agent_handlers, delivery_handlers, admin
from db.database import db_manager

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

async def main():
    """Основная функция запуска бота"""
    
    # Проверка токена
    if config.BOT_TOKEN == 'YOUR_BOT_TOKEN_HERE':
        logger.error("❌ Не установлен токен бота! Установите переменную окружения BOT_TOKEN")
        return
    
    # Инициализация бота и диспетчера
    bot = Bot(token=config.BOT_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    
    # Регистрация роутеров
    dp.include_router(common.router)
    dp.include_router(agent_handlers.router)
    dp.include_router(delivery_handlers.router)
    dp.include_router(admin.router)
    
    logger.info("🤖 Бот запускается...")
    
    try:
        # Инициализация базы данных
        logger.info("📊 Инициализация базы данных...")
        
        # Запуск бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Ошибка при запуске бота: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем")

