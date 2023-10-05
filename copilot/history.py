from copilot import history_file, shell_adapter


def _is_command(line):
    return line.startswith("- cmd: ")


def _formatted(command):
    return command.replace("- cmd: ", "").strip()[:100]


def _fish_commands():
    lines = history_file.fish_history_file_lines()
    return [_formatted(command) for command in lines if _is_command(command)]


def _zsh_commands():
    lines = history_file.zsh_history_file_lines()
    return [command.strip() for command in lines if command != ""]


def _bash_commands():
    lines = history_file.bash_history_file_lines()
    return [command.strip() for command in lines if command != ""]


def history_prompt_for(commands, n):
    if len(commands) == 0:
        return ""
    commands = list(dict.fromkeys(commands))
    most_recent_commands = "\n".join(commands[-n:])
    return f"""
The user has recently run these last {min(len(commands), n)} commands:
{most_recent_commands}
    """


def get_history(n=40):
    if shell_adapter.is_fish():
        return history_prompt_for(_fish_commands(), n)
    if shell_adapter.is_zsh():
        return history_prompt_for(_zsh_commands(), n)
    if shell_adapter.is_bash():
        return history_prompt_for(_bash_commands(), n)
    else:
        return ""


def save(cmd):
    history_file.save(cmd)
