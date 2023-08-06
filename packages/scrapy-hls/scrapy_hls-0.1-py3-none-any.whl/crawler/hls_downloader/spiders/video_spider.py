import scrapy
from dataclasses import dataclass
from typing import List
from scrapy import signals

from ..utils.merge_ts import MergeUtil
from ..utils.m3u8_parser import Parser
import os


@dataclass
class VideoItem:
    file_urls: List[str]
    dir: str


class VideoSpider(scrapy.Spider):
    name = "video"

    def __init__(self, m3u8, video_name, *args, **kwargs):
        if not m3u8 or not video_name:
            raise ValueError('m3u8 and video_name needs to be provided as parameters')
        super().__init__(*args, **kwargs)
        self.video_name = video_name or 'video-download'

        self.start_urls = [m3u8]

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.on_finish, signal=signals.spider_closed)
        return spider

    def parse(self, response, **kwargs):
        content = response.body.decode('utf8')
        print(content)
        base_uri = response.url.rsplit('/', 1)[0]
        video_urls = Parser.parse(content, base_uri)

        return VideoItem(file_urls=video_urls, dir=self.video_name)

    def on_finish(self):
        base_path = self.crawler.settings.get('FILES_STORE')
        source_path = os.path.join(base_path, self.video_name)
        target_path = os.path.join(base_path, self.video_name + '_merge')
        MergeUtil.merge(source_path, target_path, f'{self.video_name}.ts')
        sub_proc = MergeUtil.convert_to_mp4(os.path.join(target_path, f'{self.video_name}.ts'),
                                 os.path.join(target_path, f'{self.video_name}.mp4'))

        for line in sub_proc.stdout.decode('utf8').split('\n'):
            print(line)
