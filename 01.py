import os
from Normalize import normalize
import zipfile, shutil

def normalize(text):
    return text

dict_file_extension = {'picure': ['JPEG', 'PNG', 'JPG', 'SVG'],
                       'video': ['AVI', 'MP4', 'MOV', 'MKV'],
                       'documents': ['DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'],
                       'music': ['MP3', 'OGG', 'WAV', 'AMR'],
                       'archives': ['ZIP', 'GZ', 'TAR']
                       }

list_type_data = []
list_data_extension = set()
list_unknown_extension = set()

def move_data(path_i, root_path, name_category):
    target_dir = os.path.join(root_path, name_category)
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)
    file_name = os.path.basename(path_i)
    file_name = os.path.splitext(file_name)[0]
    extension = path_i.split('.')[-1]
    file_move_name = target_dir +'\\' + normalize(file_name) + '.' + extension
    os.replace(path_i, file_move_name)
    extension = extension.upper()
    if extension in ('ZIP', 'GZ', 'TAR'):
        try:
            #shutil.unpack_archive(path_i, file_move_name)
            zip_path_i = zipfile.ZipFile(path_i)
            zip_path_i.extractall(target_dir.join(file_name))
            zip_path_i.close()
        except FileNotFoundError:
            print('archive is bad')
    
def sort_extension(path_i):
    extension = path_i.split('.')[-1]
    extension = extension.upper()
    for key, list_exts in dict_file_extension.items():
        if extension in list_exts:
            list_data_extension.add(extension)
            return key
       
    list_unknown_extension.add(extension)
    return list_data_extension, list_unknown_extension
    

def del_empty_data(path_i):
    os.rmdir(path_i)


def recursion_folder(root_path, sub_path=None):
    for i in os.listdir(sub_path if sub_path else root_path):
        path_i = os.path.join(sub_path if sub_path else root_path, i)
        if os.path.isdir(path_i):
            if not os.listdir(path_i):
                del_empty_data(path_i)
            else:
                recursion_folder(root_path, path_i)
        if os.path.isfile(path_i):      
            file_name = os.path.splitext(i)[0]          # получаем имя файла
            list_type_data.append(normalize(file_name))
            name_category = sort_extension(path_i)
            move_data(path_i, root_path, name_category)
            
    return list_type_data, list_data_extension, list_unknown_extension
    
print(recursion_folder('E:\\HOME_WORK - PYTHON\\ДЗ модуль №6\\Всякая всячина'))