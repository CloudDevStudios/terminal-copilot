import os
from time import time
import platform

from copilot import shell_adapter


def _fish_history_file_location():
    possible_paths = [
        os.path.join(os.environ["HOME"], ".local/share/fish/fish_history"),
        os.path.join(os.environ["HOME"], ".config/fish/fish_history"),
    ]
    return next((path for path in possible_paths if os.path.exists(path)), None)


def fish_history_file_lines():
    history_file = _fish_history_file_location()
    if history_file is None:
        return []
    with open(history_file, "r") as history:
        return history.readlines()


def _zsh_history_file_location():
    possible_paths = [
        os.path.join(os.environ["HOME"], ".zsh_history"),
    ]
    return next((path for path in possible_paths if os.path.exists(path)), None)


def zsh_history_file_lines():
    history_file = _zsh_history_file_location()
    if history_file is None:
        return []
    with open(history_file, 'rb') as history:
        return history.read().decode(errors='replace').splitlines()


def bash_history_file_lines():
    history_file = _bash_history_file_location()
    if history_file is None:
        return []
    with open(history_file, "r") as history:
        return history.readlines()


def _bash_history_file_location():
    possible_paths = [
        os.path.join(os.environ["HOME"], ".bash_history"),
    ]
    return next((path for path in possible_paths if os.path.exists(path)), None)


def _get_fish_history_line(command_script):
    return f"- cmd: {command_script}\n  when: {int(time())}\n"


def _get_zsh_history_line(command_script):
    return f"{command_script}\n"


def _get_bash_history_line(command_script):
    return f"{command_script}\n"


def save(cmd):
    if platform.system().lower().startswith("win"):
        return
    if shell_adapter.is_fish():
        formatted_line = _get_fish_history_line(cmd)
        history_file = _fish_history_file_location()
        _append_line(formatted_line, history_file)
    elif shell_adapter.is_zsh():
        formatted_line = cmd
        history_file = _zsh_history_file_location()
        _append_line(formatted_line, history_file)
    elif shell_adapter.is_bash():
        formatted_line = cmd
        history_file = _bash_history_file_location()
        _append_line(formatted_line, history_file)


def _append_line(formatted_line, history_file):
    if history_file and os.path.isfile(history_file):
        with open(history_file, "a") as history:
            history.write(formatted_line)
