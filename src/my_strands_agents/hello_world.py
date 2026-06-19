import typer
from strands import Agent

app = typer.Typer()


@app.command()
def main(prompt: str = "Say hello and briefly explain what you are.") -> None:
    """Run a simple Strands Agents demo."""
    agent = Agent()
    agent(prompt)


if __name__ == "__main__":
    app()
