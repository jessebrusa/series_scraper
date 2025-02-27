import os

# Define the file path
file_path = r'C:/storage/Python/series_scraper/data/anime/Black Clover.json'
new_file_path = r'C:/storage/Python/series_scraper/data/anime/Black Clover_format.json'

# Read the content of the file
with open(file_path, 'r') as file:
    content = file.read()

# Replace single quotes with double quotes
modified_content = content.replace("'", '"')

# Write the modified content back to the file
with open(new_file_path, 'w') as file:
    file.write(modified_content)


print(f"Replaced all single quotes with double quotes in {file_path}")