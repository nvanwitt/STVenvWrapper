# SublimeVenvWrapper
Wrapper for Virtual Environment Access with SublimeREPL


STVenvWrapper is a wrapper script that allows simple generation of virutal-environment-specific REPLs through SublimeREPL.

This package will be made available through Package Control.

To be in line with modern virtual environment tools, STVenvWrapper will, by default, search for the following directories:

```
~/.venv
~/.virtualenvs
```

To add your own path, you have two choices:

1) Create a symbolic link to your venv bin directory (```~/User/ProjectVenv/bin```) in one of the default paths.
or
2) Create a '''STVenvWrapper.sublime-settings''' file in your Sublime User directory with your paths in json format.
