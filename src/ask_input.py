class AskInput:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def ask_media_type(self):
        media_list = ['Anime', 'TV Show', 'Movie']
        media_type = (int(input('Type Number Of Media Type: \n1. Anime\n2. TV Show\n3. Movie\n4. Cancel\nChoose a media type: '))-1)
        if 0 <= media_type < len(media_list):
            self.data_manager.set_media_type(media_list[media_type])
        
        return self.data_manager.get_media_type() is not None
    
    def ask_title(self):
        title = input('Enter Title: ')
        if title:
            return title
        return None
    
    def ask_series_title(self):
        title_list = self.data_manager.get_searched_titles()
        options = '\n'.join([f"{i+1}. {title['title']}" for i, title in enumerate(title_list)])
        options += f"\n{len(title_list)+1}. Cancel"
        choice = int(input(f'Type Number Of Series Title: \n{options}\nChoose a series title: ')) - 1
        if 0 <= choice < len(title_list):
            self.data_manager.set_series_title(title_list[choice]['title'])
            self.data_manager.set_series_url(title_list[choice]['href'])
            return title_list[choice]['title']
        return None