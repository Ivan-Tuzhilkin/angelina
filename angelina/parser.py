import datetime
import os
import sys

'''Модуль предназначен для приёма пользовательских данных и их первичной обработки.'''

def create_parser():
    '''
    Функция создаёт список аргументов командной строки с помощью метода sys.argv,
    затем возвращает словарь полученный из списка аргументов командной строки,
    с помощью функции change_arg_list()

    @value - arg_list: принимает список аргументов командной строки.
    @type: list

    @value - user_dict: словарь - ключ: значение, полученный после проверки списка
    аргументов командной строки функцией change_arg_list(), а затем дополненный необходимыми
    ключами и значениями, с помощью функции add_necessery_keys_val().
    @type: dict

    @return: возвращает словарь user_dict с проверенный на наличие ошибки бесконечного цикла
    функцией remove_endless_cycle()
    @rtype: dict
    '''
    arg_list = sys.argv[1:] #Удаляем первый элемент списка - путь к скрипту запуска программы.
    user_dict = change_arg_list(arg_list)
    user_dict = add_necessery_keys_val(user_dict)
    return remove_endless_cycle(user_dict)

def change_arg_list(arg_list):
    '''
    Функция проверяет полученный список аргументов командной строки на корректность
    введённых значений и создаёт словарь сортируя ключи и значения.

    @param - arg_list:  список аргументов командной строки.
    @type: list

    @value - permissible_keys: список поддерживаемых программой ключей.
    @type: list

    @return - user_dict: словарь - ключ: значение, получаемый после проверки данных.
    @rtype: dict
    '''

    permissible_keys = ['-a', '-h', '-zip', '-tar', '-f', '-e', '-v', '-l', '-n']
    user_dict = {}

    for i in arg_list:
        if i[0] == '-': #Определяем ключ ли это.
            if i in permissible_keys:
                user_dict[i] = [] #Добавляем ключ в словарь.
                param = i #Сохраняем текущий кчюч.
            else:
                print('Ключевой аргумент со значением {0} не поддерживается!'.format(i))
        else: #Значит это значение ключа.
            if (param == '-tar') or (param == '-zip'):
                exec(is_compression(i)) #Проверяем значение метода сжатия.
            elif (param == '-f') or (param == '-e') or (param == '-a'):
                if i[-1] == '/': # Удаляем символ '/' с конца строки, необходимо для корректного формирования абсолютного пути.
                    i = i[:-1]
                exec(is_file(i)) #Проверям существует ли данный файл, архив или директория.
            else:
                user_dict[param] += [i] #Добавляем значение к ключу.

    return user_dict

def add_necessery_keys_val(user_dict):
    '''
    Функция проверяет наличие в словаре user_dict необходимых ключей и значений,
    если их нет они будут созданы.

    @param - user_dict: словарь - ключ: значение, полученный из функции create_parser().
    @type: dict.

    @return - user_dict: после проверки.
    @rtype: dict.
    '''
    #Проверяем при наличии ключа наличие значений.
    if ('-a' in  user_dict) and (user_dict.get('-a') == []):
        user_dict = get_path_list('-a', user_dict)
    if ('-e' in  user_dict) and (user_dict.get('-e') == []):
        user_dict = get_path_list('-e', user_dict)
    if ('-f' in  user_dict) and (user_dict.get('-f') == []):
        user_dict = get_path_list('-f', user_dict)

    #При создании архива ключи '-f', '-n' обязателены.
    if ('-tar' in user_dict) or ('-zip' in user_dict):
        if '-f' not in user_dict:
            user_dict['-f'] = []
            user_dict = get_path_list('-f', user_dict)
        if '-n' not in user_dict: #Значением будет текущая дата в isoformat.
            user_dict['-n'] = datetime.datetime.now().isoformat()
        else:
            user_dict['-n'] = user_dict.get('-n')[0]

    #При добавлении к архиву ключ '-f' обязателен.
    if ('-f' not in user_dict) and ('-a' in user_dict):
        user_dict['-f'] = []
        user_dict = get_path_list('-f', user_dict)

    #При извлечении данных ключ '-n' обязателен.
    if '-e' in user_dict:
        if '-n' not in user_dict: #Пример: user_dict.get('-e') == 'ang.tar' --> 'ang_tar'
            user_dict['-n'] = [os.path.basename(i).replace('.','_') for i in user_dict.get('-e')]
        else: #Пример: user_dict.get('-e') == 'spam.tar', user_dict.get('-n') == 'ang' --> 'ang_tar'
            user_dict['-n'] = [user_dict.get('-n')[0] + '_' + os.path.splitext(i)[1][1:] for i in user_dict.get('-e')]

    return user_dict

