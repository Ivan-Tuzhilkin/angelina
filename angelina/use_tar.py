import tarfile
import os
from angelina.supplementary_lib import create_new_dir

name_arc = '' # Переменная используется функцией exclude_file().

def preparation_tar(compression_list, name_archive, list_dir):
    '''
    Функция подготавливает данные для архивации и возвращает список созданных архивов.

    @param - compression_list: список значений методов сжатия.
    @type: list.

    @param - name_archive: имя создаваемого архива.
    @type: str.

    @param - list_dir: список данных, которые необходимо поместить в архив.
    @type: list.

    @value - tar_dict: словарь, где ключ - формат архива, а значение - метод сжатия.
    @type: dict.

    @value - tar_list: список созданных архивов.
    @type: list.

    @return - tar_list: список созданных архивов..
    @rtype: list.
    '''
    tar_dict = tar_processing(compression_list)
    tar_list = []
    for format_archiv, mode_tar in tar_dict.items():
        name_archive += format_archiv
        global name_arc # Переменная используется функцией exclude_file().
        name_arc = os.path.basename(name_archive)
        create_tar(list_dir, name_archive, mode_tar)
        tar_list.append(name_archive)
        name_archive = name_archive.replace(format_archiv, '') #очистка имени архива перед следующей итерацией.
    return tar_list

def tar_processing(compression_list):
    '''
    Функция подготавливает данные для правильного сжатия при создании архива.

    @param - compression_list: список значений методов сжатия.
    @type: list.

    @value - tar_dict: словарь, где ключ - формат архива, а значение - метод сжатия.
    @type: dict.

    @return - tar_dict: словарь, где ключ - формат архива, а значение - метод сжатия.
    @rtype: dict.
    '''
    tar_dict = {}
    if len(compression_list) == 0:
        tar_dict['.tar'] = 'w'
    else:
        for i in compression_list:
            if i == 'xz':
                tar_dict['.tar.xz'] = 'w:xz'
            elif i == 'gz':
                tar_dict['.tar.gz'] = 'w:gz'
            elif i == 'bz2':
                tar_dict['.tar.bz2'] = 'w:bz2'

    return tar_dict

def create_tar(list_dir, name_tarfile, mode_tar):
    '''
    Функция создаёт архив.

    @param - list_dir: список данных, которые необходимо поместить в архив.
    @type: list.

    @param - name_tarfile: имя создаваемого архива.
    @type: str.

    @param - mode_tar: метод сжатия.
    @type: str.
    '''
    with tarfile.open(name_tarfile, mode_tar) as tar:
        current_dir = os.getcwd()
        for i in list_dir:
            os.chdir(os.path.dirname(i))
            i = os.path.basename(i)
            tar.add(i, exclude = exclude_file) #exclude_file() - функция исключения файла.
            os.chdir(current_dir)

def exclude_file(filename):
    '''
    Функция исключает созданный архив из потока записи с целью недопущения
    входа программы в бесконечный цикл.

    @param - filename: имя файла, который необходимо поместить в архив.
    @type: str.
    '''
    if name_arc == os.path.basename(filename):
        print('\nФайл {0} нельзя поместить в архив. Действие приведёт к бесконечному циклу!'.format(name_arc))
        return True
    else:
        return False

def add_tar(list_dir, name_archive):
    '''
    Функция проверяет архив и добавляет данные.

    @param - list_dir: список данных, которые необходимо поместить в архив.
    @type: list.

    @param - name_archive: имя архива.
    @type: str
    '''
    res = change_tar(name_archive)
    if res:
        mode_tar = 'a'
        create_tar(list_dir, name_archive, mode_tar) #Добавляем данные к архиву
        print('\nДанные успешно добавлены к архиву {0}!'.format(name_archive))
    else:
        print('Сожалеем, архив с именем {0} не удалось прочесть!'.format(name_archive))

def preparation_tar_extract(name_archive, name_dir):
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
    res = change_tar(name_archive) #проверяем архив на возможность чтения.
    if res:
        new_dir = create_new_dir(name_dir) #создаём новую директорию.
        extract_tar(name_archive, new_dir)
        print('\nДанные из архива {0} успешно извлечены, в директорию {1}!'.format(name_archive, new_dir))
    else:
        print('Сожалеем, архив с именем {0} не удалось прочесть!'.format(name_archive))

def extract_tar(name_tarfile, new_dir):
    '''
    Функция извлекает данные из архива.

    @param - name_tarfile: имя архива.
    @type: str

    @param - new_dir: имя директории в которую будут извлечены данные.
    @type: str
    '''
    with tarfile.open(name_tarfile) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, new_dir)

def change_tar(archive):
    '''
    Функция проверяет архив на возможность чтения данных.

    @param - archive: имя архива.
    @type: str
    '''
    return tarfile.is_tarfile(archive)
