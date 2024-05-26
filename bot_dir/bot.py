from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile, CallbackQuery
from juridical_bot.bot_dir import keyboards
from juridical_bot.bot_dir.messages import *
from juridical_bot.bot_dir.gpt import *
from juridical_bot.bot_dir.database import *
from juridical_bot.bot_dir.config import *

wbot = Router()

logging.basicConfig(
    filename=LOGS,
    level=logging.INFO,
    format="%(asctime)s FILE: %(filename)s IN: %(funcName)s MESSAGE: %(message)s",
    filemode="w",
)


class WorkStates(StatesGroup):
    State1 = State()
    State2 = State()


# Обработка команд
@wbot.message(Command("start"))
async def start_handler(msg: Message):
    UsersDatabase()
    MessagesDatabase()
    FeedbackDatabase()
    await msg.delete()
    user_id = msg.from_user.id
    if MessagesDatabase().count_all_users(user_id) > MAX_USERS:
        await msg.answer(text="Превышено кол-во пользователей. Пока.")
        return
    await msg.answer_photo(photo = FSInputFile(r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\txts\main_pic.jpg"),caption=start_text, reply_markup=keyboards.start_keyboard)


@wbot.message(Command("help"))
async def help_handler(msg: Message):
    await msg.delete()
    await msg.answer(text=help_text, reply_markup=keyboards.help_keyboard)


@wbot.message(Command("feedback"))
async def feedback_handler(msg: Message, state: FSMContext):
    await msg.delete()
    user_id = msg.from_user.id
    if MessagesDatabase().count_all_users(user_id) > MAX_USERS:
        await msg.answer(text="Превышено кол-во пользователей. Пока.")
        return
    await msg.answer(text=review_text)
    if FeedbackDatabase().is_user_send_feedback(user_id=user_id):
        feedback = FeedbackDatabase().user_feedback(user_id)
        await msg.answer(text = f'Ваш последний отзыв: \n {feedback}. \n Желаете его изменить?', reply_markup=keyboards.changekb)
        return
    else:
        await state.set_state(WorkStates.State2)



@wbot.message(Command("examples"))
async def examples_handler(msg: Message):
    await msg.delete()
    await msg.answer(text=example_docs_text, reply_markup=keyboards.examples_keyboard)


# Обработка колбэков от кнопок

@wbot.callback_query(F.data == "question_ia")
async def start_ai(msg: Message, state: FSMContext, bot: Bot):
    await msg.delete()
    user_id = msg.from_user.id
    await bot.send_message(chat_id=user_id, text=start_ai_text)
    if MessagesDatabase().count_all_users(user_id) > MAX_USERS:
        await msg.answer(text="Превышено кол-во пользователей. Пока.")
        return
    await state.set_state(WorkStates.State1)


@wbot.callback_query(F.data == "help_commands")
async def help_callback(cb: CallbackQuery):
    await cb.message.delete()
    await cb.message.answer(text=help_text, reply_markup=keyboards.help_keyboard)


@wbot.callback_query(F.data == "docs_examples")
async def docs_callback(cb: CallbackQuery):
    await cb.message.delete()
    await cb.message.answer(text=example_docs_text, reply_markup=keyboards.examples_keyboard)


@wbot.callback_query(F.data == "review")
async def review_callback(cb: CallbackQuery, state: FSMContext):
    await cb.message.delete()
    await cb.message.answer(text=review_text)
    await state.set_state(WorkStates.State2)


@wbot.callback_query(F.data == "back")
async def main_menu(cb: CallbackQuery,state: FSMContext):
    await cb.message.delete()
    await state.clear()
    await cb.message.answer(text=start_text, reply_markup=keyboards.start_keyboard)


@wbot.callback_query(F.data == "continue_generation")
async def continue_ai(msg: Message, state: FSMContext):
    pass


@wbot.callback_query(F.data == "first_doc")
async def first_doc(cb: CallbackQuery):
    await cb.message.delete()
    await cb.message.answer_document(reply_markup=keyboards.back_button, document=FSInputFile(
        path=r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\books\1 doc.docx"),
                                 caption="Вот образец для подачи иска в суд")


@wbot.callback_query(F.data == "secound_doc")
async def secound_doc(cb: CallbackQuery):
    await cb.message.delete()
    await cb.message.answer_document(reply_markup=keyboards.back_button, document=FSInputFile(
        path=r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\books\2 doc.docx"),
                                 caption="Вот образец для подачи заявления на замену срочной службы альтернативной")


@wbot.callback_query(F.data == "third_doc")
async def third_doc(cb: CallbackQuery):
    await cb.message.delete()
    await cb.message.answer_document(reply_markup=keyboards.back_button, document=FSInputFile(
        path=r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\books\3 doc.docx"),
                                 caption="Вот образец для подачи искового заявления о защите чести и достоинства")


# Стэйты

@wbot.message(WorkStates.State1)
async def ai_answer(msg: Message, state: FSMContext):
    message = msg.text
    user_id = msg.from_user.id
    if "продолжи" in message.lower():
        question = MessagesDatabase().last_row(user_id=user_id, role="user")[0][0]
        assistant_content = MessagesDatabase().last_row(user_id=user_id, role="assistant")[0][0]
        status, response, tokens_in_response = continue_gpt_response(question, assistant_content)
        if status:
            await msg.answer(response, reply_markup=keyboards.gpt_keyboard)
            MessagesDatabase().insert_row(user_id=user_id, message=response, role='assistant', tokens=tokens_in_response)
    if message.lower() != 'закончить ответ' and message.lower() != 'продолжи ответ':
        MessagesDatabase().insert_row(user_id=user_id, message=message, role='user', tokens=count_tokens(message))
        prompt = [{
            "role": "user", "text": message
        }]
        success, answer, tokens = ask_gpt(prompt)
        if success:
            await msg.answer(text=answer,reply_markup=keyboards.gpt_keyboard)
            MessagesDatabase().insert_row(user_id=user_id, message=answer, role='assistant', tokens=tokens)
    if message.lower() == 'закончить ответ':
        await msg.answer(text= "Ответ сгенерирован.", reply_markup=keyboards.back_button)
        return


@wbot.message(WorkStates.State2)
async def review_save(msg: Message, state: FSMContext):
    message = msg.text
    user_id = msg.from_user.id
    time = msg.date
    FeedbackDatabase().set_feedback(user_id=user_id, feedback=message, time=time)
    await msg.answer(text="Ваш отзыв сохранен!", reply_markup=keyboards.back_button)


@wbot.message(Command("debug"))
async def debug(message: Message, bot: Bot):
    await bot.send_document(chat_id=message.chat.id, document=FSInputFile(r"C:\Users\user\PycharmProjects\pythonProject\juridical_bot\txts\logs.txt"))




def count_tokens(message):
    import tiktoken
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(message)
    return len(tokens)
