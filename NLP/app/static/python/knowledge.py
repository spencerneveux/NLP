class Knowledge:
    def __init__(self):
        self.name: str = ""
        self.desc: str = ""
        self.url: str = ""
        self.article_body: str = ""

    def get_name(self):
        return self.name

    def get_desc(self):
        return self.desc

    def get_url(self):
        return self.url

    def get_article_body(self):
        return self.article_body

    def set_name(self, name:str):
        self.name = name

    def set_desc(self, desc:str):
        self.desc = desc

    def set_url(self, url:str):
        self.url = url

    def set_article_body(self, body:str):
        self.article_body = body

    def __str__(self):
        return f"{self.name} - {self.desc} - {self.url} - {self.article_body}"