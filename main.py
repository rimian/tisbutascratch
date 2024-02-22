import typer

def main():
    ticket_number = typer.prompt("What is the ticket number?")
    description = typer.prompt("What is the ticket description?")
    changelog_type = typer.prompt("What type is it?")


if __name__ == "__main__":
    typer.run(main)