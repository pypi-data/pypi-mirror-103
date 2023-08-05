import subprocess  # nosec - skip B404:blacklist
import logging
import shlex
from click.testing import CliRunner
logger = logging.getLogger(__name__)


def run_shell_command(command: str):
    """Given a string of a bash command, run the shell command here. This is risky AF, so make sure you are careful and don't use this to accept user input."""
    # args = command.split(" ")
    args = shlex.split(command)
    response = subprocess.Popen(args=args)  # nosec - skip B404:blacklist, B603:subprocess_without_shell_equals_true
    logger.info(f"{command} response: {response}")


def run_click_command(click_function_to_run, args: str) -> str:
    """
    Given a python method that runs a click command, use the click.testing.CliRunner to run the command with arguments provided as a string
    """
    runner = CliRunner()
    args = shlex.split(args)
    result = runner.invoke(click_function_to_run, args)
    return result
