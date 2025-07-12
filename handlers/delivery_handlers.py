import os
from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.fsm.context import FSMContext

from handlers.states import ContractForm
from handlers.document_generator import generate_documents

router = Router()

@router.message(ContractForm.supplier_name)
async def process_supplier_name(message: Message, state: FSMContext):
    """Обработка ввода имени поставщика"""
    await state.update_data(supplier_name=message.text)
    await message.answer("🛒 Введите название/ФИО Покупателя:")
    await state.set_state(ContractForm.buyer_name)

@router.message(ContractForm.buyer_name)
async def process_buyer_name(message: Message, state: FSMContext):
    """Обработка ввода имени покупателя"""
    await state.update_data(buyer_name=message.text)
    await message.answer("📦 Введите перечень товаров/услуг:")
    await state.set_state(ContractForm.goods_services)

@router.message(ContractForm.goods_services)
async def process_goods_services(message: Message, state: FSMContext):
    """Обработка перечня товаров/услуг"""
    await state.update_data(goods_services=message.text)
    await message.answer("💰 Введите цену и условия оплаты:")
    await state.set_state(ContractForm.price_payment_terms)

@router.message(ContractForm.price_payment_terms)
async def process_price_payment_terms(message: Message, state: FSMContext):
    """Обработка цены и условий оплаты"""
    await state.update_data(price_payment_terms=message.text)
    await message.answer("🚚 Введите сроки поставки:")
    await state.set_state(ContractForm.delivery_terms)

@router.message(ContractForm.delivery_terms)
async def process_delivery_terms(message: Message, state: FSMContext):
    """Обработка сроков поставки"""
    await state.update_data(delivery_terms=message.text)
    await message.answer("⚖️ Введите ответственность сторон:")
    await state.set_state(ContractForm.responsibility)

@router.message(ContractForm.responsibility)
async def process_responsibility(message: Message, state: FSMContext):
    """Обработка ответственности сторон"""
    await state.update_data(responsibility=message.text)
    await message.answer("🏦 Введите реквизиты сторон:")
    await state.set_state(ContractForm.requisites)

@router.message(ContractForm.requisites)
async def process_delivery_requisites(message: Message, state: FSMContext):
    """Обработка реквизитов для договора поставки и генерация документа"""
    await state.update_data(requisites=message.text)
    
    await message.answer("⏳ Генерирую документ...")
    
    user_data = await state.get_data()
    user_id = message.from_user.id
    
    try:
        document_paths = await generate_documents(user_data, user_id)
        
        await message.answer("✅ Документ готов!")
        
        for path in document_paths:
            with open(path, 'rb') as doc:
                await message.answer_document(document=BufferedInputFile(doc.read(), filename=os.path.basename(path)))
        
        await message.answer("📋 Документ отправлен! Используйте /start для создания нового договора.")
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при генерации документа: {str(e)}")
    
    await state.clear()

