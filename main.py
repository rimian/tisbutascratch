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

    description_formatted = description.strip().lower().replace(' ', '-')

    repo.git.checkout('-b', f"{ticket_number}-{description_formatted}")

    changelog_path = f"changelog/unreleased/{type.value}/{ticket_number}-{description_formatted}.md"

    f = open(changelog_path, "x")
    f.write(f"[{ticket_number}] - {description}\n")
    f.close()

    repo.index.add(changelog_path)
    repo.index.commit(f"feat({type.value}): changelog - {ticket_number} - {description}")


@app.command()
def commit():
    ticket_number = repo.active_branch.name
    message = typer.prompt("What is the commit message?")
    repo.index.commit(f"{ticket_number} - {message}")


# TODO get this to work
@app.command()
def wtf():
    hcommit = repo.head.commit
    print(hcommit.diff())


if __name__ == "__main__":
    app()