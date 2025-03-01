import requests

class ScanLibrary:
    def __init__(self):
        self.plex_server_url = 'http://192.168.111.200:32400'
        self.plex_token = 'H-TkG8ZfEBMZWzMkNyJo'

    def scan_library(self, library_section_id):
        headers = {
            'X-Plex-Token': self.plex_token
        }
        url = f'{self.plex_server_url}/library/sections/{library_section_id}/refresh'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print(f'Successfully started scan for library section {library_section_id}.')
        else:
            print(f'Failed to start scan for library section {library_section_id}. Status code: {response.status_code}')

    def get_library_sections(self):
        headers = {
            'X-Plex-Token': self.plex_token
        }
        url = f'{self.plex_server_url}/library/sections'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            sections = response.json()['MediaContainer']['Directory']
            for section in sections:
                print(f"Library Name: {section['title']}, Library ID: {section['key']}")
        else:
            print(f'Failed to get library sections. Status code: {response.status_code}')


