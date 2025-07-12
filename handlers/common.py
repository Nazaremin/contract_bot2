from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime
import logging

from handlers.states import ContractForm
from db.database import db_manager

router = Router()

@router.message(Command("start"))
async def start_command(message: Message, state: FSMContext):
    """Команда /start - начало работы с ботом"""
    await state.clear()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤝 Агентское соглашение", callback_data="agent")],
        [InlineKeyboardButton(text="👥 Субагентское соглашение", callback_data="subagent")],
        [InlineKeyboardButton(text="📦 Договор поставки", callback_data="delivery")],
        [InlineKeyboardButton(text="📋 Мои договоры", callback_data="my_contracts")]
    ])
    
    await message.answer(
        "🏢 Добро пожаловать в бот для создания договоров!\n\n"
        "Выберите тип договора, который хотите создать:",
        reply_markup=keyboard
    )

@router.callback_query(F.data.in_(["agent", "subagent", "delivery"]))
async def process_contract_type(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора типа договора"""
    contract_type = callback.data
    await state.update_data(contract_type=contract_type)
    
    contract_names = {
        "agent": "Агентское соглашение",
        "subagent": "Субагентское соглашение", 
        "delivery": "Договор поставки"
    }
    
    await callback.message.edit_text(
        f"📝 Создание: {contract_names[contract_type]}\n\n"
        "Введите название договора (например: №1, №АС-2024-001):"
    )
    await state.set_state(ContractForm.contract_name)
    await callback.answer()

@router.message(ContractForm.contract_name)
async def process_contract_name(message: Message, state: FSMContext):
    """Обработка ввода названия договора"""
    await state.update_data(contract_name=message.text)
    await message.answer("📅 Введите дату договора в формате ДД.ММ.ГГГГ:")
    await state.set_state(ContractForm.contract_date)

@router.message(ContractForm.contract_date)
async def process_contract_date(message: Message, state: FSMContext):
    """Обработка и валидация даты договора"""
    try:
        datetime.strptime(message.text, "%d.%m.%Y")
        await state.update_data(contract_date=message.text)
        
        user_data = await state.get_data()
        contract_type = user_data["contract_type"]
        
        if contract_type == "agent":
            await message.answer("👤 Введите название/ФИО Агента:")
            await state.set_state(ContractForm.agent_name)
        elif contract_type == "subagent":
            await message.answer("👤 Введите название/ФИО Агента:")
            await state.set_state(ContractForm.agent_name)
        else:  # delivery
            await message.answer("🏭 Введите название/ФИО Поставщика:")
            await state.set_state(ContractForm.supplier_name)
            
    except ValueError:
        await message.answer("❌ Неверный формат даты! Введите в формате ДД.ММ.ГГГГ (например: 01.01.2025):")

@router.message(Command("cancel"))
async def cancel_command(message: Message, state: FSMContext):
    """Команда отмены процесса заполнения"""
    await state.clear()
    await message.answer("❌ Процесс заполнения отменен. Начните заново с /start")

@router.callback_query(F.data == "my_contracts")
async def show_user_contracts(callback: CallbackQuery):
    """Показать договоры пользователя"""
    user_id = callback.from_user.id
    contracts = db_manager.get_user_contracts(user_id)
    
    if not contracts:
        await callback.message.edit_text("📋 У вас пока нет созданных договоров.")
        return
    
    text = "📋 Ваши договоры:\n\n"
    for contract in contracts[:10]:  # Показываем последние 10
        text += f"• {contract['name']} ({contract['type']})\n"
        text += f"  Создан: {contract['created_at'][:16]}\n\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_main")]
    ])
    
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await state.clear()
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🤝 Агентское соглашение", callback_data="agent")],
        [InlineKeyboardButton(text="👥 Субагентское соглашение", callback_data="subagent")],
        [InlineKeyboardButton(text="📦 Договор поставки", callback_data="delivery")],
        [InlineKeyboardButton(text="📋 Мои договоры", callback_data="my_contracts")]
    ])
    
    await callback.message.edit_text(
        "🏢 Выберите тип договора, который хотите создать:",
        reply_markup=keyboard
    )
    await callback.answer()

