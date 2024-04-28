class Url:
    def __init__(self, url: str, priority: int = 5):
        self._url = url
        self._priority = priority

    @property
    def url(self) -> str:
        return self._url

    @url.setter
    def url(self, value: str):
        self._url = value

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, value: int):
        self._priority = value


class Frontier:

    def __call__(self):
        return url_frontier

    def __init__(self):
        self.queue = []

    def len(self):
        if not self.queue:
            return 0
        else:
            return len(self.queue)

    def add_url(self, url: str):
        formed_url = Url(url)
        self.queue.append(formed_url)

    def remove_url(self) -> str:
        max_priority = self.queue[0]
        for url in self.queue:
            if url.priority > max_priority.priority:
                max_priority = url

        self.queue.remove(max_priority)
        return max_priority.url


url_frontier = Frontier()

#url_frontier.add_url("https://www.iana.org/help/example-domains")
#url_frontier.add_url("https://www.rfc-editor.org/rfc/rfc2606.html")