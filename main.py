from enum import Enum
import typer

class ChangelogType(str, Enum):
    internal = "internal"
    api = "api"
    front_office = "office"


def main(type: ChangelogType = ChangelogType.internal):
    ticket_number = typer.prompt("What is the ticket number?")
    description = typer.prompt("What is the ticket description?")

    print(f"{ticket_number} of type: {type.value}")


if __name__ == "__main__":
    typer.run(main)