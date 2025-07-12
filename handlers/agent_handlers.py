import os
from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from handlers.states import ContractForm
from handlers.document_generator import generate_documents

router = Router()

@router.message(ContractForm.agent_name)
async def process_agent_name(message: Message, state: FSMContext):
    """Обработка ввода имени агента"""
    await state.update_data(agent_name=message.text)
    
    user_data = await state.get_data()
    if user_data["contract_type"] == "subagent":
        await message.answer("👥 Введите название/ФИО Субагента:")
        await state.set_state(ContractForm.subagent_name)
    else:
        await message.answer("🏢 Введите название/ФИО Принципала:")
        await state.set_state(ContractForm.principal_name)

@router.message(ContractForm.subagent_name)
async def process_subagent_name(message: Message, state: FSMContext):
    """Обработка ввода имени субагента"""
    await state.update_data(subagent_name=message.text)
    await message.answer("🏢 Введите название/ФИО Принципала:")
    await state.set_state(ContractForm.principal_name)

@router.message(ContractForm.principal_name)
async def process_principal_name(message: Message, state: FSMContext):
    """Обработка ввода имени принципала"""
    await state.update_data(principal_name=message.text)
    
    user_data = await state.get_data()
    if user_data["contract_type"] == "subagent":
        await message.answer("📋 Введите предмет соглашения:")
        await state.set_state(ContractForm.agreement_subject)
    else:
        await message.answer("💰 Введите размер вознаграждения:")
        await state.set_state(ContractForm.reward)

@router.message(ContractForm.agreement_subject)
async def process_agreement_subject(message: Message, state: FSMContext):
    """Обработка предмета субагентского соглашения"""
    await state.update_data(agreement_subject=message.text)
    await message.answer("💰 Введите размер вознаграждения:")
    await state.set_state(ContractForm.reward)

@router.message(ContractForm.reward)
async def process_reward(message: Message, state: FSMContext):
    """Обработка размера вознаграждения"""
    await state.update_data(reward=message.text)
    await message.answer("🏦 Введите реквизиты сторон:")
    await state.set_state(ContractForm.requisites)

@router.message(ContractForm.requisites)
async def process_requisites(message: Message, state: FSMContext):
    """Обработка реквизитов сторон"""
    await state.update_data(requisites=message.text)
    await message.answer("📝 Введите детали поручения:")
    await state.set_state(ContractForm.assignment_details)

@router.message(ContractForm.assignment_details)
async def process_assignment_details(message: Message, state: FSMContext):
    """Обработка деталей поручения"""
    await state.update_data(assignment_details=message.text)
    await message.answer("📊 Введите детали для акта отчета:")
    await state.set_state(ContractForm.report_details)

@router.message(ContractForm.report_details)
async def process_report_details(message: Message, state: FSMContext):
    """Обработка деталей акта отчета и генерация документов"""
    await state.update_data(report_details=message.text)
    
    await message.answer("⏳ Генерирую документы...")
    
    user_data = await state.get_data()
    user_id = message.from_user.id
    
    try:
        document_paths = await generate_documents(user_data, user_id)
        
        await message.answer("✅ Документы готовы!")
        
        for path in document_paths:
            with open(path, 'rb') as doc:
                await message.answer_document(document=BufferedInputFile(doc.read(), filename=os.path.basename(path)))
        
        await message.answer("📋 Все документы отправлены! Используйте /start для создания нового договора.")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации документов: {str(e)}")
    
    await state.clear()

