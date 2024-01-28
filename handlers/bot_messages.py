from aiogram import Router, F
from aiogram.types import Message

#from keyboards import reply, inline

router = Router()


# Обработчик текста 'message'
@router.message(F.text.lower() == 'message')
async def message_text(message: Message):
  await message.answer(f'{message}')

# Обработчик текста 'message'
@router.message(F.text.lower() == 'message_id')
async def message_text(message: Message):
  await message.answer(f'{message.message_id}')