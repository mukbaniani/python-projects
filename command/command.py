import os
import shutil
import subprocess

def pwd():
    print(os.getcwd())

def make_dir(dir_name):
    return os.mkdir(''.join(dir_name))

def make_many_dir(*args):
    for dirs in range(len(args)):
        try:
            os.makedirs(args[dirs] + r"/" + args[dirs + 1])
        except:
            break

def remove_dir(dir_name_method):
    if dir_name_method[1] is None:
        return os.rmdir(''.join(dir_name_method[0]))
    elif dir_name_method[1] == 'all':
        return shutil.rmtree(''.join(dir_name_method[0]))

def where_file(file):
    file = ''.join(file)
    for path, dir_name, file_name in os.walk(os.getcwd()):
        if file in file_name or file in dir_name:
            print(path)
            break
    return 'file not found'

def change_dir(dir_name):
    for path in dir_name:
        os.chdir(os.getcwd() + '\\' + path)

def ls(path_name=None):
    if path_name is None:
        print(os.listdir()) 
    else:
        print(os.listdir(''.join(path_name)))

def rename_file(file_list):
    return os.rename(''.join(file_list[0]), ''.join(file_list[1]))

def about_file(file_name):
    print( os.stat(''.join(file_name)) )

def home_dir():
    return os.chdir(os.path.expanduser("~/Desktop"))

def cp(file_list):
    return shutil.copy(file_list[0], file_list[1])

def mv(file_list):
    return shutil.move(file_list[0], file_list[1])

def _help(command=None):
    pass

def create_file(name):
    file_name = ''.join(name)
    with open(f'{file_name}', 'w+'):
        pass

def remove_file(file_name):
    if os.path.exists(''.join(file_name)):
        return os.remove(''.join(file_name))
    print('file not found')

def read_file(file_name):
    file = ''.join(file_name)
    if os.path.exists(file):
        with open(file, 'r') as f:
            print(f.read())
    return 'file not found'

def write_file(file_method_text):
    if os.path.exists(file_method_text[0]):
        with open(file_method_text[0], file_method_text[1]) as f:
            f.write('\n' + file_method_text[2])
    else:
        return 'file not found'

def upload_git(link_comment_file):
    subprocess.run('git init', shell=True)
    subprocess.run(f'git add {link_comment_file[2]}', shell=True)
    subprocess.run(f"git commit -m {link_comment_file[1]}", shell=True)
    subprocess.run("git branch -M main", shell=True)
    subprocess.run(f"git remote add origin {link_comment_file[0]}", shell=True)
    subprocess.run("git push -u origin main", shell=True)

def re_upload_git(comment_file):
    subprocess.run(f'git add {comment_file[1]}', shell=True)
    subprocess.run(f"git commit -m  '{comment_file[0]}' ", shell=True)
    subprocess.run('git push -u origin main', shell=True)

def create_requirement_txt():
    subprocess.run('pip freeze > requirement.txt', shell=True)

os.chdir(os.path.expanduser("~/Desktop"))

while True:
    enter_command = input(f'{os.getcwd()} ').split(' | ')
    try:
        if enter_command == ['q']:
            break
        elif len(enter_command) == 1:
            eval(f"{enter_command[0]}()")
        else:
            eval(f"{enter_command[0]}({enter_command[1:]})")
    except:
        print('enter correct command')