import tkinter as tk
from tkinter import filedialog
import os

class Rename:
    def __init__(self, old_name, new_name):
        self.old_name = old_name
        self.new_name = new_name
        self.directory = None

    def ask_directory(self, skip=False):
        if skip:
            self.directory = '/Volumes/Plex Movies and Shows/Anime/Avatar The Last Airbender/Season 02'
            return
        root = tk.Tk()
        root.withdraw()
        self.directory = filedialog.askdirectory(title="Select Directory")
        root.destroy()

    def collect_files(self, skip=False):
        if skip:
            self.files = ['s01e02.mp4', 's01e03.mp4', 's01e04.mp4', 's01e05.mp4', 's01e06.mp4', 's01e07.mp4', 's01e08.mp4', 's01e09.mp4', 's01e10.mp4', 's01e11.mp4', 's01e12.mp4', 's01e13.mp4', 's01e14.mp4', 's01e15.mp4', 's01e16.mp4', 's01e17.mp4', 's01e18.mp4', 's01e19.mp4', 's02e01.mp4']
            return
        if not self.directory:
            raise ValueError("Directory not set. Please call ask_directory() first.")
        self.files = [f for f in os.listdir(self.directory) if os.path.isfile(os.path.join(self.directory, f))]

    def ask_season(self, skip=False):
        if skip:
            self.season = '02'
            return
        season = tk.simpledialog.askstring("Input", "Please enter the season number:")
        if season is None:
            raise ValueError("Season number not provided.")
        self.season = season

    def ask_episode(self, skip=False):
        if skip:
            self.episode = None
        episode = tk.simpledialog.askstring("Input", "Please enter the episode number:")
        self.episode = episode

    def format_name(self, file, skip=False):
        if skip:
            return 's01e02.mp4'
        parts = file.split('e')
        if len(parts) != 2:
            raise ValueError(f"Unexpected file format: {file}")
        episode_part = parts[1]
        new_file_name = f"s{self.season.zfill(2)}e{episode_part}"
        return new_file_name

    def rename_files(self):
        for file in self.files:
            new_name = self.format_name(file)
            old_file_path = os.path.join(self.directory, file)
            new_file_path = os.path.join(self.directory, new_name)
            os.rename(old_file_path, new_file_path)

    def main(self):
        self.ask_directory(skip=False)
        self.collect_files(skip=False)
        self.ask_season()
        self.ask_episode()
        self.rename_files()

if __name__ == "__main__":
    rename = Rename(old_name="old_name_placeholder", new_name="new_name_placeholder")
    rename.main()