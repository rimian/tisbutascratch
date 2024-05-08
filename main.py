from enum import Enum
import typer
from git import Repo

app = typer.Typer()
repo = Repo.init(".")


class ChangelogType(str, Enum):
    admin = "admin"
    api = "api"
    internal = "internal"
    front_office = "front_office"


def pick_changelog_type() -> str:
    """
    Prompt the user to select a changelog type.
    """
    types = [type_.value for type_ in ChangelogType]
    print("Please select a changelog type:")
    for index, option in enumerate(types, start=1):
        print(f"{index}. {option}")
    selected_index = int(input("Enter the number corresponding to your choice: ")) - 1
    return types[selected_index]


@app.command()
def start():
    """
    Start the changelog creation process.
    """
    changelog_type = pick_changelog_type()
    ticket_number = typer.prompt("What is the ticket number?")
    description = typer.prompt("What is the ticket description?")

    print(f"{ticket_number} of type: {changelog_type}")

    description_formatted = description.strip().lower().replace(' ', '-')

    branch_name = f"{ticket_number}-{description_formatted}"
    repo.git.checkout('-b', branch_name)

    changelog_path = f"changelog/unreleased/{changelog_type}/{branch_name}.md"

    # Check if the file already exists
    try:
        with open(changelog_path, "x") as f:
            f.write(f"[{ticket_number}] - {description}\n")
    except FileExistsError:
        typer.echo("Changelog file already exists. Aborting.")
        return

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