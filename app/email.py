import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
import os

load_dotenv()

mail_sender = os.getenv('MAIL_SENDER')
mail_sender_password = os.getenv('MAIL_SENDER_PASSWORD')
mail_recipient = os.getenv('MAIL_RECIPIENT')

def send_email(theme, dolgi, sum, zalog, imush, phone, date, time):
	msg = MIMEMultipart()
	login = mail_sender # Логин почты
	password = mail_sender_password # Пароль от почты
	poluch = mail_recipient #- Кому отправляете сообщения.
	msg['Subject'] = 'Лид с ТГ бота'
	msg['From'] = mail_sender # Тут от кого отправляли сообщения
	if theme == 'Списание кредитов и долгов':
		part = MIMEText(f"Новый лид! \n\nТелефон: {phone}\nТема консультации: {theme}\nДолги из списка(микрозаймы, кредиты, ЖКХ, налоги): {dolgi}\nСумма долга: {sum}\nКредиты под залог имущества: {zalog}\nИмущество: {imush}\nДата: {date}\nВремя: {time}")
	if theme == 'Юридический вопрос':
		part = MIMEText(f"Новый лид! \n\nТелефон: {phone}\nТема консультации: {theme}\nДата: {date}\nВремя: {time}")
	msg.attach(part)
	#smtp.gmail.com:587 - гугла. Для него надо разрешать подключения сторонних приложениях
	#в настройках аккаунта. Без этого вы не отправите сообщения и плюс вам придет сообщения на
	#почту, что кто то пытался отправить от вашего имени сообщения из сторонней программы.
	#smtp.mail.ru:587 - mail. Маилу пофигу на все, не чего разрешать не надо просто меняете данные и можете отправлять письма.
	#Все остальные имена сервера найдете в интернете))) Они могут немного отличаться 
	server = smtplib.SMTP("smtp.mail.ru:587")
	server.ehlo()
	server.starttls()
	server.login(login, password)
	server.sendmail(msg['From'], [poluch], msg.as_string())