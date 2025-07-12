#!/usr/bin/env python3
"""
Тестовый скрипт для проверки основных модулей бота
"""

import sys
import os
import unittest
from datetime import datetime

# Добавляем путь к проекту
sys.path.insert(0, '/home/ubuntu/telegram_contract_bot')

def test_imports():
    """Тест импорта всех модулей"""
    print("🔍 Тестирование импорта модулей...")
    
    try:
        from config import config
        print("✅ config.py - OK")
    except Exception as e:
        print(f"❌ config.py - ОШИБКА: {e}")
        return False
    
    try:
        from db.database import db_manager
        print("✅ database.py - OK")
    except Exception as e:
        print(f"❌ database.py - ОШИБКА: {e}")
        return False
    
    try:
        from handlers.states import ContractForm
        print("✅ states.py - OK")
    except Exception as e:
        print(f"❌ states.py - ОШИБКА: {e}")
        return False
    
    try:
        from handlers.document_generator import document_generator
        print("✅ document_generator.py - OK")
    except Exception as e:
        print(f"❌ document_generator.py - ОШИБКА: {e}")
        return False
    
    try:
        from utils.validator import validator
        print("✅ validator.py - OK")
    except Exception as e:
        print(f"❌ validator.py - ОШИБКА: {e}")
        return False
    
    return True

def test_database():
    """Тест работы с базой данных"""
    print("\n📊 Тестирование базы данных...")
    
    try:
        from db.database import db_manager
        
        # Тестовые данные
        test_data = {
            'contract_name': 'Тест №1',
            'contract_date': '01.01.2025',
            'agent_name': 'Тестовый агент'
        }
        
        # Сохранение
        contract_id = db_manager.save_contract(
            user_id=12345,
            contract_type='agent',
            contract_name='Тест №1',
            data=test_data
        )
        
        print(f"✅ Сохранение в БД - OK (ID: {contract_id})")
        
        # Получение
        contracts = db_manager.get_user_contracts(12345)
        if contracts:
            print("✅ Получение из БД - OK")
        else:
            print("❌ Получение из БД - ОШИБКА")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ База данных - ОШИБКА: {e}")
        return False

def test_validator():
    """Тест валидации данных"""
    print("\n✅ Тестирование валидатора...")
    
    try:
        from utils.validator import validator
        
        # Тест валидации даты
        is_valid, error = validator.validate_date("01.01.2025")
        if is_valid:
            print("✅ Валидация даты (корректная) - OK")
        else:
            print(f"❌ Валидация даты (корректная) - ОШИБКА: {error}")
            return False
        
        is_valid, error = validator.validate_date("неправильная дата")
        if not is_valid:
            print("✅ Валидация даты (некорректная) - OK")
        else:
            print("❌ Валидация даты (некорректная) - ОШИБКА")
            return False
        
        # Тест валидации имени
        is_valid, error = validator.validate_name("Тестовое имя", "Имя")
        if is_valid:
            print("✅ Валидация имени - OK")
        else:
            print(f"❌ Валидация имени - ОШИБКА: {error}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Валидатор - ОШИБКА: {e}")
        return False

def test_document_generation():
    """Тест генерации документов"""
    print("\n📄 Тестирование генерации документов...")
    
    try:
        from handlers.document_generator import document_generator
        
        # Тестовые данные
        test_data = {
            'contract_name': 'Тест №1',
            'contract_date': '01.01.2025',
            'agent_name': 'Тестовый агент',
            'principal_name': 'Тестовый принципал',
            'reward': '100000 рублей',
            'requisites': 'Тестовые реквизиты',
            'assignment_details': 'Тестовое поручение',
            'report_details': 'Тестовый отчет'
        }
        
        # Генерация документов
        documents = document_generator.generate_agent_documents(test_data, 12345)
        
        if documents and len(documents) == 3:
            print(f"✅ Генерация документов - OK ({len(documents)} файлов)")
            
            # Проверяем, что файлы созданы
            for doc_path in documents:
                if os.path.exists(doc_path):
                    print(f"✅ Файл создан: {os.path.basename(doc_path)}")
                else:
                    print(f"❌ Файл не найден: {doc_path}")
                    return False
        else:
            print("❌ Генерация документов - ОШИБКА")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Генерация документов - ОШИБКА: {e}")
        return False

def test_templates():
    """Тест наличия шаблонов"""
    print("\n📋 Тестирование шаблонов...")
    
    templates = [
        'agent_template.docx',
        'agent_assignment_template.docx', 
        'agent_report_template.docx',
        'subagent_template.docx',
        'subagent_assignment_template.docx',
        'subagent_report_template.docx',
        'delivery_template.docx'
    ]
    
    templates_dir = '/home/ubuntu/telegram_contract_bot/templates'
    
    for template in templates:
        template_path = os.path.join(templates_dir, template)
        if os.path.exists(template_path):
            print(f"✅ Шаблон найден: {template}")
        else:
            print(f"❌ Шаблон не найден: {template}")
            return False
    
    return True

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов Telegram-бота для договоров\n")
    
    tests = [
        ("Импорт модулей", test_imports),
        ("Шаблоны", test_templates),
        ("База данных", test_database),
        ("Валидатор", test_validator),
        ("Генерация документов", test_document_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Тест: {test_name}")
        print('='*50)
        
        if test_func():
            passed += 1
            print(f"✅ {test_name} - ПРОЙДЕН")
        else:
            print(f"❌ {test_name} - ПРОВАЛЕН")
    
    print(f"\n{'='*50}")
    print(f"РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print('='*50)
    print(f"Пройдено: {passed}/{total}")
    print(f"Процент успеха: {(passed/total)*100:.1f}%")
    
    if passed == total:
        print("🎉 ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО!")
        return True
    else:
        print("⚠️  НЕКОТОРЫЕ ТЕСТЫ ПРОВАЛЕНЫ")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

