from enum import Enum
import typer

app = typer.Typer()


class ChangelogType(str, Enum):
    internal = "internal"
    api = "api"
    front_office = "office"


@app.command()
def start(type: ChangelogType = ChangelogType.internal):
    ticket_number = typer.prompt("What is the ticket number?")
    description = typer.prompt("What is the ticket description?")
    print(f"{ticket_number} of type: {type.value}")
    f = open(f"{type.value}/{ticket_number}-{description.lower().replace(' ', '-')}.md", "x")
    f.write(f"[{ticket_number}] - {description}")


@app.command()
def other():
    pass


if __name__ == "__main__":
    app()