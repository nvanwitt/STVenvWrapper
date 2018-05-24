import sublime
import sublime_plugin
import os
import json


class SublimeVenvWrapper(sublime_plugin.TextCommand):
    srv_env = []

    def run(self, edit):

        json_file = sublime.find_resources("STVenvWrapper.sublime-settings")[0]

        data = json.loads(sublime.load_resource(json_file))

        self.venv_list = []
        self.main_list = []
        for paths in data.values():
            for path in iter(paths):
                path = os.path.expanduser(path)
                if os.path.exists(path):
                    [self.venv_list.append([venv, os.path.join(path, venv)]) for venv in iter(os.listdir(path)) if os.path.isdir(os.path.join(path, venv))]
        self.view.window().show_quick_panel(self.venv_list, self.on_done)

    def on_done(self, index):
        self.description()
        if index >= 0:
            try:
                venv_dir = os.path.realpath(self.venv_list[index][1])
                print(venv_dir)
                self.view.window().run_command('sublime_repl_venv_runner', {'venv_dir': venv_dir})
            except ValueError:
                self.print('Invalid Directory')
                pass


class SublimeReplVenvRunner(sublime_plugin.WindowCommand):
    def run(self, venv_dir):

        try:
                python_executable = os.path.join(venv_dir, "python")
                project_dir = os.path.split(venv_dir)[0]
                path_separator = ':'
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

        except ValueError:
            print('Fail')


