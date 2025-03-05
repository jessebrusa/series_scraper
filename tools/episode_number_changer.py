import os
import re

class EpisodeNumberChanger:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        print(f"Processing folder {folder_path}")

    def collect_files(self):
        files = []
        for filename in os.listdir(self.folder_path):
            files.append(filename)
        return files

    def change_episode_numbers(self, change_value):
        print(f"Changing episode numbers by {change_value}")
        files = self.collect_files()

        # Sort files based on episode number
        files.sort(key=lambda f: int(re.search(r's\d+e(\d+)', f).group(1)), reverse=(change_value > 0))

        for filename in files:
            print(f"Processing file {filename}")
            match = re.search(r'(.*?s)(\d+)(e)(\d+)(.*)', filename)
            if match:
                prefix, season_number, separator, episode_number, suffix = match.groups()
                try:
                    season_number = int(season_number)
                    episode_number = int(episode_number)
                    new_season_number = f"{season_number:02d}"
                    new_episode_number = f"{episode_number + change_value:02d}"
                    new_filename = f"{prefix}{new_season_number}{separator}{new_episode_number}{suffix}"
                    new_filepath = os.path.join(self.folder_path, new_filename)
                    if not os.path.exists(new_filepath):
                        os.rename(os.path.join(self.folder_path, filename), new_filepath)
                        print(f"Renamed {filename} to {new_filename}")
                    else:
                        print(f"Skipping renaming {filename} to {new_filename} as it already exists.")
                except ValueError:
                    print(f"Skipping file {filename} as it does not have a valid episode number.")
            else:
                print(f"Skipping file {filename} as it does not match the expected pattern.")

    def replace_hyphen_with_zero(self):
        print("Replacing '-' with '0' in filenames")
        files = self.collect_files()
        for filename in files:
            if '-' in filename:
                new_filename = filename.replace('-', '0')
                new_filepath = os.path.join(self.folder_path, new_filename)
                if not os.path.exists(new_filepath):
                    os.rename(os.path.join(self.folder_path, filename), new_filepath)
                    print(f"Renamed {filename} to {new_filename}")
                else:
                    print(f"Skipping renaming {filename} to {new_filename} as it already exists.")

if __name__ == '__main__':
    folder_path = r'E:\Anime\Boruto Naruto Next Generations\Season 01'
    changer = EpisodeNumberChanger(folder_path)
    changer.change_episode_numbers(-2)
    changer.replace_hyphen_with_zero()