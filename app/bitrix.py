import os
from dotenv import load_dotenv

from fast_bitrix24 import BitrixAsync

load_dotenv()
webhook = os.getenv('WEBHOOK_BX')
bx = BitrixAsync(webhook)

async def add_lead(theme, dolgi, sum, zalog, imush, phone, date, time):
	if theme == 'Списание кредитов и долгов':
		json={'fields': {
			'TITLE': 'Заявка с бота',
			'NAME' : 'Пользователь телеграм',
			'PHONE': [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}],
			'COMMENTS': f'Тема консультации: {theme}\nДолги из списка(микрозаймы, кредиты, ЖКХ, налоги): {dolgi}\nСумма долга: {sum}\nКредиты под залог имущества: {zalog}\nИмущество: {imush}\nДата: {date}\nВремя: {time}',
		}
		}
		await bx.call('crm.lead.add', json)
	if theme == 'Юридический вопрос':
		json={ 'fields': {
			'TITLE': 'Заявка с бота',
			'NAME' : 'Пользователь телеграм',
			'PHONE': [{'VALUE': phone, 'VALUE_TYPE': 'WORK'}],
			'COMMENTS': f'Тема консультации: {theme}\nДата: {date}\nВремя: {time}',
		}}
		await bx.call('crm.lead.add', json)