from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command,ChatMemberUpdatedFilter
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

import app.keyboards as kb

import app.bitrix as bx

import app.email as email

import app.database.db as db

from dotenv import load_dotenv
import os

rt = Router()

class Questions(StatesGroup):
	theme = State()
	dolgi = State()
	sum = State()
	zalog = State()
	imush = State()
	phone = State()
	date = State()
	time = State()

# СТАРТ БОТА
@rt.message(CommandStart())
async def start(message: Message, state: FSMContext):
	await db.add_user(message.from_user.id, message.from_user.full_name)
	await message.reply(f'Здравствуйте, {message.from_user.full_name}! \n\nЧтобы записаться на БЕСПЛАТНУЮ консультацию с юристом Юридической службы «Единство», выберите тему консультации нажав на кнопку ниже', reply_markup=kb.main)
	await state.set_state(Questions.theme)

# ТЕМА КОНСУЛЬТАЦИИ
@rt.message(F.text)
async def buttons_text(message: Message, state: FSMContext):
	if message.text == 'Списание кредитов и долгов':
		await state.update_data(theme='Списание кредитов и долгов')
		await message.answer('Чтобы понять, можно ли списать Ваши долги, ответьте на 4 важных вопроса.\nЭто позволит проанализировать Вашу ситуацию и помочь ее решить', reply_markup=kb.dolgi)
	if message.text == 'Юридический вопрос':
		await state.update_data(theme='Юридический вопрос')
		await message.answer('Мы готовы помочь защитить ваши интересы по этой ситуации! Запишитесь на консультацию с профильным юристом по кнопке ниже!⬇️', reply_markup=kb.appointment)

