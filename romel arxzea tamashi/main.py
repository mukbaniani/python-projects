from bs4 import BeautifulSoup
import requests
import sqlite3
import smtplib
import concurrent.futures
import re

full_url_list = [8, 9, 10, 11]
url = 'https://www.silksport.ge/Channels/'

tv_id = {8: 'silk sport 1', 9: 'silk sport 2', 10: 'silk sport 3', 11: 'silk universal'}
tv_timetable = {}

for item in full_url_list:
    r = requests.get(url + str(item))
    c = r.content
    soup = BeautifulSoup(c, 'html.parser')
    data = soup.find('div', {'class': 'epg-wrapper order-lg-1'})
    timetable = data.find_all('div', {'class': 'p-3'})
    timetable_list = [i.text.strip() for i in timetable]
    live_match = [i for i in timetable_list if "LIVE" in i]
    tv_timetable[tv_id[item]] = live_match

def create_table():
	conn = sqlite3.connect('info.db')
	cursor = conn.cursor()
	cursor.execute('''
		CREATE TABLE info(
		id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
		username TEXT NOT NULL,
		fav_team TEXT NOT NULL
		)
		''')
	conn.commit()
	cursor.close()
	conn.close()

def insert_data(mail, favorite_team):
	conn = sqlite3.connect('info.db')
	cursor = conn.cursor()
	cursor.execute('''
		INSERT INTO info (username, fav_team) VALUES(?, ?)
		''', (mail, favorite_team, ))
	conn.commit()
	cursor.close()
	conn.close()

def show_data():
	conn = sqlite3.connect('info.db')
	cursor = conn.cursor()
	cursor.execute('''
		SELECT * FROM info
		''')
	data = cursor.fetchall()
	return data

def delete(custumer):
	conn = sqlite3.connect('info.db')
	cursor = conn.cursor()
	cursor.execute('''
		DELETE FROM info WHERE username=?
		''', (custumer,))
	conn.commit()
	cursor.close()
	conn.close()

print('ფავორიტი გუნდის სახელი შეიყვანეთ ქართული შრიფტით\n')

def sendmail(mail, tv, match):
	bot_mail = ''
	bot_password = ''

	with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
		smtp.ehlo()
		smtp.starttls()
		smtp.ehlo()

		smtp.login(bot_mail, bot_password)

		subject = 'დღეს დიდი დღეა'
		body = 'დღეს შენი ფავორიტი გუნდი {} თამაშობს {}'.format(match, tv)

		msg = f"subject: {subject}\n\n{body}"

		smtp.sendmail(bot_mail, mail, msg.encode('utf-8'))

def get_user_fav_team():
	conn = sqlite3.connect('info.db')
	cursor = conn.cursor()
	cursor.execute('''
		SELECT username, fav_team FROM info
		''')
	data = cursor.fetchall()
	check_match(tv_timetable, data)

def check_match(tv_timetable, data):
	mail, tv, matchs = [], [], []
	for user in data:
		for arxi, cxrili in tv_timetable.items():
			for match in cxrili:
				fav_team = user[1]
				rule = r" {}| {}".format(fav_team, fav_team)
				if re.findall(rule, match):
					mail.append(user[0])
					tv.append(arxi)
					matchs.append(match)
	procesing(mail, tv, matchs)
		
def procesing(mail, tv, match):
	with concurrent.futures.ThreadPoolExecutor() as executor:
		executor.map(sendmail, mail, tv, match)

while True:
	choice = input('[a] - მომხმარებლის დამატება\n[s] - განრიგის გაგზავნა\n[q] - გასვლა\n[d] - მომხმარებლის წაშლა\n')
	if choice == 'a':
		mail = input('შეიყვანეთ მეილი\n')
		favorite_team = input('შეიყვანეთ ფავორიტი გუნდი\n')
		insert_data(mail, favorite_team)
	elif choice == 's':
		get_user_fav_team()
	elif choice == 'q':
		break
	elif choice == 'd':
		custumer = input('შეიყვანეთ მომხმარებლის მეილი\n')
		delete(custumer)
	else:
		print('შეიყვანეთ სწორი ბრძალება')