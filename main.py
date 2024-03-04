from enum import Enum
import typer
from git import Repo

app = typer.Typer()
repo = Repo.init(".")

class ChangelogType(str, Enum):
    admin = "admin"
    api = "api"
    internal = "internal"
    front_office = "office"


@app.command()
def start(type: ChangelogType = ChangelogType.internal):
    ticket_number = typer.prompt("What is the ticket number?")
    description = typer.prompt("What is the ticket description?")
    print(f"{ticket_number} of type: {type.value}")
    f = open(f"changelog/unreleased/{type.value}/{ticket_number}-{description.strip().lower().replace(' ', '-')}.md", "x")
    f.write(f"[{ticket_number}] - {description}")


@app.command()
def wtf():
    hcommit = repo.head.commit
    print(hcommit.diff())


if __name__ == "__main__":
    app()