from os import mkdir

'''Модуль с дополнительными функциями'''

def create_new_dir(name_dir):
    '''
    Функция проверяет есть ли в текущей директории папка с таким именем,
    если есть задаём другое имя, если нет создаём папку.

    @param - name_archive: имя архива.
    @type: str
    '''
    #new_dir = name_dir[:name_dir.find('.')]
    while True:
        try:
            mkdir(name_dir)
        except OSError as ex:
            #print('Ошибка {0}'.format(ex))
            name_dir = input('Задайте имя директории, в неё будут распакованы данные: ')
        finally:
            break
    return name_dir
