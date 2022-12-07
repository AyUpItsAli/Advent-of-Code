import json

ROOT = "/"
file_system = {}


# Returns the directory dict for the given path
def get_directory(directory_path: list) -> dict:
    directory = file_system  # Start at the root
    for sub_directory in directory_path:  # Iterate over sub dirs, down to the last dir
        directory = directory[sub_directory]
    return directory


# Creates a new directory at the given path, then returns the new path to the inside of that directory
def create_new_directory(new_directory: str, directory_path: list) -> list:
    parent_directory = get_directory(directory_path)  # Get where this directory will be located
    parent_directory[new_directory] = {}  # Add new empty directory to the parent directory
    directory_path.append(new_directory)  # Update the path
    return directory_path  # Return the new path, which now points inside the newly created directory


# Adds a new file to the directory at the given path
def add_file(file: list, directory_path: list) -> None:
    file_size = int(file[0])
    file_name = file[1]
    directory = get_directory(directory_path)
    directory[file_name] = file_size


# Traverses the file system via the commands in the puzzle input.
# Builds the file_system dict as it traverses the file system.
def create_file_system() -> None:
    current_path = []
    with open("day7input.txt", "r") as file:
        line = file.readline()
        while line != "":
            if not line.startswith("$"):
                line = file.readline()
            else:
                command = line.strip("\n").strip("$ ").split(" ")
                if command[0] == "cd":
                    new_directory = command[1]
                    if new_directory == ".." and current_path:
                        current_path.pop()
                    elif new_directory == ROOT:
                        current_path = []
                    else:
                        current_path = create_new_directory(new_directory, current_path)
                    line = file.readline()
                elif command[0] == "ls":
                    line = file.readline()
                    while not line.startswith("$") and line != "":
                        if not line.startswith("dir"):
                            child_file = line.strip("\n").split(" ")
                            add_file(child_file, current_path)
                        line = file.readline()


create_file_system()
print(json.dumps(file_system, indent=4))
print("File system above ^^^")


# Returns the sum of file sizes (direct or indirect) for the given directory dict
def get_directory_size(directory: dict) -> int:
    size = 0
    for child in directory.values():
        if isinstance(child, int):
            size += child
        elif isinstance(child, dict):
            size += get_directory_size(child)
    return size


# Returns the sum of directory sizes up to 100,000
def get_total_directory_sizes(directory: dict):
    total = 0
    for child in directory.values():
        if isinstance(child, dict):
            size = get_directory_size(child)
            if size <= 100_000:
                total += size
            total += get_total_directory_sizes(child)
    return total


# Part 1
print("Part 1: {}".format(get_total_directory_sizes(file_system)))

# Part 2
DISK_SPACE = 70_000_000
REQUIRED_SPACE = 30_000_000

used_space = get_directory_size(file_system)
free_space = DISK_SPACE - used_space


# Returns a list of directory sizes that, when deleted, would free up enough space to run the update
def get_sufficient_directory_sizes(directory: dict):
    sufficient_sizes = []
    for child in directory.values():
        if isinstance(child, dict):
            size = get_directory_size(child)
            if size + free_space >= REQUIRED_SPACE:
                sufficient_sizes.append(size)
            sufficient_sizes.extend(get_sufficient_directory_sizes(child))
    return sufficient_sizes


# Begin with the size of the whole file system, in case we have to remove everything to run the update
sufficient_sizes = [used_space]
sufficient_sizes.extend(get_sufficient_directory_sizes(file_system))  # Extend with any other sufficient sizes
sufficient_sizes.sort()  # Sort sizes (smallest to biggest)
print("Part 2: {}".format(sufficient_sizes[0]))  # Print smallest