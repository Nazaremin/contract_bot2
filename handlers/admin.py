from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import os
import shutil

from config import config
from db.database import db_manager

router = Router()

def is_admin(user_id: int) -> bool:
    """Проверка прав администратора"""
    return user_id == config.ADMIN_USER_ID

@router.message(Command("admin"))
async def admin_command(message: Message):
    """Команда админ-панели"""
    if not is_admin(message.from_user.id):
        await message.answer("❌ У вас нет прав администратора.")
        return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton(text="📁 Управление шаблонами", callback_data="admin_templates")],
        [InlineKeyboardButton(text="🗑️ Очистить выходные файлы", callback_data="admin_cleanup")]
    ])
    
    await message.answer("🔧 Админ-панель:", reply_markup=keyboard)

@router.callback_query(F.data == "admin_stats")
async def admin_stats(callback: CallbackQuery):
    """Показать статистику использования"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа")
        return
    
    # Получаем статистику из базы данных
    with db_manager._get_connection() as conn:
        cursor = conn.execute("SELECT COUNT(*) FROM contracts")
        total_contracts = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT contract_type, COUNT(*) FROM contracts GROUP BY contract_type")
        type_stats = cursor.fetchall()
        
        cursor = conn.execute("SELECT COUNT(DISTINCT user_id) FROM contracts")
        unique_users = cursor.fetchone()[0]
    
    stats_text = f"📊 Статистика бота:\n\n"
    stats_text += f"👥 Уникальных пользователей: {unique_users}\n"
    stats_text += f"📄 Всего договоров: {total_contracts}\n\n"
    stats_text += "По типам:\n"
    
    for contract_type, count in type_stats:
        type_names = {
            'agent': 'Агентские',
            'subagent': 'Субагентские', 
            'delivery': 'Поставки'
        }
        stats_text += f"• {type_names.get(contract_type, contract_type)}: {count}\n"
    
    await callback.message.edit_text(stats_text)
    await callback.answer()

@router.callback_query(F.data == "admin_templates")
async def admin_templates(callback: CallbackQuery):
    """Управление шаблонами"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа")
        return
    
    templates_dir = config.TEMPLATES_PATH
    templates = os.listdir(templates_dir) if os.path.exists(templates_dir) else []
    
    text = "📁 Шаблоны документов:\n\n"
    if templates:
        for template in templates:
            text += f"• {template}\n"
    else:
        text += "Шаблоны не найдены"
    
    text += "\n💡 Для обновления шаблонов замените файлы в папке templates/"
    
    await callback.message.edit_text(text)
    await callback.answer()

@router.callback_query(F.data == "admin_cleanup")
async def admin_cleanup(callback: CallbackQuery):
    """Очистка выходных файлов"""
    if not is_admin(callback.from_user.id):
        await callback.answer("❌ Нет прав доступа")
        return
    
    output_dir = config.OUTPUT_PATH
    if os.path.exists(output_dir):
        files = os.listdir(output_dir)
        for file in files:
            file_path = os.path.join(output_dir, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
        
        await callback.message.edit_text(f"🗑️ Удалено {len(files)} файлов из папки output/")
    else:
        await callback.message.edit_text("📁 Папка output/ не найдена")
    
    await callback.answer()

@router.message(Command("help"))
async def help_command(message: Message):
    """Команда помощи"""
    help_text = """
🤖 Помощь по использованию бота

📋 Основные команды:
/start - Начать создание договора
/cancel - Отменить текущий процесс
/help - Показать эту справку

📝 Типы договоров:
• Агентское соглашение (+ поручение и акт отчета)
• Субагентское соглашение (+ поручение и акт отчета)  
• Договор поставки

💡 Советы:
• Вводите даты в формате ДД.ММ.ГГГГ
• Заполняйте все поля подробно
• Проверяйте данные перед отправкой
• Используйте /cancel для отмены в любой момент

📞 Поддержка: обратитесь к администратору
    """
    
    await message.answer(help_text)

