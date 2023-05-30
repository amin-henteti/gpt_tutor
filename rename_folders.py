from pathlib import Path
import re
from pprint import pprint

def split_name(name):
    """Split the name of an input directory name or a file name

    Args:
        name (str): The name of the file or directory.

    Returns:
        int: The prefix of the name.
        base: The remaining name.
    """
    text = Path(name).name
    pattern = r'^(\d{1,3})\.? ([\w\s&\-,\.\(\)\[\]\^\+\'\!_#;\–]+)$'
    match = re.search(pattern, text)
    if match:
        prefix = match.group(1)
        base = match.group(2)
        # get the index of the first alphabet in the string.
        index = re.search(r"[a-zA-Z]", base).start()
        base = base[index:]
    else:
        raise AssertionError(f"Pattern not respected for '{text}'")
    return int(prefix), base


def rename_files_in_folder(folder_path):
    """Renames files in the given folder to have a zero-padded prefix.

    Args:
        folder_path (Path): The path of the folder.

    Returns:
        None.
    """
    folder = Path(folder_path)
    # remove docx, pdf,txt,... files that have the pattern \d.\d *
    files = [f for f in folder.iterdir() if f.is_file() and not f.endswith(("docx", "pdf", "jpg", "doc", "xlsx", "txt", "html"))]
    max_prefix = max([split_name(f.name)[0] for f in files])
    padding_length = len(str(max_prefix))
    
    for file in files:
        try:
            prefix, base = split_name(file.name)
            new_prefix = str(prefix).zfill(padding_length)
            file_new_name = f"{new_prefix}. {base}"
            file_new = Path(file.parent, file_new_name)
            file.rename(file_new)
            print(f"Renamed file {file}\n ----> {file_new}\n{'-' * 80}")
        except Exception as e:
            print(f"Failed to rename file {file}: {e}")


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
    
    max_prefix = max([split_name(d.name)[0] for d in subfolders])
    padding_length = len(str(max_prefix))
    print("padding_length", padding_length)
    for subfolder in subfolders:
        # pprint([split_name(d.name) for d in subfolders][:5])
        # should be declared (and recalculated) here as we use the same names when called from within files rename
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
            rename_files_in_folder(subfolder_new)
        except Exception as e:
            print(f"Failed to rename folder {subfolder}: {e}")


if __name__ == "__main__":
    base_path = Path(__file__).parent
    folder_names = ["learn"]
    
    for folder_name in folder_names:
        rename_subfolders(base_path, folder_name)
        print(f"Finished renaming directory {folder_name} and its subdirectories.")
