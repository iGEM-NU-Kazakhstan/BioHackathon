# Библиотека необходимая для работы ассинхронных методов
import asyncio
import os
import urllib

from aiogram import Bot, Dispatcher, executor, types

# Импортируем класс для работы со стадиями
from aiogram.contrib.middlewares import logging
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import state
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton, CallbackQuery

# Импортируем токен бота из файла config.py
from config import BOT_TOKEN

# Создаем обязательный для работа ассинхронных методов поток в котором будут обрабатываться все события
loop = asyncio.get_event_loop()

storage = MemoryStorage()

# Создаем объект нашего бота, также задаем форматирование для записи курсивом или жирным шрифтом
bot = Bot(BOT_TOKEN, parse_mode="HTML")

# Создаем объект диспатчера, в который передаем нашего бота и созданный ранее поток
dp = Dispatcher(bot, storage=storage, loop=loop)

class Order(StatesGroup):
    zero_action = State()
    first_action = State()
    second_action = State()
    third_action = State()
    fourth_action = State()

@dp.message_handler(commands=['help'])
async def send_welcome(message: types.Message):
    """Отправляет помощь по боту"""
    await message.answer(
        "Hello! I'm Restricton_Hider_3000.\n"
        "Let's start!\n"
        "/start"
        )


@dp.message_handler(commands=['start'], state='*')
async def ask_table(message: types.Message):
    answer_message = 'Choose the codon table from the list below\nSend me the index for example: 1\n\n' \
                     '1. The Standard Code\n'\
                     '2. The Vertebrate Mitochondrial Code\n'\
                     '3. The Yeast Mitochondrial Code\n'\
                     '4. The Mold, Protozoan, and Coelenterate Mitochondrial Code and the Mycoplasma/Spiroplasma Code\n'\
                     '5. The Invertebrate Mitochondrial Code\n'\
                     '6. The Ciliate, Dasycladacean and Hexamita Nuclear Code\n'\
                     '9. The Echinoderm and Flatworm Mitochondrial Code\n'\
                     '10. The Euplotid Nuclear Code\n'\
                     '11. The Bacterial, Archaeal and Plant Plastid Code\n'\
                     '12. The Alternative Yeast Nuclear Code\n'\
                     '13. The Ascidian Mitochondrial Code\n'\
                     '14. The Alternative Flatworm Mitochondrial Code\n'\
                     '16. Chlorophycean Mitochondrial Code\n'\
                     '21. Trematode Mitochondrial Code\n'\
                     '22. Scenedesmus obliquus Mitochondrial Code\n'\
                     '23. Thraustochytrium Mitochondrial Code\n'\
                     '24. Rhabdopleuridae Mitochondrial Code\n'\
                     '25. Candidate Division SR1 and Gracilibacteria Code\n'\
                     '26. Pachysolen tannophilus Nuclear Code\n'\
                     '27. Karyorelict Nuclear Code\n'\
                     '28. Condylostoma Nuclear Code\n'\
                     '29. Mesodinium Nuclear Code\n'\
                     '30. Peritrich Nuclear Code\n'\
                     '31. Blastocrithidia Nuclear Code\n'\
                     '33. Cephalodiscidae Mitochondrial UAA-Tyr Code'
    buttons = InlineKeyboardMarkup(row_width=2)
    buttons.insert(InlineKeyboardButton('Cancel', callback_data='Cancel'))
    await message.answer(answer_message, reply_markup=buttons)
    await Order.zero_action.set()


@dp.message_handler(state=Order.zero_action, content_types=types.ContentTypes.TEXT)
async def ask_sequence_and_site(message: types.Message, state: FSMContext):
    from handlers import choose_codon_table
    try:
        codon_table = choose_codon_table(message.text)
        async with state.proxy() as data:
            data['codon_table'] = codon_table
        answer_message = 'Send me sequence file as plain text or FASTA format\n'
        buttons = InlineKeyboardMarkup(row_width=2)
        buttons.insert(InlineKeyboardButton('Cancel', callback_data='Cancel'))
        await message.answer(answer_message, reply_markup=buttons)
        await Order.first_action.set()
    except BaseException:
        answer_message = ('Wrong input, try again')
        await message.answer(answer_message)



@dp.message_handler(state=Order.first_action, content_types=['document'])
async def choose_sequence(message: types.Message, state: FSMContext):
    """Отправка боту файла и сохранение его в корне"""
    try:
        document_id = message.document.file_id
        file_info = await bot.get_file(document_id)
        fi = file_info.file_path
        name = message.document.file_name
        urllib.request.urlretrieve(f'https://api.telegram.org/file/bot{BOT_TOKEN}/{fi}', f'./{name}')
        buttons = InlineKeyboardMarkup(row_width=2)
        buttons.insert(InlineKeyboardButton('Cancel', callback_data='Cancel'))
        from handlers import read_fasta
        seq = read_fasta(name)
        async with state.proxy() as data:
            data['seq'] = seq
        os.remove(name)
        answer_message = 'Write the restriction site you are looking for.\nFor example: AAGTCG'
        await message.answer(answer_message)
        await Order.second_action.set()
    except BaseException:
        answer_message = ('Wrong input, try again')
        await message.answer(answer_message)


