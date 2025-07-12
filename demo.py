#!/usr/bin/env python3
"""
Демонстрационный скрипт для показа возможностей бота
без реального подключения к Telegram API
"""

import sys
import os
from datetime import datetime

# Добавляем путь к проекту
sys.path.insert(0, '/home/ubuntu/telegram_contract_bot')

from handlers.document_generator import generate_documents
from db.database import db_manager
from utils.validator import validator

def demo_agent_contract():
    """Демонстрация создания агентского соглашения"""
    print("🤝 Демонстрация: Агентское соглашение")
    print("="*50)
    
    # Тестовые данные
    data = {
        'contract_type': 'agent',
        'contract_name': 'АС-2025-001',
        'contract_date': '22.06.2025',
        'agent_name': 'ООО "Агентская компания"',
        'principal_name': 'ООО "Принципал"',
        'reward': '150000 (сто пятьдесят тысяч) рублей',
        'requisites': '''
Агент:
ООО "Агентская компания"
ИНН: 1234567890
КПП: 123456789
Адрес: г. Москва, ул. Примерная, д. 1

Принципал:
ООО "Принципал"
ИНН: 0987654321
КПП: 987654321
Адрес: г. Санкт-Петербург, пр. Тестовый, д. 10
        '''.strip(),
        'assignment_details': 'Поиск и привлечение новых клиентов в сфере IT-услуг',
        'report_details': 'Привлечено 5 новых клиентов на общую сумму 500000 рублей'
    }
    
    print("Входные данные:")
    for key, value in data.items():
        if key != 'contract_type':
            print(f"  {key}: {value}")
    
    print("\nВалидация данных...")
    
    # Валидация
    is_valid, error = validator.validate_date(data['contract_date'])
    print(f"  Дата: {'✅' if is_valid else '❌'} {error or 'OK'}")
    
    is_valid, error = validator.validate_name(data['agent_name'], 'Агент')
    print(f"  Агент: {'✅' if is_valid else '❌'} {error or 'OK'}")
    
    is_valid, error = validator.validate_money_amount(data['reward'])
    print(f"  Вознаграждение: {'✅' if is_valid else '❌'} {error or 'OK'}")
    
    print("\nГенерация документов...")
    
    try:
        import asyncio
        documents = asyncio.run(generate_documents(data, 12345))
        
        print(f"✅ Создано документов: {len(documents)}")
        for doc in documents:
            print(f"  📄 {os.path.basename(doc)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def demo_delivery_contract():
    """Демонстрация создания договора поставки"""
    print("\n📦 Демонстрация: Договор поставки")
    print("="*50)
    
    # Тестовые данные
    data = {
        'contract_type': 'delivery',
        'contract_name': 'ДП-2025-001',
        'contract_date': '22.06.2025',
        'supplier_name': 'ООО "Поставщик"',
        'buyer_name': 'ООО "Покупатель"',
        'goods_services': '''
1. Компьютеры ASUS - 10 шт.
2. Мониторы Samsung - 10 шт.
3. Клавиатуры и мыши - 10 комплектов
        '''.strip(),
        'price_payment_terms': 'Общая стоимость: 500000 рублей. Оплата в течение 10 дней с момента поставки.',
        'delivery_terms': 'Поставка в течение 14 дней с момента подписания договора',
        'responsibility': 'За просрочку поставки - пеня 0.1% за каждый день просрочки',
        'requisites': '''
Поставщик:
ООО "Поставщик"
ИНН: 1111111111
КПП: 111111111

Покупатель:
ООО "Покупатель"
ИНН: 2222222222
КПП: 222222222
        '''.strip()
    }
    
    print("Входные данные:")
    for key, value in data.items():
        if key != 'contract_type':
            print(f"  {key}: {value}")
    
    print("\nГенерация документов...")
    
    try:
        import asyncio
        documents = asyncio.run(generate_documents(data, 12346))
        
        print(f"✅ Создано документов: {len(documents)}")
        for doc in documents:
            print(f"  📄 {os.path.basename(doc)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def demo_database():
    """Демонстрация работы с базой данных"""
    print("\n📊 Демонстрация: База данных")
    print("="*50)
    
    # Получаем все договоры пользователя 12345
    contracts = db_manager.get_user_contracts(12345)
    print(f"Договоров пользователя 12345: {len(contracts)}")
    
    for contract in contracts:
        print(f"  • {contract['name']} ({contract['type']}) - {contract['created_at'][:16]}")
    
    # Получаем все договоры пользователя 12346
    contracts = db_manager.get_user_contracts(12346)
    print(f"\nДоговоров пользователя 12346: {len(contracts)}")
    
    for contract in contracts:
        print(f"  • {contract['name']} ({contract['type']}) - {contract['created_at'][:16]}")

def main():
    """Основная демонстрационная функция"""
    print("🚀 ДЕМОНСТРАЦИЯ TELEGRAM-БОТА ДЛЯ ДОГОВОРОВ")
    print("="*60)
    print("Этот скрипт показывает работу бота без подключения к Telegram API")
    print("="*60)
    
    success_count = 0
    total_demos = 3
    
    # Демонстрация агентского соглашения
    if demo_agent_contract():
        success_count += 1
    
    # Демонстрация договора поставки
    if demo_delivery_contract():
        success_count += 1
    
    # Демонстрация базы данных
    demo_database()
    success_count += 1
    
    print(f"\n{'='*60}")
    print("ИТОГИ ДЕМОНСТРАЦИИ")
    print('='*60)
    print(f"Успешно выполнено: {success_count}/{total_demos}")
    
    if success_count == total_demos:
        print("🎉 ВСЕ ДЕМОНСТРАЦИИ ПРОШЛИ УСПЕШНО!")
        print("\n💡 Для запуска реального бота:")
        print("1. Получите токен у @BotFather")
        print("2. Создайте файл .env с токеном")
        print("3. Запустите: python main.py")
    else:
        print("⚠️  НЕКОТОРЫЕ ДЕМОНСТРАЦИИ ЗАВЕРШИЛИСЬ С ОШИБКАМИ")
    
    return success_count == total_demos

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

