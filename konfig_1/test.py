import unittest
from io import StringIO
import sys
import os
import datetime
from shell_emulator import ShellEmulator


class TestShellEmulator(unittest.TestCase):

    def setUp(self):
        self.held_output = StringIO()
        sys.stdout = self.held_output
        self.emulator = ShellEmulator("test_user", "./file_system.zip")

    def tearDown(self):
        sys.stdout = sys.__stdout__

    def test_ls_empty_directory(self):
        self.held_output.truncate(0)
        self.held_output.seek(0)

        self.emulator.cwd = "/"
        self.emulator.ls()
        output = self.held_output.getvalue().strip()

        self.assertIn("dir1", output)
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)

    def test_ls_non_empty_directory(self):
        if "file1.txt" not in self.emulator.virtual_sys_folder.namelist():
            self.emulator.virtual_sys_folder.writestr("file1.txt", "content")
        if "file2.txt" not in self.emulator.virtual_sys_folder.namelist():
            self.emulator.virtual_sys_folder.writestr("file2.txt", "content")

        self.emulator.cwd = "/"
        self.emulator.ls()
        output = self.held_output.getvalue().strip()
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)

    def test_cd_root_directory(self):
        self.emulator.cd(["/"])
        self.assertEqual(self.emulator.cwd, "/")

    def test_cd_non_existing_directory(self):
        self.emulator.cd(["non_existing"])
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "No such file or directory")

    def test_rmdir_existing_directory(self):
        if "dir1/" not in self.emulator.virtual_sys_folder.namelist():
            self.emulator.virtual_sys_folder.writestr("dir1/", "")
        self.emulator.cwd = "/"
        self.emulator.rmdir(["dir1"])
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "Directory 'dir1' removed (simulated)")

    def test_rmdir_non_existing_directory(self):
        self.emulator.cwd = "/"
        self.emulator.rmdir(["non_existing"])
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "No such directory")

    def test_date_command(self):
        self.emulator.date()
        output = self.held_output.getvalue().strip()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.assertTrue(output.startswith(current_date[:10]))  # Проверяем начало даты

    def test_chown_command(self):
        self.emulator.chown(["user1", "file1"])
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "Owner of 'file1' changed to 'user1' (simulated)")

    def test_chown_missing_arguments(self):
        self.emulator.chown(["file1"])
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "Usage: chown <user> <file>")

    def test_exit_command(self):
        with self.assertRaises(SystemExit):
            self.emulator.exit()
        output = self.held_output.getvalue().strip()
        self.assertEqual(output, "Bye!")

    def test_run_script(self):
        script_path = "temp_script.sh"
        with open(script_path, "w") as script:
            script.write("ls\n")
            script.write("date\n")

        self.emulator.run_script(script_path)
        output = self.held_output.getvalue().strip()
        self.assertIn("file1.txt", output)
        self.assertIn("file2.txt", output)
        self.assertTrue(
            any(line.startswith(datetime.datetime.now().strftime("%Y-%m-%d")) for line in output.splitlines()))

        os.remove(script_path)


if __name__ == '__main__':
    unittest.main()

