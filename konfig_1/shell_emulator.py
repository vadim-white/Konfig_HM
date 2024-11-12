import os
import datetime
from zipfile import ZipFile
import argparse


class ShellEmulator:
    def __init__(self,user_name ="default",path_to_arxiv="./file_system.zip",path_to_script = ""):
        self.user_name = user_name
        self.path_to_arxiv = path_to_arxiv
        self.path_to_script = path_to_script
        self.virtual_sys_folder = ZipFile(path_to_arxiv, 'a')
        self.cwd = '/'
    def run_script(self,script_path):
        with open(script_path,'r') as script:
            for line in script:
                self.execute_command(line)
    def run(self):
        if(self.path_to_script != None and self.path_to_script[0:2] == "./"):
            self.run_script(self.path_to_script)
        try:
            while True:
                command = input(f"{self.user_name}@{self.cwd}> ")
                self.execute_command(command)
        except KeyboardInterrupt:
            self.exit()
    def execute_command(self, command):
        if not command:
            return

        commands = command.split()
        cmd = commands[0]
        args = commands[1:]

        if cmd == "ls":
            self.ls()
        elif cmd == "cd":
            self.cd(args)
        elif cmd == "exit":
            self.exit()
        elif cmd == "rmdir":
            self.rmdir(args)
        elif cmd == "date":
            self.date()
        elif cmd == "chown":
            self.chown(args)
        else:
            print(f"{cmd}: unknown command")

    def ls(self):
        list_of_paths = self.virtual_sys_folder.namelist()
        items = set()

        for path in list_of_paths:
            if path.startswith(self.cwd[1:]) and path != self.cwd[1:]:
                sub_path = path[len(self.cwd[1:]):].split('/')[0]
                items.add(sub_path)

        for item in sorted(items):
            print(item)

    def cd(self, args):
        if not args:
            return

        target = args[0]
        list_of_paths = self.virtual_sys_folder.namelist()

        if target == '/':
            self.cwd = '/'
        elif target == '..':
            if self.cwd == '/':
                return
            self.cwd = '/'.join(self.cwd.split('/')[:-2]) + '/'
            if self.cwd == '':
                self.cwd = '/'
        elif target == '.':
            return
        else:
            new_path = os.path.join(self.cwd[1:], target) + '/'
            if new_path in list_of_paths:
                self.cwd = '/' + new_path
            else:
                print("No such file or directory")

    def rmdir(self, args):
        if not args:
            print("Usage: rmdir <directory>")
            return

        target = args[0]
        full_path = os.path.join(self.cwd[1:], target) + '/'

        if full_path in self.virtual_sys_folder.namelist():
            # Симуляция удаления директории
            print(f"Directory '{target}' removed (simulated)")
        else:
            print("No such directory")

    def date(self):
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    def chown(self, args):
        if len(args) < 2:
            print("Usage: chown <user> <file>")
            return
        user, file = args
        print(f"Owner of '{file}' changed to '{user}' (simulated)")

    def exit(self):
        print("Bye!")
        self.virtual_sys_folder.close()
        exit(0)


def args_parser():
    parser = argparse.ArgumentParser(description="Эмулятор Shell")
    parser.add_argument("user_name",nargs="?",help="Имя пользователя",default="username")
    parser.add_argument("path_to_arxiv",nargs="?",help="Путь до виртуальной файлово системы",default="./file_system.zip")
    parser.add_argument("path_to_script",nargs="?",default=None)
    return parser.parse_args()

if __name__ == '__main__':
    args=args_parser()
    emulator = ShellEmulator(args.user_name,args.path_to_arxiv,args.path_to_script)
    emulator.run()