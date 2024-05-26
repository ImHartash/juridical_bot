# from dotenv import load_dotenv, find_dotenv
from os import getenv



FOLDER_ID_PATH = r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\sets\folder_id.txt"  # ID папки в Yandex Cloud.
GPT_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"
IAM_TOKEN_PATH = r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\sets\iam_token.txt"
GPT_MODEL = "yandexgpt-lite"
BOT_TOKEN = open(r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\sets\bot_token.txt", "r").readline()
ADMINS_IDS = "ADMINS_IDS"  # id admina

TOKENIZE_URL = "TOKENIZE_URL"

MAX_USERS = 3  # максимальное кол-во пользователей

MAX_GPT_TOKENS = 120  # максимальное кол-во токенов в ответе GPT

COUNT_LAST_MSG = 4  # кол-во последних сообщений из диалога

# лимиты для пользователя

MAX_USER_STT_BLOCKS = 10  # 10 аудиоблоков

MAX_USER_TTS_SYMBOLS = 5_000  # 5 000 символов

MAX_USER_GPT_TOKENS = 2_000  # 2 000 токенов

LOGS = r'C:\Users\user\PycharmProjects\pythonProject\juridical_bot\txts\logs.txt'  # файл для логов

SYSTEM_PROMPT = [{'role': 'system',
                 'text': "Ты являешься юридическим консультантом, отвечающим на вопросы пользователей в Telegram через чат-бот. "
                         "Твоя задача назвать нарушенные юридические документы (Уголовный Кодекс, Трудовой и т.п.) по заданной ситуации пользователем"
                         "Пожалуйста, отвечай на вопросы, как если бы ты был опытным юристом, объясняя сложные юридические понятия простыми словами и давая конкретные рекомендации. "
                         "Также предоставляй ссылки на дополнительные ресурсы или законодательные акты, если это необходимо."
                         }]

message_db = r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\txts\message.db"
user_db = r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\txts\user.db"
feedback_db = r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\txts\feedback.db"