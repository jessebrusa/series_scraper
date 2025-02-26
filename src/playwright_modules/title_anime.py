class TitleAnime:
    def __init__(self, page):
        self.page = page

    def search_title(self, title):
        input_selector = '#searchbox'
        self.page.wait_for_selector(input_selector)
        self.page.fill(input_selector, title)

        submit_button = '#konuara > div > input[type=submit]'
        self.page.wait_for_selector(submit_button)
        self.page.click(submit_button)

    def collect_titles(self):
        title_selector = '.aramadabaslik a'
        self.page.wait_for_selector(title_selector)

        title_selector_list = self.page.query_selector_all(title_selector)

        searched_titles = []
        for title in title_selector_list:
            searched_titles.append({
                'title': title.text_content().strip(),
                'href': title.get_attribute('href')
            })
        
        return searched_titles  
