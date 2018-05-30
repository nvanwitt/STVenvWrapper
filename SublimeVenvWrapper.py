import sublime
import sublime_plugin
import os


class SublimeVenvWrapper(sublime_plugin.TextCommand):

    def run(self, edit):
        # Load Settings file, /User/STVenvWrapper.sublime-settings file will predominate per SublimeText hierarchy
        data = sublime.load_settings("STVenvWrapper.sublime-settings").get("python_venv_paths")

        self.venv_list = []

        # Create list of lists of user virtual environments with corresponding /bin paths
        self.venvlistcreate(data)

        # Show quick panel with virtual environments listed
        self.view.window().show_quick_panel(self.venv_list, self.on_done)

    def venvlistcreate(self, data):
        for path in iter(data):
            print(path)
            print(self.view.settings().get("python_venv_paths", True))
            path = os.path.expanduser(path)
            if os.path.exists(path):
                for venv in iter(os.listdir(path)):
                    real_path = os.path.realpath(os.path.join(path, venv))
                    if '/bin' not in real_path:
                            real_path = os.path.join(real_path, 'bin')
                    if os.path.isdir(real_path):
                        if 'activate' and 'python' in os.listdir(real_path):
                            if self.view.window().project_file_name() is not None:
                                print(self.view.window().project_data())
                                if os.path.split(real_path)[0] == os.path.split(self.view.window().project_file_name())[0]:
                                    # If project file detected, insert corresponding virtual environment (if applicable) to start of list
                                    self.venv_list.insert(0, [venv, real_path])
                                else:
                                    self.venv_list.append([venv, real_path])
                            else:
                                self.venv_list.append([venv, real_path])

    def on_done(self, index):
        if index >= 0:
            try:
                venv_dir = os.path.realpath(self.venv_list[index][1])
                self.view.window().run_command('sublime_repl_venv_runner', {'venv_dir': venv_dir})
            except ValueError:
                self.print('Invalid Directory')
                pass


class SublimeReplVenvRunner(sublime_plugin.WindowCommand):
    def run(self, venv_dir):

        python_executable = os.path.join(venv_dir, "python")
        project_dir = os.path.split(venv_dir)[0]
        path_separator = ':'

        # Open Repl Command, code altered from Wuub's SublimeREPL
        self.window.run_command("repl_open",
        {
            "encoding": "utf8",
            "type": "subprocess",
            "autocomplete_server": True,
            "extend_env": {
                "PATH": venv_dir + path_separator + "{PATH}",
                "PYTHONIOENCODING": "utf-8"
            },
            "cmd": [python_executable, "-i", "-u"],
            "cwd": project_dir,
            "encoding": "utf8",
            "syntax": "Packages/Python/Python.tmLanguage",
            "external_id": "python"
        })

