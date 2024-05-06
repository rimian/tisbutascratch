from enum import Enum
import typer
from git import Repo

app = typer.Typer()
repo = Repo.init(".")


def pick_changelog_type():
    types = ["admin", "api", "internal", "front_office"]
    print("Please select a changelog type:")
    for index, option in enumerate(types, start=1):
        print(f"{index}. {option}")
    selected_index = int(input("Enter the number corresponding to your choice: ")) - 1

    return types[selected_index]


@app.command()
def start():
    changelog_type = pick_changelog_type()
    ticket_number = typer.prompt("What is the ticket number?")
    description = typer.prompt("What is the ticket description?")

    print(f"{ticket_number} of type: {changelog_type}")

    description_formatted = description.strip().lower().replace(' ', '-')

    repo.git.checkout('-b', f"{ticket_number}-{description_formatted}")

    changelog_path = f"changelog/unreleased/{changelog_type}/{ticket_number}-{description_formatted}.md"

    f = open(changelog_path, "x")
    f.write(f"[{ticket_number}] - {description}\n")
    f.close()

    repo.index.add(changelog_path)
    repo.index.commit(f"feat({changelog_type}): changelog - {ticket_number} - {description}")


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