@dp.message_handler(state=Order.second_action, content_types=types.ContentTypes.TEXT)
async def choose_sites(message: types.Message, state: FSMContext):
    try:
        buttons = InlineKeyboardMarkup(row_width=2)
        buttons.insert(InlineKeyboardButton('Cancel', callback_data='Cancel'))
        async with state.proxy() as data:
            pattern = (message.text).upper()
            data['pattern'] = pattern
            seq = data['seq']
            from handlers import find_pattern
            answer_message = 'Patters that I found below\nFormat: index of first nucleotide of site, DNA(+/-)\n\n'
            data['all_patterns'] = find_pattern(seq, pattern)
            for row in find_pattern(seq, pattern):
                answer_message += (str(row[0]) + ' ' + row[1] + '\n')
            await message.answer(answer_message)
            await message.answer('What sites you want to save. Send me index of first nucleotide of site using space as separator. If you want mask all sites send me 0\n\nFor example: 3 5', reply_markup=buttons)
            #await state.finish()
            await Order.third_action.set()
    except BaseException:
        answer_message = ('Wrong input, try again')
        await message.answer(answer_message)


@dp.message_handler(state=Order.third_action, content_types=types.ContentTypes.TEXT)
async def choose_orf(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            sites = message.text
            try:
                for i in sites.split():
                    int(i)
                data['sites'] = sites
                codon_table = data['codon_table']
                seq = data['seq']
                buttons = InlineKeyboardMarkup(row_width=2)
                buttons.insert(InlineKeyboardButton('Cancel', callback_data='Cancel'))
                from handlers import write_file, find_orfs_with_trans
                data['ORFs'] = find_orfs_with_trans(seq, codon_table)
                answer_message = 'ORFs that I found are in file'
                write_file(seq, codon_table)
                with open ('ORFs.txt', 'rb') as file:
                    await message.bot.send_document(chat_id=message.chat.id, document=file)
                os.remove('ORFs.txt')
                await message.answer(answer_message)
                await message.answer('Choose ORFs index that suppose to be real using space as separator or send me 0 if there is no any ORFs.\nFor example: 3 5', reply_markup=buttons)
                #await state.finish()
                await Order.fourth_action.set()
            except BaseException:
                answer_message = ('Wrong input, try again')
                await message.answer(answer_message)
    except BaseException:
        answer_message = ('Wrong input, try again')
        await message.answer(answer_message)


@dp.message_handler(state=Order.fourth_action, content_types=types.ContentTypes.TEXT)
async def masking_of_sites(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            orfs_choosed = message.text
            try:
                for i in orfs_choosed.split():
                    int(i)
                from program import breake_choosen_sites, annotate_restrict_sites  # ТУТ НУЖНО ВЫЗВАТЬ НЕОБХОДИМЫЕ ФУНКЦИИ
                codon_table = data['codon_table']
                seq = data['seq']
                pattern = data['pattern']
                sites = data['sites']
                orfs = data['ORFs']
                all_patterns = data['all_patterns']
                selected_patterns = []
                for i in all_patterns:
                    check_all = False
                    for j in sites.split():
                        if int(j) == i[0]:
                            check_all = True
                    if check_all == False:
                        selected_patterns.append(i)
                annotated_selected_patterns = annotate_restrict_sites(selected_patterns, orfs)
                answer_message = breake_choosen_sites(seq, pattern, annotated_selected_patterns, codon_table)
                with open ('result.txt', 'w') as file:
                    file.write(answer_message)
                with open ('result.txt', 'rb') as file:
                    await message.bot.send_document(chat_id=message.chat.id, document=file)
                os.remove('result.txt')
                await state.finish()
            except BaseException:
                answer_message = ('Wrong input, try again')
                await message.answer(answer_message)
        except BaseException:
            answer_message = ('Wrong input, try again')
            await message.answer(answer_message)


"""Хэндлэр который ловит нажатие инлайн кнопки"""
@dp.callback_query_handler(state='*', text="Cancel")
async def cancel_action(call: CallbackQuery,  state: FSMContext):
    async with state.proxy():
        await call.message.answer('Canceled')
        await call.message.edit_reply_markup()
        await state.finish()


@dp.message_handler()
async def echo(message: types.Message):
    """Отвечает на любые сообщения вне команд и предлагает справку"""
    await message.answer(
        "Sorry, but I can not talk\n"
        "To get help press: /help"
    )

if __name__ == "__main__":
    from handlers import dp

    # Запуск автоматического обмена данных
    executor.start_polling(dp)