def remove_endless_cycle(user_dict):
    '''
    Функция удаляет(частично) дублирование данных,
    которое может привести к попаданию программы в бесконечный цикл,
    остальная часть защиты от попадания в бесконечный цикл реализована в
    соответствующих модулях.

    @param - user_dict: словарь - ключ: значение, полученный из функции create_parser().
    @type: dict.

    @return - user_dict: после проверки.
    @rtype: dict.
    '''
    while True:
        if '-a' in user_dict:
            for i in user_dict.get('-a'):
                if i in user_dict.get('-f'): #Если значения ключей совпадают.
                    print('Вы не можите добавлять к текущему архиву, этот же архив!')
                    user_dict.get('-f').remove(i) #Удаляем совпадение.
                    user_dict = get_path_list('-f', user_dict)
                else:
                    return user_dict
                    break
        else:
            return user_dict
            break

def is_compression(value):
    '''
    Функция проверяет является ли значение поддерживаемым методом сжатия.

    @param - value: значение.
    @type: str

    @value - permissible_values: список поддерживаемых методов сжатия.
    @type: list

    @return: исполняемый код.
    @rtype: str
    '''
    permissible_values = ['xz', 'gz', 'bz2']

    if value in permissible_values:
        return 'user_dict[param] += [i]'
    else:
        return "print('Значение {0} не поддерживается!'.format(i))"

def is_file(value):
    '''
    Функция проверяет существует ли данный файл, архив или директория.

    @param - value: значение.
    @type: str

    @return: исполняемый код.
    @rtype: str
    '''
    if os.path.exists(value) == True: #Если путь существует.
        if value in os.listdir(os.getcwd()): #Если файл/папка в текущей директории, то создаём абсолютный путь.
            return "user_dict[param] += [os.getcwd() + '/' + i]"
        else:
            return 'user_dict[param] += [i]'
    else:
        if value in os.listdir('/home/' + os.getlogin()): #Если файл/папка в домашней директории, то создаём абсолютный путь.
            return "user_dict[param] += ['/home/' + os.getlogin() + '/' + i]"
        else:
            return "print('Файла с таким путём {0} не существует!'.format(i))"

def get_path_list(param, user_dict):
    '''
    Функция получает список путей к файлам, архивам, директорияg.

    @param - param: ключь словаря.
    @type: str

    @param - user_dict: словарь - ключ: значение, получаемый после проверки данных.
    @type: dict

    @value - input_text: текст для отображения функцией input()
    @type: str

    @value - path_user_list: введённый пользователем список путей к файлам, архивам, директориям.
    @type: list

    @return: исполняемый код.
    @rtype: str
    '''
    if param == ('-a' or '-e'):
        input_text = 'Введите имя архива или архивов через пробел: '
    elif param == '-f':
        input_text = '''Введите через пробел пути относительно корневой директории к папкам,
                      \rиз которых необходимо создать резервную копию: '''
    while True:
        path_user_list = [str(i) for i in input(input_text).split()]

        for i in path_user_list:
            if i[-1] == '/': # Удаляем символ '/' с конца строки, необходимо для корректного формирования абсолютного пути.
                i = i[:-1]
            exec(is_file(i)) #Проверям существует ли данный файл, архив или директория.

        print('\n Вы ввели следующие пути: ')
        for i in user_dict.get(param):
            print(' ' * 4, i, end='\n')

        check = input('\n Подтвердите корректность введя yes или no: ')
        if check == 'yes':
            break
        else:
            user_dict[param] = []

    return user_dict
