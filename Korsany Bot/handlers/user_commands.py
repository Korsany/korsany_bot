from random import randint as rint
from time import sleep as slp

import qrcode
import g4f
import pyfiglet

from aiogram import Router, F
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message
from aiogram.types import (Message, FSInputFile, InlineKeyboardMarkup,
                           InlineKeyboardButton)
from aiogram.enums import ParseMode

import main
import config
from keyboards import inline

router = Router()
bot = main.bot

ml_admin = [5193123666, 6854009493, 6536683594]


@router.message(CommandStart())
async def start(message: Message):
    await message.answer(f'''
<b>Приветствуем вас, @{message.from_user.username} 👋</b>\n Узнать команды можно через /help''')
    

# Обработчик комманды /help
@router.message(Command('help'))
async def start(message: Message):
    await message.answer(f'''
<b>У меня есть много крутых комманд!</b>
/rn x-y; например /rn 1-100
    Рандомное число от x до y!
/play цифра от 1 до 6
    Игра в кости!
/qrcode Любой текст
    Генерирует qrcode из текста
/link Обычный текст-Текст на кнопке-Ссылка
    Может создать кнопку с ссылкой!
/gpt Ваш запрос для ChatGPT
    Задать вопрос    ChatGPT(контекст в разработке!)
/gpt_ru Ваш запрос для ChatGPT
    Больше подходит для русских и кодеров!
Остальные команды в разработке!
/p_message Ваше сообщение
    Отправлить сообщние в лс создателю бота!''')


@router.message(Command(commands=['private_message', 'p_message']))
async def start(message: Message, command: CommandObject, bot: bot):
    if command.args == None:
        await message.reply('Вы не правельно ввели команду!')
    else:
        await bot.send_message(chat_id="-1002008657754",
                                                     text=f'''Сообщение: {command.args}
<b>Инфа о отправителе!</b>
username: <b>{message.from_user.username}</b>;
ID: <b>{message.from_user.id}</b>''')
        await message.reply('Сообщение отправленно!')


@router.message(Command('admin_m'))
async def admin_m_command(message: Message, command: CommandObject):
    data = command.args
    data = data.split('=')
    a1 = data[0]
    a2 = data[1]
    if message.from_user.id in ml_admin:
        await bot.send_message(chat_id=a1, text=a2)
        await message.answer('💭Сообщение отправленно!💭')
    elif a1 == None or a2 == None:
        await message.answer('Введите команду верно!:\n/admin_m id=текст')
    else:
        await message.answer('🆘Вы не являетесь админом!🆘')


@router.message(Command(commands=['rn', 'random-number']))    # /rn 1-100
async def get_random_number(message: Message, command: CommandObject):
    if command.args == None:
       await message.answer('Укажите агрументы! Пример:\n/rn 1-100')
    else:
      a, b = [int(n) for n in command.args.split('-')]    # [1, 100]
      rnum = rint(a, b)

      await message.reply(f'Рандомное число: {rnum}')


@router.message(Command('play', prefix='!/.'))
async def play_games(message: Message, command: CommandObject):
    x = await message.answer_dice(DiceEmoji.DICE)
    print(x.dice.value)
    slp(2.7)
    if command.args == None:
        await message.answer(
                'Вы неправелльно ввели комманду!\n Пример комманды:\n /play 5')
    else:
        if int(x.dice.value) == int(command.args):
            await message.answer(
                    f'Выпало значение: {int(x.dice.value)}, вы победили!')
        elif int(x.dice.value) != int(command.args):
            await message.answer(
                    f'Выпало значение: {int(x.dice.value)}, вы проиграли!')


@router.message(F.text.lower() == 'play')
async def play_games(message: Message):
    x = await message.answer_dice(DiceEmoji.DICE)
    print(x.dice.value)
    await message.answer(f'Значение: {x.dice.value}')


@router.message(Command('arg'))
async def arg(message: Message, command: CommandObject):
    data = command.args
    data = data.split()
    a1 = data[0]
    a2 = data[1]
    await message.answer(f'1-й: {a1}')
    await message.answer(f'2-й: {a2}')


'''@router.message(Command('file'))
async def arg(message: Message, command: CommandObject):
        if command.args == None:
                await message.answer('Надо указать аргумент - /file имя файла!')
        elif command.args == 'game':
                game = FSInputFile("Ded_moroz.zip")
            result = await message.answer_document(
            filename='Ded_moroz.zip',
            caption='Игра про деда мороза!🎅')
    else:
        await message.answer('Такой файл отсутствует!')'''


@router.message(Command('qrcode'))
async def all_message(message: Message, command: CommandObject):
  if command.args == None:
    await message.reply(text="Вы не указали аркумент!")
  else:
    texts = command.args
    img = qrcode.make(texts)
    img.save("qrcode.png")

    file_ids = []
    # Отправка файла из файловой системы
    image_from_pc = FSInputFile("qrcode.png")
    if message.text:
      result = await message.answer_photo(image_from_pc,
                                          caption=texts,
                                          reply_markup=inline.kanal)
    else:
      await message.reply(
          text="Из картинок, стикеров, смайликов, gif и видео qr-коды не делаю!"
      )


@router.message(Command('link'))
async def link_command(message: Message, command: CommandObject):
  data = command.args
  data = data.split('-')
  a1 = data[0]
  a2 = data[1]
  a3 = data[2]

  if data == None:
    await message.answer("Вы неправильно ввели комманду, посмотрите в /help!")
  elif a2 == None:
    await message.answer("Вы неправильно ввели комманду, посмотрите в /help!")
  elif a3 == None:
    await message.answer("Вы неправильно ввели комманду, посмотрите в /help!")
  else:
    links = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=a2, url=a3)]])
    await message.answer(text=a1, reply_markup=links)


@router.message(Command('font'))
async def link_command(message: Message, command: CommandObject):
  argument = command.args
  font = pyfiglet.figlet_format(argument)
  await message.reply(font + "  ")


@router.message(Command('gpt'))
async def handle_message(message: Message, command: CommandObject):
  if command.args == None:
    await message.answer("Вы не задали вопрос ChatGPT!")
  else:
    user_message = command.args
    slp(1)
    await message.reply(
        'Иммейте в виду, что функция ChatGPT в разработке, если ChatGPT не отвечает в течении 1 минуты, то попробуйте позже! Лучше использовать /gpr_ru'
    )
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.gpt_35_turbo,
        messages=[{
            "role": "user",
            "content": user_message
        }])
    await message.reply(response)


@router.message(Command('gpt_ru'))
async def handle_message(message: Message, command: CommandObject):
  if command.args == None:
    await message.answer("Вы не задали вопрос ChatGPT!")
  else:
    user_message = command.args
    slp(1)
    await message.answer('Бот генерирует запрос...')
    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": user_message + ' (Ответь обязательно на русском языке!)'}])
    response = response.replace('!', '\!').replace('?', '\?').replace('.', '\.').replace(',', '\,').replace(':', '\:')
    await message.bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id+1, text=f'{response}', parse_mode=ParseMode.MARKDOWN_V2)
    #await message.reply(response, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(Command('file'))
async def arg(message: Message, command: CommandObject):
  if command.args == None:
    await message.answer('Надо указать аргумент - /file имя файла!')
  elif command.args == 'game':
    game = FSInputFile("Ded_moroz.zip")
    result = await message.answer_document(document=game,
                                           caption='Игра про деда мороза!🎅')
  else:
    await message.answer('Такой файл отсутствует!')


@router.message(Command('copy'))
async def copy_command(message: Message, command: CommandObject):
  #await message.copy_to(message.chat.id, command.args)
  await message.reply(command.args)
