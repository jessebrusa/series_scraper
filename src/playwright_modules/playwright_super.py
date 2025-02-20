class PlaywrightSuper:
    def click(self, selector: str):
        self.page.click(selector)

    def type_input(self, selector: str, text: str):
        self.page.type(selector, text)

    def get_selector(self, selector: str):
        return self.page.query_selector(selector)

    def collect_selectors(self, selector: str):
        return self.page.query_selector_all(selector)

    def get_page(self):
        return self.page
    
    def get_browser(self):
        return self.browser
    
    def get_playwright(self):
        return self.playwright  
    
    def close_browser(self):
        self.browser.close()