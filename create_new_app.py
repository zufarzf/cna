import os
from  jinja2 import Environment, FileSystemLoader
# ===============================================


def default_app_path(dir_name):
    app_dir = None
    alphabet = [
                'a', 'b', 'c', 'd', 'e', 'f', 'g',
                'h', 'i', 'j', 'k', 'l', 'm', 'n',
                'o', 'p', 'q', 'r', 's', 't', 'u',
                'v', 'w', 'x', 'y', 'z'
                ]
    # ----------------------------
    for letter in alphabet:
        if str(dir_name).lower().replace('\\', '/').replace(' ', '').startswith( f'{letter}:' ): app_dir = dir_name
        # ----------------------------
    if app_dir == None:
        # ----------------------------------------------------------------------------
        if os.path.exists(f'C:\\Users\\{pc_user_name}\\OneDrive\\Desktop'):
            app_dir = f'C:/Users/{pc_user_name}/OneDrive/Desktop/{dir_name}'
        # ----------------------------------------------------------------------------
        elif os.path.exists(f'C:\\Users\\{pc_user_name}\\OneDrive\\Рабочий стол'):
            app_dir = f'C:/Users/{pc_user_name}/OneDrive/Рабочий стол/{dir_name}'
        # ----------------------------------------------------------------------------
        elif os.path.exists(f'C:\\Users\\{pc_user_name}\\Рабочий стол'):
            app_dir = f'C:/Users/{pc_user_name}/Рабочий стол/{dir_name}'
        # ----------------------------------------------------------------------------
        elif os.path.exists(f'C:\\Users\\{pc_user_name}\\Desktop'):
            app_dir = f'C:/Users/{pc_user_name}/Desktop/{dir_name}'
    # ----------------------------------------------------------------------------
    if os.path.exists(app_dir): return None
    else: return f'{app_dir}'
# ----------------------




def clear_name(name):
    el_list = [
        '!', ' ', '"', '#', '$', '%', '&\\', "'", '(', ')', '*',
        '+', ',','-', '.', '/', ':', ';', '<', '=', '>', '?',
        '@', '[', '\\', ']', ',' , '_', '`', '{', '|', '}', '~',
        '\t', '\n', '\r', '\x0b', '\x0c', '^'
    ]

    name_dict = {1: name}
    dict_keys = []
    for i in el_list:
        for key in name_dict:
            dict_keys.append(key)
        if i in name_dict[dict_keys[-1]]: name_dict[dict_keys[-1] + 1] = name_dict[dict_keys[-1]].replace(i, '')
    result = name_dict[dict_keys[-1]]
    dict_keys.clear()
    name_dict.clear()
    return result












while 1:
    apps_name = []
    dir_name = None
    all_good = True
    pc_user_name = os.getlogin()

    while 1:
        print('\n###############################################\n')
        dir_name = input('(Q)uit | (R)estart || dir name --> ')
        dir_name = clear_name(dir_name)
        app_dir = None

        if dir_name.lower() == 'q': exit()
        elif dir_name.lower() == 'r': all_good = False; apps_name.clear(); break
        elif default_app_path(dir_name) == None: print('\nПапка с таким именем уже существует!')
        else: app_dir = default_app_path(dir_name); break



    if all_good:
        while 1:
            print('\n###############################################\n')
            app_name = input('(Q)uit | (R)estart | (C)reate || app name --> ')
            if app_name.lower() == 'c': break
            elif app_name.lower() == 'r': all_good = False; apps_name.clear(); break
            elif app_name.lower() == 'q': exit()
            else: 
                app_name = clear_name(app_name)
                apps_name.append(app_name)


    if all_good:
        root_dir = f'{app_dir}/app'
        os.makedirs(root_dir)

        for app in apps_name:
            os.mkdir(root_dir + '/' + app)
            os.mkdir(root_dir + '/' + f'{app}/{app}-templates')
            os.mkdir(root_dir + '/' + f'{app}/{app}-static')
            os.mkdir(root_dir + '/' + f'{app}/{app}-static/CSS')
            os.mkdir(root_dir + '/' + f'{app}/{app}-static/JS')
            os.mkdir(root_dir + '/' + f'{app}/{app}-static/images')


        enviroment = Environment(loader=FileSystemLoader("templates/"))


        # run
        # ===============================================================
        template__run = enviroment.get_template('run.txt').render()
        with open(f'{app_dir}/run.py', 'w') as f: f.write(template__run)
        # ===============================================================

        # config
        # ===============================================================
        key = os.urandom(30).hex()

        template__config = enviroment.get_template('config.txt').render(secret_key=key)
        with open(f'{app_dir}/config.py', 'w') as f: f.write(template__config)
        # ===============================================================


        # ###############################################################
        # ###############################################################


        # root __init__
        # ===============================================================
        template__root_init = enviroment.get_template('root__init.txt')
        root_init = template__root_init.render(import_app=apps_name)
        with open(f'{root_dir}/__init__.py', 'w') as f: f.write(root_init)
        # ===============================================================


        # ###############################################################
        # ###############################################################


        # __init__
        # ===============================================================
        template__init = enviroment.get_template('init.txt')

        for file_name in apps_name:
            init = template__init.render(app_name=file_name)
            with open(f'{root_dir}/{file_name}/__init__.py', 'w') as f: f.write(init)
        # ===============================================================


        # db models
        # ===============================================================
        template__db_models = enviroment.get_template('db_models.txt')
        
        for file_name in apps_name:
            db_models = template__db_models.render(app_name=file_name)
            with open(f'{root_dir}/{file_name}/db_models.py', 'w') as f: f.write(db_models)
        # ===============================================================


        # views
        # ===============================================================
        template__views = enviroment.get_template('views.txt')

        for file_name in apps_name:
            views = template__views.render(app_name=file_name)
            with open(f'{root_dir}/{file_name}/views.py', 'w') as f: f.write(views)
        # ===============================================================

        # forms
        # ===============================================================
        template__forms = enviroment.get_template('forms.txt')

        for file_name in apps_name:
            forms = template__forms.render()
            with open(f'{root_dir}/{file_name}/forms.py', 'w') as f: f.write(forms)
        # ===============================================================


        # HTML
        # ===============================================================
        template__html = enviroment.get_template('main.html')

        for file_name in apps_name:
            html = template__html.render()
            with open(f'{root_dir}/{file_name}/{file_name}-templates/main.html', 'w') as f: f.write(html)
        # ===============================================================


        # ###############################################################
        # ###############################################################





        # os.system(f'python -m venv {app_dir}/venv')
        with open(f'{app_dir}/pip_lib_list.txt', 'w') as f:
            f.write(
                'python -m venv venv\nvenv\\scripts\\activate\npip install flask flask-sqlalchemy flask-migrate flask-wtf flask-moment flask-socketio pymysql')

        dir_name_end = dir_name.split('\\')

        print(f'Приложение {dir_name_end[-1]} Успешно создан!')
        
        while 1:
            new_app = input(f'Хотите создать ещё одно приложение? (Y)es/(N)o --> ')
            if new_app.lower() == 'yes' or new_app.lower() == 'y': apps_name.clear(); break
            elif new_app.lower() == 'no' or new_app.lower() == 'n': exit()

