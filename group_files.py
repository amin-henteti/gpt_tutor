import json
from pathlib import Path
from fuzzywuzzy import fuzz
import shutil

def get_actual_file_name(file_name, actual_files):
    # Calculate similarity scores between the given file name and actual file names
    similarities = [fuzz.ratio(file_name.lower(), actual_file_name.lower()) for actual_file_name in actual_files]
    # Find the index of the highest similarity score
    max_similarity_index = similarities.index(max(similarities))
    # Return the actual file name with the highest similarity
    return actual_files[max_similarity_index]
    threshold = 80
    # print("similarity:", similarities[max_similarity_index])
    # Find the indices of elements equal to "similar"
    # ind = np.where(np.isin(find_similar, ["similar"]))[0]
    # ind = list(find_similar).index("similar")

def create_subfolder(folder_path, subfolder_name):
    # Create a subfolder with the given name inside the folder path
    subfolder_path = folder_path / subfolder_name
    subfolder_path.mkdir(parents=True, exist_ok=True)
    return subfolder_path

if __name__ == "__main__":
    # Path to the folder containing the files
    folder_path = Path(r'D:\online_learning\CBTNuggets - Linux Professional Institute LPIC-1 (101-500 & 102-500) 2022-4')
    # Path to the JSON file
    json_file_path = Path(r'D:\online_learning\Linux Professional Institute LPIC LPI Certification Training1.json')
    # Load the JSON data
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
