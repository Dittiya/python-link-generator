import requests

class FuckingFast():
    def __init__(self, url: str) -> None:
        self._substring: str = "https://fuckingfast.co/dl/"
        self._url = url
    
    def crawl(self) -> None:
        response = requests.get(self._url)
        for line in response.text.split("\n"):
            if self._substring in line:
                return line.split("\"")[1]

class Datanodes(FuckingFast):
    def __init__(self, url: str) -> None:
        super().__init__(url)
        self._substring: str = "https://datanodes.to/"
        self._host: str = "https://datanodes.to/download"
        self._content_type: str = "application/x-www-form-urlencoded"
        # self._body: str = "op=download2&id="
    
    def crawl(self) -> None:
        # obtain id from web url
        id = self._url.split("/")[3]

        # make a POST request with payload
        headers = {"POST /download HTTP/2": "","Content-Type": self._content_type}
        data = {"op":"download2", "id": id}
        response = requests.post(self._host, headers=headers, data=data, allow_redirects=False)
        
        return response.headers["location"]