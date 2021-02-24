from getpass import getpass
import random
import json
import sqlite3
import hashlib
import re
import colorama
from colorama import Fore

colorama.init(autoreset=True)


def create_table():
    db = sqlite3.connect('users.db')

    cursor = db.cursor()

    q = '''CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                email VARCHAR NOT NULL UNIQUE,
                                password VARCHAR NOT NULL)'''

    q2 = '''CREATE TABLE score (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                right INTEGER NUT NULL,
                                wrong INTEGER NOT NULL,
                                user_id INTEGER NOT NULL,
                                FOREIGN KEY (user_id)
                                    REFERENCES test (user_id)
                                )'''

    db.execute(q)
    db.execute(q2)

    db.commit()
    cursor.close()
    db.close()


def open_questions(choice):
    with open('questions.json', encoding='utf-8') as f:
        data = json.load(f)

    for questions in data[choice]:
        return quiz(questions)


def quiz(choice):
    questions = list(choice.keys())
    random_questions = random.sample(questions, k=len(questions))
    rigth = 0
    wrong = 0
    for i in random_questions:
        q = input(f"{i} დედაქალაქია ? ")
        if q == choice[i]:
            rigth += 1
        else:
            wrong += 1
    print(f"სწორი პასუხები ---> {rigth} არასწორი პასუხები -----> {wrong}")
    return save_results(rigth, wrong)


def save_results(rigth, wrong):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    _SQL = cursor.execute('''INSERT INTO score (right, wrong, user_id) VALUES (?,?,?) ''', (rigth, wrong, user_id))
    conn.commit()
    cursor.close()
    _SQL.close()


def register():
    print(Fore.BLUE + "უკან დასაბრუნებლად შეიყვანეთ 0 \n")
    mail = input('შეიყვანეთ მეილი\n')
    if mail == "0":
        return home()
    password1 = getpass('შეიყვანეთ პაროლი\n')
    if password1 == "0":
        return home()
    password2 = getpass('გაიმეორეთ პაროლი\n')
    if password2 == "0":
        return home()
    return validate_register(mail, password1, password2)


def validate_register(mail, password1, password2):
    validate_mail = re.findall(r'^\S+@\S+\.\S+$', mail)
    if not validate_mail:
        print(Fore.RED + "შეიყვანეთ სწორი მეილი")
        return register()
    elif not password1 or not password2 or password1 != password2:
        print(Fore.RED + "შეიყვანეთ ერთნაირი პაროლი")
        return register()
    else:
        save_user(mail, password1)


def save_user(mail, password1):
    hashed_password = hashlib.md5(password1.encode('utf-8')).hexdigest()
    conn = sqlite3.connect('users.db')
    curson = conn.cursor()
    try:
        curson.execute('''INSERT INTO users (email, password) VALUES (?, ?) ''', (mail, hashed_password))
        conn.commit()
        curson.close()
        conn.close()
        print(Fore.LIGHTCYAN_EX + "წარმატებით გაიარე რეგისტრაცია ახლა გაიარე ავტორიზაცია")
        return login()
    except:
        print(Fore.RED + "მეილი უკვე გამოყენებულია")
        return register()


def login():
    print(Fore.BLUE + 'უკან დასაბრუნებლად დაწერეთ 0 \n')
    mail = input('შეიყვანეთ მეილიn\n')
    if mail == "0":
        return home()
    password = getpass('შეიყვანეთ პაროლი\n')
    if password == "0":
        return home()
    return validate_login(mail, password)


def validate_login(mail, password):
    global user_id
    if mail and password:
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        _SQL = cursor.execute('''SELECT id, password FROM users WHERE email = ?''', (mail,))
        data = _SQL.fetchall()
        if data:
            user_password = data[0][1]
            hashed_passowrd = hashlib.md5(password.encode('utf-8')).hexdigest()
            if user_password == hashed_passowrd:
                user_id = data[0][0]
                return main()
            else:
                print(Fore.RED + 'მეილი ან პაროლი არასწორია')
                return login()
        else:
            print(Fore.RED + 'მეილი ან პაროლი არასწორია')
            return login()
    else:
        print( Fore.RED + 'მეილი ან პაროლი არასწორია')
        return login()


def main():
    print(Fore.LIGHTYELLOW_EX + "წარმატებით გაიარე ავტორიზაცია ახლა აირჩიე რეგიონი შესაბამისი რიცხვით\n")
    while True:
        print("აირჩიეთ რეგიონი")
        user_input = input('''[1] - ევროპა\n[2] - აზია\n[3] -ჩრდილოეთ ამერიკა\n
        \n[4] - სამხრეთი ამერიკა\n[5] - აფრიკა\n[6] - ავსტრალია და ოკენათი\n[8] - სტატისტიკის ნახვა\n[9] - გასვლა\n''')
        if user_input == "9":
            break
        elif user_input == "8":
            stat_info()
        c = {"1": "ევროპა", "2": "აზია", "3": "ჩრდილოეთ ამერიკა", "4": "სამხრეთ ამერიკა", "5": "აფრიკა", "6": "ავსტრალია და ოკეანეთი"}
        key = c.get(user_input)
        if key is None:
            break
        print(open_questions(key))


def stat_info():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    _SQL = cursor.execute('''SELECT SUM(right), SUM(wrong) FROM score WHERE user_id=?''', (user_id,))
    date = _SQL.fetchall()
    print(Fore.YELLOW + f"სწორი პასუხები --> {date[0][0]}\nარასწორი პასუხები --> {date[0][1]}\n")
    return main()


def home():
    while True:
        print("[1] - რეგისტრაცია\n[2] - ავტორიზაცია\n[3] - გავსლა\n")
        custumer_choice = input()
        if custumer_choice == "1":
            register()
            break
        elif custumer_choice == "2":
            login()
            break
        elif custumer_choice == "3":
            break
        else:
            print(Fore.RED + "შეიყვანეთ სწორი ბრძანება")


if __name__ == '__main__':
    home()