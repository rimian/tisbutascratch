from enum import Enum
import typer
from git import Repo
import re


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
def commit(dry_run: bool = typer.Option(False, "--dry-run", help="Perform a dry run without committing changes.")):
    """
    Commit changes with a formatted commit message based on the current branch name.
    """
    branch_name = repo.active_branch.name

    # Define the pattern to extract the ticket number
    pattern = r"^TF-\d+"
    matches = re.search(pattern, branch_name)

    if matches:
        ticket_number = matches.group()
        print("Ticket number:", ticket_number)

        # Prompt for the commit message and validate it
        while True:
            message = typer.prompt("What is the commit message?")
            if message.strip():
                break
            else:
                print("Please provide a non-empty commit message.")

        commit_message = f"{ticket_number} - {message}"

        if dry_run:
            print("Dry run mode enabled. Changes not committed.")
            print("Commit message:", commit_message)
            return

        # Commit changes with the formatted message
        repo.index.commit(commit_message)
        print("Changes committed successfully.")
    else:
        print("Did not find the ticket number in your branch name.")


# TODO get this to work
@app.command()
def wtf():
    hcommit = repo.head.commit
    print(hcommit.diff())


if __name__ == "__main__":
    app()