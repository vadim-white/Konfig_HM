import sys
from zipfile import ZipFile
import argparse
from datetime import datetime
import os


class ShellEmulator:
    def __init__(self, user_name, path_to_arxiv, path_to_script=None):
        self.user_name = user_name
        self.path_to_arxiv = path_to_arxiv
        self.path_to_script = path_to_script
        self.cwd = '/'
        self.virtual_sys_folder = ZipFile(path_to_arxiv, 'a')
        self.file_owners = {}  # Инициализируем словарь для хранения владельцев файлов

        # Инициализируем владельцев для всех существующих файлов и директорий
        for path in self.virtual_sys_folder.namelist():
            self.file_owners[path] = self.user_name

    def run_script(self, script_path):
        with open(script_path, 'r') as script:
            for line in script:
                self.execute_command(line.strip())

    def execute_command(self, command):
        if not command:
            return
        commands = command.split()
        cmd = commands[0]
        args = commands[1:]

        commands_map = {
            'cd': self.cd,
            'ls': self.ls,
            'exit': self.exit,
            'rmdir': self.rmdir,
            'date': self.date,
            'chown': self.chown
        }

        if cmd in commands_map:
            commands_map[cmd](args)
        else:
            print(f"{cmd}: unknown command")

    def cd(self, args):
        if not args:
            self.cwd = '/'
            return

        target = args[0]
        list_of_paths = self.virtual_sys_folder.namelist()

        if target == '/':
            self.cwd = '/'
        elif target == '..':
            if self.cwd == '/':
                return
            self.cwd = '/'.join(self.cwd.split('/')[:-2]) + '/'
        elif target == '.':
            return
        elif self.cwd[1:] + target + '/' in list_of_paths:
            self.cwd += target + '/'
        elif target[1:] + '/' in list_of_paths:
            self.cwd = target + '/'
        else:
            print("No such file or directory")

    def ls(self, args):
        if len(args) == 1:
            prev_cwd = self.cwd
            self.cd([args[0]])
            self.ls([])
            self.cwd = prev_cwd
        elif len(args) == 0:
            list_of_paths = self.virtual_sys_folder.namelist()
            current_dir_items = set()

            for path in list_of_paths:
                if path.startswith(self.cwd[1:] if self.cwd != '/' else ''):

                    relative_path = path[len(self.cwd[1:] if self.cwd != '/' else ''):]

                    first_component = relative_path.split('/')[0]

                    if first_component:
                        current_dir_items.add(first_component)

            for item in sorted(current_dir_items):
                print(item)
        else:
            print("Error: wrong option/s")

    def rmdir(self, args):
        if not args:
            print("rmdir: missing operand")
            return

        dir_name = args[0]
        full_path = (self.cwd[1:] + dir_name + '/') if self.cwd != '/' else (dir_name + '/')

        if full_path not in self.virtual_sys_folder.namelist():
            print(f"rmdir: failed to remove '{dir_name}': No such file or directory")
            return

        for path in self.virtual_sys_folder.namelist():
            if path.startswith(full_path) and path != full_path:
                print(f"rmdir: failed to remove '{dir_name}': Directory not empty")
                return

        new_zip = ZipFile(self.path_to_arxiv + '.temp', 'w')
        for item in self.virtual_sys_folder.namelist():
            if item != full_path:
                new_zip.writestr(item, self.virtual_sys_folder.read(item))

        self.virtual_sys_folder.close()
        new_zip.close()

        os.replace(self.path_to_arxiv + '.temp', self.path_to_arxiv)
        self.virtual_sys_folder = ZipFile(self.path_to_arxiv, 'a')

    def date(self, args):
        current_time = datetime.now()
        if not args:
            print(current_time.strftime("%a %b %d %H:%M:%S %Y"))
        elif args[0] == "+%Y":
            print(current_time.strftime("%Y"))
        elif args[0] == "+%m":
            print(current_time.strftime("%m"))
        elif args[0] == "+%d":
            print(current_time.strftime("%d"))
        else:
            print("date: invalid date format")

    def chown(self, args):
        if len(args) < 2:
            print("chown: missing operand")
            return

        owner = args[0]
        path = args[1]

        # Формируем полный путь
        full_path = (self.cwd[1:] + path + '/') if self.cwd != '/' else (path + '/')

        # Убираем лишние слеши
        full_path = full_path.replace('//', '/')

        if full_path not in self.virtual_sys_folder.namelist():
            print(f"chown: cannot access '{path}': No such file or directory")
            return

        self.file_owners[full_path] = owner
        print(f"Changed owner of '{path}' to {owner}")
    def exit(self, args=None):
        print("Bye!")
        self.virtual_sys_folder.close()
        sys.exit(0)

    def run(self):
        if self.path_to_script and self.path_to_script.startswith("./"):
            self.run_script(self.path_to_script)
        try:
            while True:
                command = input(f"{self.user_name}@{self.cwd}> ")
                self.execute_command(command)
        except KeyboardInterrupt:
            self.exit()


def args_parser():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("user_name", nargs="?", help="Username", default="username")
    parser.add_argument("path_to_arxiv", nargs="?", help="Path to virtual file system", default="./file_system.zip")
    parser.add_argument("path_to_script", nargs="?", default=None)
    return parser.parse_args()


if __name__ == '__main__':
    args = args_parser()
    emulator = ShellEmulator(args.user_name, args.path_to_arxiv, args.path_to_script)
    emulator.run()