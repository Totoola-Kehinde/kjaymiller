"""
Step 1 - Scans the content folder for '.md' and '.markdown' files

Step 2 - Check 'blog/'filename'.html' for already processed files.

Step 3a - If 2 == False, Parse Markdown and Save as blog/filename.html
Step 3b - If 2 == True, Skip and go to the next file
"""

from blog_engine.render_post import render_post
from pathlib import Path
import json
import arrow
import string


class JSON_Feed():
    def __init__(content_path, title=True):
        self.content_path = Path(content_path).glob('*.md')
        self.json_object = __add_json_content__(title)

    def sorted_items(self, json_object, item_count):
        latest = sorted(json_object,
                        key=lambda x:
                        arrow.get(json_object[x]['date_published']),
                        reverse=True)[:item_count]
        return [json_object[x] for x in latest]

    def __add_json_content__(self, content_path, title=True):
        json_object = {}
        for md_file in content_path:
            metadata = render_post(md_file, title=title)
            json_object[metadata['slug']] = metadata
        return json_object

class Blog(JSON_Feed):
    def __init__(self, content_path, title=True, **kwargs):
        super().__init__(content_path, title)
        if all([kwargs.get(json_base),
                kwargs.get(json_filename),
                kwargs.get(json_title)]):
            self.json_file = self.create_feed(json_base, json_filename, json_title)

    def create_feed(self, json_base, title):
        with open(json_base) as f:
            feed = json.load(f)
        feed['title'] = title
        sorted_items = sorted(self.json_object,
                    key=lambda x:
                    arrow.get(self.json_object[x]['date_published']),
                    reverse=True)
        feed['items'] = sorted_items
        return feed


    def write_feed(self, feed, filename):
        with open(f'static/{filename}', 'w') as outfile:
            json.dump(feed, outfile)
            outfile.truncate()


class MicroBlog(Blog):
    def __init__(self, content_path, **kawrgs):
        super().__init__(content_path, kwargs, title=False,)
        self.json_object = self.add_json_content(self.content_path, title=True)
