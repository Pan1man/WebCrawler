class Url:
    def __init__(self, url: str, priority: int):
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

    def __init__(self):
        self.queue = []

    def add_url(self, url: Url):
        self.queue.append(url)

    def remove_url(self) -> str:
        max_priority = self.queue[0]
        for url in self.queue:
            if url.priority > max_priority.priority:
                max_priority = url

        self.queue.remove(max_priority)
        return max_priority.url







