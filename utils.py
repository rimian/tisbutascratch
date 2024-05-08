import re
from enum import Enum

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


def extract_ticket_number(branch_name: str) -> str:
    """
    Extract the ticket number from the branch name.
    """
    pattern = r"^TF-\d+"
    matches = re.search(pattern, branch_name)
    if matches:
        return matches.group()
    else:
        return ""
