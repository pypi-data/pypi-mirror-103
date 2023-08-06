import os
import m3u8
from typing import List

class Parser:
    @classmethod
    def parse(cls, content: str, host: str) -> List[str]:

        playlist = m3u8.loads(content)
        return [os.path.join(host, segment) for segment in playlist.segments.uri]


# uri = 'https://fdc.91p49.com/m3u8/457298/457298.m3u8'
# print(Parser.parse(uri))
