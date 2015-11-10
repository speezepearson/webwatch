import bs4
from ..fetch import fetch

def remove_global_effects(element):
  for tag in list(element.find_all('style')):
    tag.extract()
  for tag in list(element.find_all('script')):
    tag.extract()
  for tag in list(element.find_all(True)):
    for attr in list(tag.attrs.keys()):
      if attr.startswith('on'):
        del tag.attrs[attr]

class Resource:
  '''
  Every resource has ways to:
  - fetch "the part we care about"
  - take that and the cached value and compute a diff
  - format the diff as HTML

  1. Fetch the part we care about.

     This is usually (always?) a set of XML tags. So:
     - fetch the raw XML
     - parse it
     - select the tags

     "Fetch the raw XML" might be any of:
     - plain urrlib.request.urlopen().read()
     - fancy HTTPConnection business with spoofed headers
     - Selenium

  2. Take that and the cached value and compute a diff.

     - Convert each tag in the set into a caching-friendly representation
     - Diff the reprset against the cached reprset, and update the cached reprset
     - Return the tags whose reprs are new

  3. Format the diff as HTML

     - Put the tags in some order
     - For each tag, print some function of it

  '''

  def __init__(self, name, url, selector, fetch_xml=fetch, tag_to_cache_repr=str, format_tag=str, tag_sort_key=None):
    self.name = name
    self.url = url
    self.selector = selector
    self.fetch_xml = fetch_xml
    self.tag_to_cache_repr = tag_to_cache_repr
    self.tag_sort_key = tag_sort_key
    self.format_tag = format_tag

  def fetch_elements(self):
    result = bs4.BeautifulSoup(self.fetch_xml(self.url), 'html.parser').select(self.selector)
    for element in result:
      remove_global_effects(element)
    return result

  def select_new_elements(self, cache, elements):
    return [
      e for e in elements
      if self.tag_to_cache_repr(e) not in cache.get(self.name, set())]

  def update_cache(self, cache, elements):
    cache[self.name] = set(self.tag_to_cache_repr(e) for e in elements)

  def summarize(self, new_elements):
    lines = []
    if new_elements:
      lines.append('<h1>{}</h1>'.format(self.name))
      for e in new_elements:
        lines.append(self.format_tag(e))
    return '\n'.join(lines)

  def fetch_and_summarize(self, cache, update_cache=False):
    current_elements = self.fetch_elements()
    new_elements = list(self.select_new_elements(cache, current_elements))

    if self.tag_sort_key:
      new_elements.sort(key=self.tag_sort_key)

    result = self.summarize(new_elements)

    if update_cache:
      self.update_cache(cache, current_elements)

    return result

from .atom import *
from .rss import *
from .twitter import *