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

print("Hallo")


def version_callback(value: bool):
    """Prints the version of the package."""
    if value:
        console.print(
            f"[yellow]bewaarbot[/] version: [bold blue]{__version__}[/]"
        )
        raise typer.Exit()


@app.command(name="start")
def main():
    print("Bewaarbot initializing")
    start_bot()


if __name__ == "__main__":
    app()
