from pathlib import Path
import re
from pprint import pprint

def split_name(name):
    """Split the name of an input directory name or a file name

    Args:
        name (str): The name of the file or directory.

    Returns:
        int: The prefix of the name.
        base: The remaining name
    """
    text = Path(name).parts[-1]
    pattern = r'^(\d{1,3})\.? ([\w\s&\-,\.\(\)\[\]\^\+\'\!_#;\–]+)$'
    match = re.search(pattern, text)
    # print("got match for", name)
    if match:
        prefix = match.group(1)
        base = match.group(2)
        # get the index of the first alphabet in the string.
        index = re.search(r"[a-zA-Z]", base).start()
        base = base[index:]
    else:
        raise AssertionError(f"pattern not respected for '{text}'")
    # convert the prefix to an integer
    return int(prefix), base


def rename_subfolders(base_path, folder_name):
    """Renames files and/or directories in the given folder to have a zero-padded prefix.

    Args:
        base_path (Path): The base path of the folder containing the subfolders.
        folder_name (str): The name of the folder containing the subfolders.

    Returns:
        None.
    """
    folder_path = Path(base_path, folder_name)
    subfolders = [d for d in folder_path.iterdir() if d.is_dir()]
    for subfolder in subfolders:
        # pprint([split_name(d.name) for d in subfolders][:5])
        # should be declared (and recalculated) here as we use the same names when called from within files rename
        max_prefix = max([split_name(d.name)[0] for d in subfolders])
        padding_length = len(str(max_prefix))
        print("padding_length", padding_length)
        try:
            prefix, base = split_name(subfolder.name)
            new_prefix = str(prefix).zfill(padding_length)
            # The parts[-1] attribute of a Path object represents the base name of the subfolder,
            # without the file extension for files or the trailing dot for directories.
            # The suffix attribute represents the file extension for files or an empty string for directories.
            subfolder_new_name = f"{new_prefix}. {base}"
            subfolder_new = Path(subfolder.parent, subfolder_new_name)
            subfolder.rename(subfolder_new)
            print(f"{80*'='}\nRenamed folder {subfolder}\n ----> {subfolder_new}\n{80*'-'}")
            files = [d for d in subfolder_new.iterdir() if d.is_file()]
            # remove docx, pdf,txt,... files that have the pattern \d.\d *
            files = [file for file in files if not str(file).endswith(("docx", "pdf", "jpg", "doc", "xlsx", "txt", "html"))]
            for file in files:
                max_prefix = max([split_name(f.name)[0] for f in files])
                padding_length = len(str(max_prefix))
                try:
                    prefix, base = split_name(file.name)
                    new_prefix = str(prefix).zfill(padding_length)
                    file_new_name = f"{new_prefix}. {base}"
                    file.rename(Path(file.parent, file_new_name))
                    print(f"Renamed file {file}\n ----> {Path(file.parent, file_new_name)}\n{80*'-'}")
                except Exception as e:
                    print(f"Failed to rename file {file}: {e}")
        except Exception as e:
            raise Exception(f"Failed to rename file {subfolder}: {e}")


if __name__ == "__main__":
    base_path = Path(__file__).parent
    folder_names = (
        "Udemy - Practical Reinforcement Learning using Python - 8 AI Agents 2021-3",
        "Udemy – Reinforcement Learning beginner to master – AI in Python 2022-10",
        "Udemy - Logging in Kubernetes with EFK Stack 2022-3"
    )
    for folder_name in folder_names:
        rename_subfolders(base_path, folder_name)

        print(f"Finished renaming directory {folder_name} and its subdirectories.")
