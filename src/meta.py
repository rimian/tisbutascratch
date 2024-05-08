import yaml

METADATA_FILE = ".kcli.yml"

import yaml

def write_meta(branch_name, changelog_type, ticket_number, description):
    """
    Append metadata to the YAML file.
    """
    # Read existing metadata from file
    try:
        with open(METADATA_FILE, "r") as f:
            existing_metadata = yaml.safe_load(f)
    except FileNotFoundError:
        existing_metadata = {}

    # Update existing metadata with new entry
    existing_metadata[branch_name] = {
        "changelog_type": changelog_type,
        "ticket_number": ticket_number,
        "description": description
    }

    # Write merged metadata back to file
    with open(METADATA_FILE, "w") as f:
        yaml.dump(existing_metadata, f)


def read_meta(branch_name):
    """
    Read metadata for a specific branch from the YAML file.
    """
    try:
        with open(METADATA_FILE, "r") as f:
            metadata = yaml.safe_load(f)
            if metadata and branch_name in metadata:
                return metadata[branch_name]
            else:
                print(f"Metadata for branch '{branch_name}' not found.")
                return None
    except FileNotFoundError:
        print("Metadata file not found.")
        return None
