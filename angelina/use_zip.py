import zipfile
import os
from angelina.supplementary_lib import create_new_dir

def preparation_zip(compression_list, name_archive, list_dir):
    '''
    Функция подготавливает данные для архивации и возвращает список созданных архивов.

    @param - compression_list: список значений методов сжатия.
    @type: list.

    @param - name_archive: имя создаваемого архива.
    @type: str.

    @param - list_dir: список данных, которые необходимо поместить в архив.
    @type: list.

    @value - zip_dict: словарь, где ключ - формат архива, а значение - метод сжатия.
    @type: dict.

    @value - zip_list: список созданных архивов.
    @type: list.

    @return - zip_list: список созданных архивов..
    @rtype: list.
    '''
    zip_dict = zip_processing(compression_list)
    zip_list = []
    for format_archiv, method_zip in zip_dict.items():
        name_archive += format_archiv
        create_zip(list_dir, name_archive, method_zip)
        zip_list.append(name_archive)
        name_archive = name_archive.replace(format_archiv, '') #очистка имени архива перед следующей итерацией.
    return zip_list

def zip_processing(compression_list):
    '''
    Функция подготавливает данные для правильного сжатия при создании архива.

    @param - compression_list: список значений методов сжатия.
    @type: list.

    @value - zip_dict: словарь, где ключ - формат архива, а значение - метод сжатия.
    @type: dict.

    @return - zip_dict: словарь, где ключ - формат архива, а значение - метод сжатия.
    @rtype: dict.
    '''
    zip_dict = {}
    if len(compression_list) == 0:
        zip_dict['.zip'] = zipfile.ZIP_STORED
    else:
        for i in compression_list:
            if i == 'xz':
                zip_dict['_xz.zip'] = zipfile.ZIP_LZMA
            elif i == 'gz':
                zip_dict['_gz.zip'] = zipfile.ZIP_DEFLATED
            elif i == 'bz2':
                zip_dict['_bz2.zip'] = zipfile.ZIP_BZIP2

    return zip_dict

def create_zip(list_dir, name_zipfile, method_zip):
    '''
    Функция создаёт архив.

    @param - list_dir: список данных, которые необходимо поместить в архив.
    @type: list.

    @param - name_zipfile: имя создаваемого архива.
    @type: str.

    @param - method_zip: метод сжатия.
    @type: int.

    @value - myzip: модуль https://docs.python.org/3.5/library/zipfile.html.
    @type: zipfile.ZipFile
    '''
    myzip = zipfile.ZipFile(name_zipfile,'w', method_zip)
    write_zip(myzip, list_dir, name_zipfile) #вызываем функцию непосредственной записи данных.
    myzip.close()

def add_zip(list_dir, name_archive):
    '''
    Функция проверяет архив и добавляет данные.

    @param - list_dir: список данных, которые необходимо поместить в архив.
    @type: list.

    @param - name_archive: имя архива.
    @type: str

    @value - myzip: модуль https://docs.python.org/3.5/library/zipfile.html.
    @type: zipfile.ZipFile
    '''
    res = change_zip(name_archive)
    if res:
        myzip = zipfile.ZipFile(name_archive,'a')
        write_zip(myzip, list_dir, name_archive) #вызываем функцию непосредственной записи данных.
        myzip.close()
        print('\nДанные успешно добавлены к архиву {0}!'.format(name_archive))
    else:
        print('Сожалеем, архив с именем {0} не удалось прочесть!'.format(name_archive))

def write_zip(myzip, list_dir, name_archive):
    '''
    Функция записи данных в архив.

    @param - list_dir: список данных, которые необходимо поместить в архив.
    @type: list.

    @param - myzip: модуль https://docs.python.org/3.5/library/zipfile.html.
    @type: zipfile.ZipFile
    '''
    current_dir = os.getcwd() #Сохраняем путь к текущей директории.
    name_zip = os.path.basename(name_archive)
    for i in list_dir:
        os.chdir(os.path.dirname(i)) #Переходим в директорию, в которой находятся данные для записи.
        i = os.path.basename(i) #Получаем имя, отсекаем путь.
        if os.path.isdir(i): #Если директория.
            for dirname, subdirs, files in os.walk(i):
                myzip.write(dirname)
                for filename in files:
                    if name_zip == filename:
                        print('\nФайл {0} нельзя поместить в архив. Действие приведёт к бесконечному циклу!'.format(name_zip))
                    else:
                        myzip.write(os.path.join(dirname, filename))
        elif os.path.isfile(i): #Если файл.
            myzip.write(i)
        os.chdir(current_dir) #Возращаемся в директрию запуска скрипта.

def preparation_zip_extract(name_archive, name_dir):
    '''
    Функция проверяет и подготавливает архив к извлечению данных.

    @param - name_archive: имя архива.
    @type: str

    @param - name_dir: имя директории в которую будут извлечены данные.
    @type: str

    @value - new_dir: имя созданной директории, после проверки функцией create_new_dir(),
    в которую будут извлечены данные.
    @type: str
    '''
    res = change_zip(name_archive) #проверяем архив на возможность чтения.
    if res:
        new_dir = create_new_dir(name_dir) #создаём новую директорию.
        extract_zip(name_archive, new_dir)
        print('\nДанные из архива {0} успешно извлечены, в директорию {1}!'.format(name_archive, new_dir))
    else:
        print('Сожалеем, архив с именем {0} не удалось прочесть!'.format(name_archive))

def extract_zip(name_zipfile, new_dir):
    '''
    Функция извлекает данные из архива.

    @param - name_zipfile: имя архива.
    @type: str

    @param - new_dir: имя директории в которую будут извлечены данные.
    @type: str
    '''
    with zipfile.ZipFile(name_zipfile) as z:
        z.extractall(new_dir)
    #print(os.listdir(new_dir))

def change_zip(archive):
    '''
    Функция проверяет архив на возможность чтения данных.

    @param - archive: имя архива.
    @type: str
    '''
    return zipfile.is_zipfile(archive)
