import sqlite3 as sq

async def connect() -> None:
	global db, cur
	db = sq.connect('database.db')
	cur = db.cursor()

	cur.execute('''
				CREATE TABLE IF NOT EXISTS users (
				id INTEGER PRIMARY KEY,
				tg_id INTEGER NOT NULL,
				full_name TEXT
				)
				''')
		
	cur.execute('''
				CREATE TABLE IF NOT EXISTS appointments (
				id INTEGER PRIMARY KEY,
				tg_id INTEGER NOT NULL,
				theme TEXT NOT NULL,
				date TEXT NOT NULL,
				time TEXT NOT NULL,
				phone TEXT NOT NULL,
				FOREIGN KEY (tg_id) REFERENCES users(tg_id)
				)
				''')
	
async def add_user(tg_id, first_name):
	user = cur.execute('SELECT * FROM users WHERE tg_id = ?', (tg_id,)).fetchone()
	if not user:
		cur.execute('INSERT INTO users (tg_id, full_name) VALUES (?, ?)', (tg_id, first_name))
		db.commit()

async def add_appointment(tg_id, theme, date, time, phone):
	cur.execute('INSERT INTO appointments (tg_id, theme, date, time, phone) VALUES (?, ?, ?, ?, ?)', (tg_id, theme, date, time, phone))
	db.commit()

async def get_appointments(time):
	appointment = cur.execute('SELECT * FROM appointments WHERE time = ?', (time,)).fetchall()
	if not appointment:
		return False
	else:
		return True

		