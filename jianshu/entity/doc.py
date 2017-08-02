class Doc:
    title = ''
    score = 0
    time = ''
    url = ''
    snippet = ''
    recommend = []

    def __init__(self, title, score, time, url, snippet, recommend):
        self.title = title
        self.score = score
        self.time = time
        self.url = url
        self.snippet = snippet
        self.recommend = recommend
