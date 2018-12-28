from pathlib import Path
from glob import glob
from render_engine.content import (
        BlogPost, 
        MicroBlogPost,
        Page,
        PodcastEpisode,
        )
from render_engine.feeds import path_crawler
import config
from dataclasses import dataclass

@dataclass
class path:
    name: str
    content_type: Page
    content_path: Path
    output_path: Path

pages = path(
        name = 'pages',
        content_type = Page,
        content_path = Path('content/pages'),
        output_path = Path('output/pages'),
        )

blog = path(
        name = 'blog',
        content_type = BlogPost,
        content_path = Path('content'),
        output_path = Path('output/blog'),
        )

microblog = path(
        name = 'microblog',
        content_type = MicroBlogPost,
        content_path = Path('content/microblog'),
        output_path = Path('output/microblog'),
        )

podcast = path(
        name = 'podcast',
        content_type = PodcastEpisode,
        content_path = Path('content/podcast'),
        output_path = Path('output/podcast'),
        )

PATHS = (pages, blog, podcast, microblog)

def build():
    for p in PATHS:
        file_path = p.content_path
        files = path_crawler(item_type=p.content_type, file_path=file_path) 
        for i in files:
            with open(f'{p.output_path}/{i.id}.html', 'w') as f:
                f.write(i.html) 

if __name__ == '__main__':
    build()