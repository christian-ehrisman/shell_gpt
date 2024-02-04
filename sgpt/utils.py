import os
import platform
import shlex
import subprocess
from tempfile import NamedTemporaryFile
from typing import Any, Callable

import typer
from click import BadParameter, UsageError

from sgpt.__version__ import __version__
from sgpt.integration import bash_integration, zsh_integration, powershell_integration, fish_integration


def get_edited_prompt() -> str:
    """
    Opens the user's default editor to let them
    input a prompt, and returns the edited text.

    :return: String prompt.
    """
    with NamedTemporaryFile(suffix=".txt", delete=False) as file:
        # Create file and store path.
        file_path = file.name
    editor = os.environ.get("EDITOR", "vim")
    # This will write text to file using $EDITOR.
    os.system(f"{editor} {file_path}")
    # Read file when editor is closed.
    with open(file_path, "r", encoding="utf-8") as file:
        output = file.read()
    os.remove(file_path)
    if not output:
        raise BadParameter("Couldn't get valid PROMPT from $EDITOR")
    return output


def run_command(command: str) -> None:
    """
    Runs a command in the user's shell.
    It is aware of the current user's $SHELL.
    :param command: A shell command to run.
    """
    if platform.system() == "Windows":
        is_powershell = len(os.getenv("PSModulePath", "").split(os.pathsep)) >= 3
        full_command = (
            f'powershell.exe -Command "{command}"'
            if is_powershell
            else f'cmd.exe /c "{command}"'
        )
    else:
        shell = os.environ.get("SHELL", "/bin/sh")
        full_command = f"{shell} -c {shlex.quote(command)}"

    os.system(full_command)


def option_callback(func: Callable) -> Callable:  # type: ignore
    def wrapper(cls: Any, value: str) -> None:
        if not value:
            return
        func(cls, value)
        raise typer.Exit()

    return wrapper


def powershell_profile_path():
    command = 'Write-Host $PROFILE'
    result = subprocess.run(["powershell", "-Command", command], capture_output=True)
    profile_path = result.stdout.decode().strip()
    if os.path.exists(profile_path):
        return profile_path
    else:
        return None

def install_shell_integration(shell_script):
    shell = os.getenv("SHELL", "")
    if shell == "/bin/zsh":
        typer.echo("Installing Zsh integration...")
        with open(os.path.expanduser("~/.zshrc"), "a", encoding="utf-8") as file:
            file.write(zsh_integration)
    elif shell == "/bin/bash":
        typer.echo("Installing Bash integration...")
        with open(os.path.expanduser("~/.bashrc"), "a", encoding="utf-8") as file:
            file.write(bash_integration)
    elif "fish" in shell.lower():
        typer.echo("Installing Fish integration...")
        fish_config_path = os.path.expanduser("~/.config/fish/config.fish")
        with open(fish_config_path, "a", encoding="utf-8") as file:
            file.write(fish_integration)
    elif "powershell" in shell.lower():
        typer.echo("Installing PowerShell integration...")
        with open(powershell_profile_path(), "a", encoding="utf-8") as file:
            file.write(powershell_integration)
    else:
        raise UsageError("ShellGPT integrations only available for Zsh, Bash, Fish, and PowerShell.")

    typer.echo("Done! Restart your shell to apply changes.")

@option_callback
def get_sgpt_version(*_args: Any) -> None:
    """
    Displays the current installed version of ShellGPT
    """
    typer.echo(f"ShellGPT {__version__}")
