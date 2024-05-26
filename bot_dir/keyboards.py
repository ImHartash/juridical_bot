from aiogram.utils.keyboard import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Задать вопрос GPT", callback_data="question_ia"),
            InlineKeyboardButton(text="Помощь по боту", callback_data="help_commands"),
        ],
        [
            InlineKeyboardButton(
                text="Примеры документов", callback_data="docs_examples"
            ),
            InlineKeyboardButton(text="Оставить отзыв", callback_data="review"),
        ],
    ]
)

help_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Задать вопрос GPT", callback_data="question_ia")],
        [
            InlineKeyboardButton(
                text="Примеры документов", callback_data="docs_examples"
            ),
            InlineKeyboardButton(text="Оставить отзыв", callback_data="review"),
        ],
        [
            InlineKeyboardButton(
                text="Вернуться на главную страницу", callback_data="back"
            ),
        ],
    ]
)

gpt_question = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Продолжить генерацию", callback_data="continue_generation"
            ),
            InlineKeyboardButton(
                text="Закончить генерацию", callback_data="question_ia"
            ),
        ]
    ]
)

examples_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Образей искового заявления", callback_data="first_doc"),
            InlineKeyboardButton(text="Образец замены военной службы", callback_data="secound_doc"),
        ],
        [InlineKeyboardButton(text="Образец защиты права и чести", callback_data="third_doc")],
        [InlineKeyboardButton(text="В главное меню", callback_data="back")],
    ]
)

back_button = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text="Назад", callback_data="back")]]
)

docs_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Назад", callback_data="docs_examples")]
    ]
)

changekb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="yes"),
            InlineKeyboardButton(text="Нет", callback_data="back"),
        ]
    ]
)

gpt_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Продолжи ответ")],
        [KeyboardButton(text="Закончи ответ")],
    ]
)
