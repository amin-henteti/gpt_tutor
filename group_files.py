import json
from pathlib import Path
from fuzzywuzzy import fuzz
import shutil

def get_actual_file_name(file_name, actual_files):
    """
    Get the actual file name from a list of actual file names based on the highest similarity score with the given file name.

    Args:
        file_name (str): The file name to match.
        actual_files (list): List of actual file names.

    Returns:
        str: The actual file name with the highest similarity score.
    """
    similarities = [fuzz.ratio(file_name.lower(), actual_file_name.lower()) for actual_file_name in actual_files]
    # Find the index of the highest similarity score
    max_similarity_index = similarities.index(max(similarities))
    # Return the actual file name with the highest similarity
    return actual_files[max_similarity_index]
    # threshold = 80
    # print("similarity:", similarities[max_similarity_index])
    # Find the indices of elements equal to "similar"
    # ind = np.where(np.isin(find_similar, ["similar"]))[0]
    # ind = list(find_similar).index("similar")

def create_subfolder(folder_path, subfolder_name):
    """
    Create a subfolder with the given name inside the provided folder path.

    Args:
        folder_path (Path): Path to the parent folder.
        subfolder_name (str): Name of the subfolder.

    Returns:
        Path: The path to the created subfolder.
    """
    subfolder_path = folder_path / subfolder_name
    subfolder_path.mkdir(parents=True, exist_ok=True)
    return subfolder_path

def process_files(folder_path, json_file_path):
    with open(json_file_path, 'r') as json_file:
        json_data = json.load(json_file)

    actual_files = [f.name for f in folder_path.iterdir() if f.is_file()]

    for subfolder_name, files_dict in json_data.items():
        print("=" * 70)
        subfolder_path = create_subfolder(folder_path, subfolder_name)
        print(f"Created subfolder: {subfolder_name}")

        for file_name in files_dict.values():
            actual_file_name = get_actual_file_name(file_name, actual_files)
            source_file_path = folder_path / actual_file_name

            if not actual_file_name:
                print(f"File not found: {file_name}")
            else:
                actual_file_name = actual_file_name.replace(" .mp4", ".mp4")
                destination_file_path = subfolder_path / actual_file_name
                print(f"{actual_file_name} represents {file_name}")
                shutil.move(source_file_path, destination_file_path)
                print(f"Moved {source_file_path} to {destination_file_path}")

if __name__ == "__main__":
    folder_path = Path('D:/online_learning/linux')
    json_file_path = Path('D:/online_learning/Linux.json')
    process_files(folder_path, json_file_path)