# ОТВЕТЫ НА ВОПРОСЫ
@rt.callback_query(F.data == 'answer_questions')
async def questions(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('По закону списать можно только долги по: \nМикрозаймам \nКредитам \nЖКХ \nНалогам \n\nЕсли тип долга из списка выше , нажмите ДА \nЕсли долги другие, нажмите НЕТ', reply_markup=kb.dolgi_1)
	await state.set_state(Questions.dolgi)

@rt.callback_query(F.data == 'yes1')
async def yes1(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(dolgi='Да')
	await callback.message.answer('Общая сумма долга по всем обязательствам?', reply_markup=kb.dolgi_2)
	await state.set_state(Questions.sum)

@rt.callback_query(F.data == 'no1')
async def no1(callback: CallbackQuery):
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('⬇️ Кнопка записи ⬇️', reply_markup=kb.appointment)

@rt.callback_query(F.data == 'sum1')
async def sum1(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(sum='50000 - 100000')
	await callback.message.answer('Есть ли у вас кредиты под залог имущества? (например: ипотека, автокредит, и другие)', reply_markup=kb.dolgi_3)
	await state.set_state(Questions.zalog)

@rt.callback_query(F.data == 'sum2')
async def sum2(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(sum='более 300 000')
	await callback.message.answer('Есть ли у вас кредиты под залог имущества? (например: ипотека, автокредит, и другие)', reply_markup=kb.dolgi_3)
	await state.set_state(Questions.zalog)

@rt.callback_query(F.data == 'est')
async def zalog_da(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(zalog='Да')
	await callback.message.answer('Есть ли у вас имущество в собственности ?\n Недвижимое имущество: квартира, земля, гараж, дом и т.п.\n\n Движимое имущество: автомобиль, ценные бумаги и т.п.', reply_markup=kb.dolgi_4)
	await state.set_state(Questions.imush)

@rt.callback_query(F.data == 'net')
async def zalog_net(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(zalog='Нет')
	if Questions.sum == 'более 300 000':
		await callback.message.answer('Есть ли у вас имущество в собственности ?\n Недвижимое имущество: квартира, земля, гараж, дом и т.п.\n\n Движиое имущество: автомобиль, ценные бумаги и т.п.', reply_markup=kb.dolgi_4)
	else:
		await callback.message.answer('Спасибо за ответы! \n\nПредварительно мы оценили вашу ситуацию и можем вам помочь!\nЧтобы мы смогли более детально проанализировать вашу ситуацию и предложить наиболее выгодный вариант решения, нажмите на кнопку записи', reply_markup=kb.appointment)
	await state.set_state(Questions.imush)

@rt.callback_query(F.data == 'no_imush')
async def no_imush(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(imush='Нет')
	await callback.message.answer('Спасибо за ответы! \n\nПредварительно оценили вашу ситуацию. Чтобы начать новую жизнь без долгов - получи консультацию юриста! \nНа ней вы узнаете: \n1) Пошаговый план \n2) Стоимость услуг\n3) Условия социальной программы\n4) Риски и подводные камни', reply_markup=kb.appointment)

@rt.callback_query(F.data == 'one_zhile')
async def one_zhile(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(imush='Одно жилье')
	await callback.message.answer('Спасибо за ответы! \n\nПредварительно оценили вашу ситуацию. Чтобы начать новую жизнь без долгов - получи консультацию юриста! \nНа ней вы узнаете: \n1) Пошаговый план \n2) Стоимость услуг\n3) Условия социальной программы\n4) Риски и подводные камни', reply_markup=kb.appointment)

@rt.callback_query(F.data == 'zhile_other')
async def zhile_other(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await state.update_data(imush='Жилье и другое имущество')
	await callback.message.answer('Спасибо за ответы! Предвартельно оценили вашу ситуацию, при соблюдение прочих условий такие долги можно списать. Чтобы мы смогли более детального проанализировать ситуацию и предложить способы решения финансовых проблем без потери имущества, Вам нужно записаться на бесплатную консультацию к юристу!', reply_markup=kb.appointment)

@rt.callback_query(F.data == 'now')
async def now(callback: CallbackQuery):
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('⬇️ Кнопка записи ⬇️', reply_markup=kb.appointment)

# ЗАПИСЬ НА КОНСУЛЬТАЦИЮ
@rt.callback_query(F.data == 'appointment')
async def appointmentt(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	await callback.message.answer('1.Для продолжения отправь свой номер телефона для записи к юристу. \n\n⬇️ Нажми на кнопку снизу, чтобы отправить свой номер ⬇️ ', reply_markup=kb.contact)
	await state.set_state(Questions.phone)

@rt.message(F.contact)
async def contact(message: Message, state: FSMContext):
	await state.update_data(phone=message.contact.phone_number)
	await message.answer('Выберите удобную дату для консультации', reply_markup=await kb.choose_date())
	await state.set_state(Questions.date)

@rt.callback_query(F.data.startswith('date_'))
async def date(callback: CallbackQuery, state: FSMContext):
	await callback.answer()
	await callback.message.delete()
	date = callback.data.split('_')[1]
	await state.update_data(date=date)
	await callback.message.answer('Выберите удобное время для консультации', reply_markup=await kb.choose_time(date))
	await state.set_state(Questions.time)

@rt.callback_query(F.data.startswith('time_'))
async def time(callback: CallbackQuery, state: FSMContext, bot: Bot):
	await callback.answer()
	await callback.message.delete()
	time = callback.data.split('_')[1]
	db_time = await db.get_appointments(time)
	if db_time == False:
		await state.update_data(time=time)
		data = await state.get_data()
		print(data)
		load_dotenv()
		await db.add_appointment(callback.from_user.id, data["theme"], data["date"], time, data["phone"])
		await bx.add_lead(data["theme"], data["dolgi"], data["sum"], data["zalog"], data["imush"], data["phone"], data["date"], time)
		# email.send_email(data["theme"], data["dolgi"], data["sum"], data["zalog"], data["imush"], data["phone"], data["date"], time)
		await bot.send_message(os.getenv('ADMIN_TG_ID'), f'Новая заявка на консультацию! \n\nТема: {data["theme"]} \nДата: {data["date"]} в {time} \nТелефон: {data["phone"]}')
		await callback.message.answer(f'Вы записаны на встречу! \n\nНаш офис находится по адресу: г. Кемерово ул. Ноградская 32 (ост. Главпочтамт) \nДата: {data["date"]} в {time} \n\nТелефон: 8 (3842)78-00-98\n<a href="https://2gis.ru/kemerovo/firm/70000001082550197">Ссылка на 2ГИС</a>', parse_mode="html")
		await state.clear()
	if db_time == True:
		data = await state.get_data()
		await callback.message.answer('Время занято, выберите другое', reply_markup=await kb.choose_time(data["date"]))