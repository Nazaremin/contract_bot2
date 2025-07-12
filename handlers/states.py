from aiogram.fsm.state import State, StatesGroup

class ContractForm(StatesGroup):
    # Выбор типа договора
    contract_type = State()
    
    # Общие поля
    contract_name = State()
    contract_date = State()
    
    # Агентское соглашение
    agent_name = State()
    principal_name = State()
    reward = State()
    requisites = State()
    assignment_details = State()
    report_details = State()
    
    # Субагентское соглашение
    subagent_name = State()
    agreement_subject = State()
    
    # Договор поставки
    supplier_name = State()
    buyer_name = State()
    goods_services = State()
    price_payment_terms = State()
    delivery_terms = State()
    responsibility = State()
    
    # Завершение
    generate_documents = State()

