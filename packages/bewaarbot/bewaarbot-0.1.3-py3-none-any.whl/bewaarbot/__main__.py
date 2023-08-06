# type: ignore[attr-defined]

import typer
from bewaarbot import __version__
from bewaarbot.cli import start_bot
from rich.console import Console

app = typer.Typer(
    name="bewaarbot",
    help="Awesome `bewaarbot` is a Python cli/package created with https://github.com/TezRomacH/python-package-template",
    add_completion=False,
)
console = Console()


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]bewaarbot[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command(name="start")
def start():
    """
    Start a new instance of Bewaarbot.
    """

    print("Bewaarbot initializing")
    start_bot()


@app.callback()
def callback(
    version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the {{ cookiecutter.project_name }} package.",
    ),
):
    pass


if __name__ == "__main__":
    app()
