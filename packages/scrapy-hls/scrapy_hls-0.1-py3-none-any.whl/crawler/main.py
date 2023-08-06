from scrapy.cmdline import execute
import os


def run():
    os.chdir(os.path.dirname(__file__))
    url = input('mu3u8 url: ')
    name = input('video name: ')
    execute(argv=['scrapy', 'crawl', 'video', '-a', f'm3u8={url}', '-a', f'video_name={name}'])
