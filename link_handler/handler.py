import requests

class FuckingFast():
    def __init__(self, url: str) -> None:
        self._substring: str = "https://fuckingfast.co/dl/"
        self._url = url
    
    def crawl(self) -> None:
        response = requests.get(self._url)
        for line in response.text.split("\n"):
            if self._substring in line:
                print(line.split("\"")[1])

    def write(self) -> None:
        # TODO
        # implement writing to file capability
        pass

class DataNodes(FuckingFast):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self._substring: str = "https://datanodes.io/"
    
    def crawl(self) -> None:
        print(f"{self._url}")