import typer
from git import Repo
from utils import extract_ticket_number, pick_changelog_type
from meta import read_meta, write_meta


app = typer.Typer()
repo = Repo.init(".")


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
        write_meta(branch_name, changelog_type, ticket_number, description)
        with open(changelog_path, "x") as f:
            f.write(f"[{ticket_number}] - {description}\n")
    except FileExistsError:
        typer.echo("Changelog file already exists. Aborting.")
        return

    repo.index.add(changelog_path)
    repo.index.commit(f"feat({changelog_type}): changelog - {ticket_number} - {description}")


@app.command()
def commit(dry_run: bool = typer.Option(False, "--dry-run", "-d", help="Perform a dry run without committing changes.")):
    """
    Commit changes with a formatted commit message based on the current branch name.
    """
    branch_name = repo.active_branch.name
    ticket_number = extract_ticket_number(branch_name)

    if ticket_number:
        if dry_run:
            print("Dry run mode enabled. Changes not committed.")

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
            print("Commit message:", commit_message)
            return

        # Commit changes with the formatted message
        repo.index.commit(commit_message)
        print("Changes committed successfully.")
    else:
        print("Did not find the ticket number in your branch name.")


@app.command()
def wtf():
    """
    Print metadata for the current branch.
    """
    branch_name = repo.active_branch.name
    metadata = read_meta(branch_name)
    if metadata:
        print(f"Metadata for branch '{branch_name}':")
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print(f"No metadata found for branch '{branch_name}'.")


if __name__ == "__main__":
    app()