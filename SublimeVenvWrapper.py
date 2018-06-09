import sublime
import sublime_plugin
import os


class RunVenvSelectorCommand(sublime_plugin.WindowCommand):

    def run(self):
        if os.path.exists(os.path.join(sublime.packages_path(), 'SublimeREPL')) is False:
            sublime.message_dialog('Use of this wrapper requires the SublimeREPL package. You can install this package via Package Control')
            exit()

        # Load Settings file, /User/STVenvWrapper.sublime-settings file will predominate per SublimeText hierarchy
        data = sublime.load_settings("STVenvWrapper.sublime-settings").get("python_venv_paths")

        self.venv_list = []

        # Create list of lists of user virtual environments with corresponding /bin paths
        self.verifyuserpath(data)
        # Show quick panel with virtual environments listed
        self.window.show_quick_panel(self.venv_list, self.on_done)

    def verifyuserpath(self, data):
        # Check for venv path validity based off presence of /bin directory
        # This is used to filter down possible list of directories to ones most likely to be venv bin paths
        for envpaths in data:
            envpaths = os.path.expanduser(envpaths)
            if os.path.exists(envpaths):
                if os.path.basename(envpaths) == 'bin':
                    venv = os.path.basename(os.path.split(envpaths)[0])
                    self.appendvenvlist(venv, envpaths)
                elif os.path.exists(os.path.join(envpaths, 'bin')):
                    venv = os.path.basename(envpaths)
                    venvpath = os.path.join(envpaths, 'bin')
                    self.appendvenvlist(venv, venvpath)
                else:
                    for venv in os.listdir(envpaths):
                        real_path = os.path.realpath(os.path.join(envpaths, venv))
                        if '/bin' not in real_path:
                            real_path = os.path.join(real_path, 'bin')
                        self.appendvenvlist(venv, real_path)

    def appendvenvlist(self, venv, venvpath):
        # Appends virtual environemnt name and path to list if activate and python files are detected (indicating true venv bin path)
        if os.path.isdir(venvpath):
            if 'activate' and 'python' in os.listdir(venvpath):
                if self.window.project_file_name() is not None:
                    if os.path.split(venvpath)[0] == os.path.split(self.window.project_file_name())[0]:
                        # If project file detected, insert corresponding virtual environment (if applicable) to start of list
                        self.venv_list.insert(0, [venv, venvpath])
                    else:
                        self.venv_list.append([venv, venvpath])
                else:
                    self.venv_list.append([venv, venvpath])

    def on_done(self, index):
        if index >= 0:
            venv_dir = self.venv_list[index][1]
            self.window.run_command('sublime_repl_venv_runner', {'venv_dir': venv_dir})


class SublimeReplVenvRunnerCommand(sublime_plugin.WindowCommand):
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

