from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton,
                           KeyboardButtonRequestChat)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

import app.date_time as date_time

main = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Списание кредитов и долгов', )], 
									 [KeyboardButton(text='Юридический вопрос')]], 
							resize_keyboard=True,
							one_time_keyboard=True)

dolgi = InlineKeyboardMarkup(inline_keyboard=[
							[InlineKeyboardButton(text='Ответить на вопросы', callback_data='answer_questions')],
							[InlineKeyboardButton(text='Записаться сразу', callback_data='now')]
							])

dolgi_1 = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Да', callback_data='yes1')],
	[InlineKeyboardButton(text='Нет', callback_data='no1')]
	])

dolgi_2 = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='50000 - 100000', callback_data='sum1')],
	[InlineKeyboardButton(text='более 300 000', callback_data='sum2')]
	])

dolgi_3 = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Есть', callback_data='est')],
	[InlineKeyboardButton(text='Нет', callback_data='net')]
	])

dolgi_4 = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Нет имущества', callback_data='no_imush')],
	[InlineKeyboardButton(text='Только 1 жилье', callback_data='one_zhile')],
	[InlineKeyboardButton(text='Есть жилье и другое имущество', callback_data='zhile_other')]
	])

appointment = InlineKeyboardMarkup(inline_keyboard=[
	[InlineKeyboardButton(text='Записаться к юристу', callback_data='appointment')]
	])

contact = ReplyKeyboardMarkup(
	keyboard=[
	[KeyboardButton(text='Отправить контакт', request_contact=True)]
	],
	resize_keyboard=True,
	one_time_keyboard=True)


async def choose_date():
	days_times = await date_time.get_times_and_dates()
	kb = InlineKeyboardBuilder()
	for day in days_times:
		kb.add(InlineKeyboardButton(text=day, callback_data=f'date_{day}')).row()
	return kb.adjust(2).as_markup()

async def choose_time(date):
	days = await date_time.get_times_and_dates()
	times = days[f"{date}"]
	kb = InlineKeyboardBuilder()
	for time in times:
		kb.add(InlineKeyboardButton(text=time, callback_data=f'time_{time}')).row()
	return kb.adjust(2).as_markup()