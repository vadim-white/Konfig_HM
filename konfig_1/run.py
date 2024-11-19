#run.py
import os
import subprocess
import sys

def main():
    # Получаем путь к текущему интерпретатору Python
    python_executable = sys.executable

    # 1. Создаем файловую систему
    print("Creating file system...")
    subprocess.run([python_executable, 'init_fs.py'])

if __name__ == '__main__':
    main()