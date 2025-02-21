import os

class FileManager:
    def __init__(self):
        self.mount_point = "/Volumes/Plex Movies and Shows/Anime"

    def write_file(self, file_path, data):
        full_path = os.path.join(self.mount_point, file_path)
        with open(full_path, 'wb') as file:
            file.write(data)


if __name__ == "__main__":
    file_manager = FileManager()
    file_manager.write_file("example.txt", b"Hello, NAS!")

