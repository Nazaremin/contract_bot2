import re
from datetime import datetime
from typing import Optional, Tuple

class DataValidator:
    """Класс для валидации пользовательских данных"""
    
    @staticmethod
    def validate_date(date_str: str) -> Tuple[bool, Optional[str]]:
        """
        Валидация даты в формате ДД.ММ.ГГГГ
        Возвращает (is_valid, error_message)
        """
        try:
            datetime.strptime(date_str, "%d.%m.%Y")
            return True, None
        except ValueError:
            return False, "Неверный формат даты. Используйте формат ДД.ММ.ГГГГ (например: 01.01.2025)"
    
    @staticmethod
    def validate_contract_name(name: str) -> Tuple[bool, Optional[str]]:
        """
        Валидация названия договора
        """
        if not name or len(name.strip()) < 1:
            return False, "Название договора не может быть пустым"
        
        if len(name) > 100:
            return False, "Название договора слишком длинное (максимум 100 символов)"
        
        return True, None
    
    @staticmethod
    def validate_name(name: str, field_name: str) -> Tuple[bool, Optional[str]]:
        """
        Валидация имен/названий организаций
        """
        if not name or len(name.strip()) < 2:
            return False, f"{field_name} должно содержать минимум 2 символа"
        
        if len(name) > 200:
            return False, f"{field_name} слишком длинное (максимум 200 символов)"
        
        return True, None
    
    @staticmethod
    def validate_money_amount(amount: str) -> Tuple[bool, Optional[str]]:
        """
        Валидация денежных сумм
        """
        if not amount or len(amount.strip()) < 1:
            return False, "Сумма не может быть пустой"
        
        # Проверяем, содержит ли строка цифры
        if not re.search(r'\d', amount):
            return False, "Сумма должна содержать числовое значение"
        
        return True, None
    
    @staticmethod
    def validate_text_field(text: str, field_name: str, min_length: int = 5) -> Tuple[bool, Optional[str]]:
        """
        Валидация текстовых полей
        """
        if not text or len(text.strip()) < min_length:
            return False, f"{field_name} должно содержать минимум {min_length} символов"
        
        if len(text) > 2000:
            return False, f"{field_name} слишком длинное (максимум 2000 символов)"
        
        return True, None
    
    @staticmethod
    def validate_requisites(requisites: str) -> Tuple[bool, Optional[str]]:
        """
        Валидация реквизитов
        """
        if not requisites or len(requisites.strip()) < 10:
            return False, "Реквизиты должны содержать минимум 10 символов"
        
        if len(requisites) > 1000:
            return False, "Реквизиты слишком длинные (максимум 1000 символов)"
        
        return True, None

validator = DataValidator()

