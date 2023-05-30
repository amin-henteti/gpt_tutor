import os
from xml.etree.ElementTree import ElementTree, Element, SubElement

def write_playlist(folder_path, playlist_file):
    subfolders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    subfolders.sort()
    # Create a list of video files sorted by folder name and video name
    video_files = []
    for subfolder in subfolders:
        subfolder_path = os.path.join(folder_path, subfolder)
        video_files_in_subfolder = [f for f in os.listdir(subfolder_path) if f.endswith(".mp4")]
        video_files_in_subfolder.sort()
        video_files.extend([os.path.join(subfolder, f) for f in video_files_in_subfolder])

    root = Element("playlist", xmlns="http://xspf.org/ns/0/", xmlns_vlc="http://www.videolan.org/vlc/playlist/ns/0/", version="1")
    SubElement(root, "title").text = "Liste de lecture"
    tracklist = SubElement(root, "trackList")

    for i, filename in enumerate(video_files):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            track = SubElement(tracklist, "track")
            SubElement(track, "location").text = f"file:///{file_path}"
            SubElement(track, "title").text = os.path.splitext(os.path.basename(filename))[0]
            SubElement(track, "duration").text = "0"
            extension = SubElement(track, "extension", application="http://www.videolan.org/vlc/playlist/0")
            SubElement(extension, "vlc:id").text = str(i)

    with open(playlist_file, "wb") as f:
        # f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        # root.write(f, encoding="utf-8", xml_declaration=True)
        ElementTree(root).write(f, encoding="utf-8", xml_declaration=True)

# Example usage
base_path = os.path.dirname(os.path.abspath(__file__))
parent_folders = [os.path.join(base_path, d) for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]

for folder_path in parent_folders:
    playlist_file = f"{folder_path}_playlist.xspf"
    write_playlist(folder_path, playlist_file)
