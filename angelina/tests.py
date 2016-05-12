import os
import angelina.parser as parser
from angelina.parser_processing import parser_processing

'''
Модуль предназначен для тестирования программы.

Запуск тестирования:
1. Как скрипт(перед исполнением добавьте первой строкой - #!/usr/bin/env python3 ):
./angelina/tests.py >> res.txt 
2. Как пакет Python:
angelina-test >> res.txt

Результаты тестирования смотрим в файле res.txt в текущей директории
и в папке test_dir/.
'''

def create_test_space():
    '''
    Функция создаёт тестовое пространство в текущей директории.
    Папка test_dir/, в ней четыре папки, в каждой из них файл text.txt.
    Также внутри запускается функция test().

    @value - list_dir: список путей.
    @type: list

    @value - current_dir: текущаяя директория.
    @type: str
    '''
    list_dir = ['/data1', '/data2', '/data3', '/data4']
    for i in list_dir:
        os.makedirs('test_dir' + i)
        with open('test_dir' + i + '/text.txt', 'w') as f:
            f.write('text\n' * 100)

    current_dir = os.getcwd()
    os.chdir('test_dir')
    test() #Запускаем тест.
    os.chdir(current_dir)

def test():
    '''
    Функция передает в программу тестовые данные.

    @value - test_list: список тестовых данных.
    @type: list

    @value - user_dict: принимает словарь преобразованные из test_list[i].
    @type: dict
    '''
    test_list = [['-tar', 'xz', 'gz', 'bz2', '-zip', 'xz', 'gz', 'bz2', '-f', 'data1', 'data2','-n' , 'test_archive'],
                ['-tar', '-zip', '-f', 'data3', 'data4', '-n' , 'test_archive'],
                ['-a', 'test_archive.zip', 'test_archive.tar', '-f', 'data1', 'data2'],
                ['-a', 'test_archive_xz.zip', 'test_archive_gz.zip', 'test_archive_bz2.zip', '-f', 'data3', 'data4'],
                ['-e', 'test_archive.zip', 'test_archive.tar'],
                ['-e', 'test_archive_xz.zip', 'test_archive.tar.xz', 'test_archive.tar.gz', 'test_archive.tar.bz2', '-n', 'extract']]

    k = 1 #Счётчик.
    for i in test_list:
        print('\nTEST{0}\n'.format(k))
        arg_list = i
        user_dict = parser.change_arg_list(arg_list)
        user_dict = parser.add_necessery_keys_val(user_dict)
        user_dict = parser.remove_endless_cycle(user_dict)
        print(user_dict)
        parser_processing(user_dict)
        k += 1

