"""
Generates the files to build out your HTML Path
"""
import os
import shutil
from writer import write_page
import paginate
from pathlib import Path
from render_engine.content import (
        BlogPost, 
        MicroBlogPost,
        Page,
        PodcastEpisode,
        )
# from render_engine.feeds import PathCrawler
import config

def remove_path(path):
    # Remove output directory if it exists
    try:
        shutil.rmtree(path.output_path)
    except:
        pass
    
def gen_static():
    static_path = Path(config.STATIC_PATH)
    shutil.copytree(static_path, Path(f'{config.OUTPUT_PATH}/static'))

def generate(path):
    # Create Static Files
    remove_path(path)
    file_path = Path(f'{config.OUTPUT_PATH}/{path.output_path}')
    file_path.mkdir(parents=True)
    files = [item for item in path.content_path.glob(f'*{path.extension}')]
    page_dict = path.__dict__

    # write page
    pages = []
    for i in files:
        page = path.content_type(base_file=i)
        write_page(f'{path.output_path}/{page.id}', page.html)
        pages.append(page) 
    
    page_dict['pages'] = pages
    
    if path.paginate:
        paginate.write_paginated_pages(
                name = path.name, 
                pagination = paginate.paginate(pages, 10), 
                template = 'blog_list.html', 
                post_list=pages) 

    if path.categories:
        page_dict['categories'] = set((p._category for p in pages))
         
    
    if path.categories:
        page_dict['tags'] = set()
        for p in pages:
            page_dict['tags'].update(set((tag for tag in p.tags)))
            

    return page_dict
