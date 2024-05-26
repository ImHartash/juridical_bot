import requests  # модуль для отправки HTTP-запросов

import logging  # модуль для сбора логов

# подтягиваем инфу из config файла
from config import LOGS, MAX_GPT_TOKENS, SYSTEM_PROMPT, GPT_URL, TOKENIZE_URL, GPT_MODEL, IAM_TOKEN, FOLDER_ID


# Настраиваем запись логов в файл
logging.basicConfig(filename=LOGS, level=logging.DEBUG,
                    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s", filemode="a")


# Функция для подсчета количества токенов в сообщениях
def count_gpt_tokens(messages):
    url = GPT_URL
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/{GPT_MODEL}",
        "messages": messages
    }
    try:
        response = requests.post(url=TOKENIZE_URL, json=data, headers=headers).json()['tokens']
        return len(response)
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return 0

# Запрос к GPT
def ask_gpt(messages):
    url = GPT_URL
    headers = {
        'Authorization': f'Bearer {IAM_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'modelUri': f"gpt://{FOLDER_ID}/{GPT_MODEL}",
        "completionOptions": {
            "stream": False,
            "temperature": 0.7,
            "maxTokens": MAX_GPT_TOKENS
        },
        "messages": SYSTEM_PROMPT + messages  # добавляем к системному сообщению предыдущие сообщения
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        # проверяем статус код
        if response.status_code != 200:
            return False, f"Ошибка GPT. Статус-код: {response.status_code}", None

        # если всё успешно - считаем количество токенов, потраченных на ответ,
        # возвращаем статус, ответ, и количество токенов в ответе
        answer = response.json()['result']['alternatives'][0]['message']['text']
        tokens_in_answer = count_gpt_tokens([{'role': 'assistant', 'text': answer}])
        return True, answer, tokens_in_answer
    except Exception as e:
        logging.error(e)  # если ошибка - записываем её в логи
        return False, "Ошибка при обращении к GPT",  None

#previous_messages (list): Список предыдущих сообщений.
#assistant_response (str): Текущий ответ ассистента.
#max_tokens (int, optional): Максимальное количество токенов в ответе. По умолчанию равно MAX_GPT_TOKENS.
#    Продолжает ответ GPT на основе предыдущих сообщений и текущего ответа.
def continue_gpt_response(previous_messages, assistant_response, max_tokens=MAX_GPT_TOKENS):
   
    # Добавляем предыдущие сообщения и текущий ответ к запросу
    messages = previous_messages + [{'role': 'user', 'text': assistant_response}]

    # Отправляем запрос к GPT
    status, response, tokens_in_response = ask_gpt(messages)

    # Продолжаем ответ, пока не достигнем максимального количества токенов
    while tokens_in_response + len(response) < max_tokens:
        messages.append({'role': 'user', 'text': response})
        status, response, tokens_in_response = ask_gpt(messages)

    # Возвращаем статус, продолженный ответ и количество токенов в продолженном ответе
    return status, response, tokens_in_response

if __name__ == '__main__':
    print(count_gpt_tokens([{'role': 'user', 'text': 'Привет'}]))
