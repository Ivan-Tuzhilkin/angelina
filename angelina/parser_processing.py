import os
import angelina.use_zip as z
import angelina.use_tar as t
import angelina.software_help as sh

'''Модуль предназначен для передачи полученных данных в соответствующие модули.'''

def parser_processing(user_dict):
    '''
    Функция обрабатывает словарь возвращённый функцией create_parser() из модуля parser и
    запускает соответствуюие функции для обработки каждого из ключей словаря user_dict.

    @value - user_dict: принимает словарь возвращённый функцией create_parser() из модуля parser.
    @type: dict
    '''
    #print(user_dict)

    if ('-tar' in user_dict) or ('-zip' in user_dict):
        tar_zip_processing(user_dict)
    elif '-a' in user_dict:
        add_processing(user_dict.get('-a'), user_dict.get('-f'))
    elif '-e' in user_dict:
        extract_processing(user_dict.get('-e'), user_dict.get('-n'))
    else:
        sh.help_processing(user_dict)

def tar_zip_processing(user_dict):
    '''
    Функция подготавливает первичные данные для архивации, передаёт их в специализированные
    функции и получает от них даныые на основе которых генерирует информацию об успехе архивации.

    @param - user_dict: принимает словарь из функции parser_processing().
    @type: dict

    @value - list_dir: список данных, которые необходимо поместить в архив.
    @type: list

    @value - name_archive: имя создаваемого архива.
    @type: str

    @value - archiv_list: список созданных архивов, возвращённый соответствующиими функциями.
    @type: list

    @value - current_dir: имя директории в которой запущена программа.
    @type: str
    '''
    list_dir = user_dict.get('-f')
    current_dir = os.getcwd()
    name_archive = os.path.join(current_dir, user_dict.get('-n'))
    archiv_list = []

    for key, value in user_dict.items():
        if key == '-tar':
            archiv_list.extend(t.preparation_tar(value, name_archive, list_dir)) #расширяем список.
        if key == '-zip':
            archiv_list.extend(z.preparation_zip(value, name_archive, list_dir))

    for name in archiv_list:
        size = os.path.getsize(os.path.join(current_dir, name))
        print('\nАрхив с именем {0} создан в директоррии {1}, размер архива {2} байт.'
              .format(os.path.basename(name), current_dir, size))

def extract_processing(list_archive, list_names):
    '''
    Функция извлекает данные из архива.

    @param - list_archive: принимает список архивов для распаковки из функции parser_processing().
    @type: list

    @param - list_names: принимает список имён для создания директорий, в которые
    будут распакованы данные из функции parser_processing().
    @type: list

    @value - dir_name: имя директории в которую будет произведена распаковка данных.
    @type: str
    '''
    i = 0 #Счётчик.
    for name in list_archive:
        #name = os.path.basename(name)
        dir_name = list_names[i]
        if os.path.basename(name).find('tar') != -1:
            t.preparation_tar_extract(name, dir_name)
        elif os.path.basename(name).find('zip') != -1:
            z.preparation_zip_extract(name, dir_name)
        else:
            print('Архив с именем {0} не поддерживается!'.format(name))
        i += 1

def add_processing(list_archive, list_dir):
    '''
    Функция добавляет данные к существующему архиву.

    @param - list_archive: принимает список архивов, для добавления в них данных, из функции parser_processing().
    @type: list

    @param - list_dir:  список данных, которые необходимо поместить в архив из функции parser_processing().
    @type: list
    '''
    for name in list_archive:
        if os.path.basename(name).find('tar') != -1: #Отсекаем путь, ищем только в имене файла.
            if 'tar.' in name:
                print('Добавление данных к сжатому tar архиву не поддерживается!')
            else:
                t.add_tar(list_dir, name)
        elif os.path.basename(name).find('zip') != -1:
            z.add_zip(list_dir, name)
        else:
            print('Архив с именем {0} не поддерживается!'.format(name))
