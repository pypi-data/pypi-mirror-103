# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline


class VideoPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        custom_dir = item.dir or 'videos'
        orig_name = request.url.rsplit('/', 1)[1]
        return f'{custom_dir}/{orig_name}'


