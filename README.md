# Telegram бот для генерации договоров

Этот бот позволяет пользователям генерировать договоры различных типов (агентское соглашение, субагентское соглашение, договор поставки) на основе шаблонов.

## Установка

1.  **Клонируйте репозиторий:**
    ```bash
    git clone <URL репозитория>
    cd <название папки>
    ```

2.  **Создайте и активируйте виртуальное окружение:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Для Windows: venv\Scripts\activate
    ```

3.  **Установите зависимости:**
    ```bash
    pip install -r requirements.txt
    ```

## Настройка

1.  **Получите токен для вашего Telegram бота** у [@BotFather](https://t.me/BotFather).

2.  **Установите токен в качестве переменной окружения:**
    ```bash
    export TELEGRAM_TOKEN="ВАШ_ТОКЕН"
    ```
    Или создайте файл `.env` и запишите в него `TELEGRAM_TOKEN="ВАШ_ТОКЕН"`.

3.  **Поместите шаблоны договоров в папку `templates`**. Названия файлов должны соответствовать формату:
    *   `agent_template.docx`
    *   `agent_assignment_template.docx`
    *   `agent_report_template.docx`
    *   `subagent_template.docx`
    *   `subagent_assignment_template.docx`
    *   `subagent_report_template.docx`
    *   `supply_template.docx`

## Запуск

Для запуска бота выполните команду:
```bash
python main.py
```

## Как это работает

1.  **Запустите бота** командой `/start` в Telegram.
2.  **Выберите тип договора** с помощью кнопок.
3.  **Отвечайте на вопросы бота**, чтобы предоставить необходимые данные для договора.
4.  **Выберите формат файла** (PDF или DOCX).
5.  **Бот сгенерирует и пришлет вам готовый документ**.
