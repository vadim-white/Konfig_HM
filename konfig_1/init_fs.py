#init_fs.py
from zipfile import ZipFile
import os


def create_test_filesystem():
    # Создаем временные файлы и директории
    if not os.path.exists('temp'):
        os.makedirs('temp/test/dir1', exist_ok=True)


    # Создаем zip архив
    with ZipFile('file_system.zip', 'w') as zipf:
        # Добавляем директории (пустые файлы с / в конце)
        zipf.writestr('test/', '')
        zipf.writestr('test/dir1/', '')

    # Очищаем временные файлы
    for root, dirs, files in os.walk('temp', topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir('temp')


if __name__ == '__main__':
    create_test_filesystem()
    print("File system archive created successfully!")