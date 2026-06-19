import typer
from rich import print as rprint

app = typer.Typer()


@app.command()
def main(prompt: str = "Hello world!") -> None:
    """Run a simple Strands Agents demo."""
    rprint(f"[bold red]{prompt}[/bold red]")


if __name__ == "__main__":
    app()
