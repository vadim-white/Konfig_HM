# test_emulator.py
import unittest
from zipfile import ZipFile
import os
from datetime import datetime
from emulator import ShellEmulator

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        """Создаем тестовое окружение перед каждым тестом"""
        self.test_zip = "test_fs.zip"
        # Создаем тестовую файловую систему
        with ZipFile(self.test_zip, 'w') as zf:
            zf.writestr('test/', '')
            zf.writestr('test/dir1/', '')
            zf.writestr('test/dir1/file1.txt', 'content1')
            zf.writestr('test/dir1/file2.txt', 'content2')
            zf.writestr('empty_dir/', '')

        self.emulator = ShellEmulator("test_user", self.test_zip)

    def tearDown(self):
        """Очищаем тестовое окружение после каждого теста"""
        self.emulator.virtual_sys_folder.close()
        if os.path.exists(self.test_zip):
            os.remove(self.test_zip)

    # Тесты для cd
    def test_cd_valid_directory(self):
        """Тест перехода в существующую директорию"""
        self.emulator.cd(['test'])
        self.assertEqual(self.emulator.cwd, '/test/')

    def test_cd_invalid_directory(self):
        """Тест перехода в несуществующую директорию"""
        original_cwd = self.emulator.cwd
        self.emulator.cd(['nonexistent'])
        self.assertEqual(self.emulator.cwd, original_cwd)

    # Тесты для ls
    def test_ls_root_directory(self):
        """Тест вывода содержимого корневой директории"""
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.emulator.ls([])

        output = f.getvalue().strip()
        self.assertIn('test', output)
        self.assertIn('empty_dir', output)

    def test_ls_nested_directory(self):
        """Тест вывода содержимого вложенной директории"""
        import io
        from contextlib import redirect_stdout

        self.emulator.cd(['test'])
        f = io.StringIO()
        with redirect_stdout(f):
            self.emulator.ls([])

        output = f.getvalue().strip()
        self.assertIn('dir1', output)

    # Тесты для rmdir
    def test_rmdir_empty_directory(self):
        """Тест удаления пустой директории"""
        self.emulator.rmdir(['empty_dir'])
        self.assertNotIn('empty_dir/', self.emulator.virtual_sys_folder.namelist())

    def test_rmdir_non_empty_directory(self):
        """Тест попытки удаления непустой директории"""
        self.emulator.rmdir(['test'])
        self.assertIn('test/', self.emulator.virtual_sys_folder.namelist())

    # Тесты для date
    def test_date_no_args(self):
        """Тест вывода даты без аргументов"""
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.emulator.date([])

        output = f.getvalue().strip()
        self.assertTrue(len(output) > 0)

    def test_date_with_format(self):
        """Тест вывода даты с форматированием"""
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.emulator.date(['+%Y'])

        output = f.getvalue().strip()
        self.assertEqual(output, datetime.now().strftime('%Y'))

    # Тесты для chown
    def test_chown_valid_path(self):
        # Проверка изменения владельца
        self.emulator.chown(['newowner', 'test'])
        self.assertEqual(self.emulator.file_owners.get('test/'), 'newowner')

    def test_chown_invalid_path(self):
        initial_owners = self.emulator.file_owners.copy()
        self.emulator.chown(['newowner', 'nonexistent'])
        self.assertEqual(self.emulator.file_owners, initial_owners)

    # Тесты для exit
    def test_exit_normal(self):
        """Тест корректного завершения работы"""
        with self.assertRaises(SystemExit):
            self.emulator.exit()

    def test_exit_with_args(self):
        """Тест завершения работы с аргументами"""
        with self.assertRaises(SystemExit):
            self.emulator.exit(['dummy_arg'])



    # Тест обработки неизвестной команды
    def test_unknown_command(self):
        """Тест обработки неизвестной команды"""
        import io
        from contextlib import redirect_stdout

        f = io.StringIO()
        with redirect_stdout(f):
            self.emulator.execute_command('unknown_cmd')

        output = f.getvalue().strip()
        self.assertIn('unknown command', output)


if __name__ == '__main__':
    unittest.main()
