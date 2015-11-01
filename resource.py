import threading
import html
import bs4
import sys

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

  def __init__(self, name, fetch_xml, selector, tag_to_cache_repr=str, format_tag=str, tag_sort_key=None):
    self.name = name
    self.fetch_xml = fetch_xml
    self.selector = selector
    self.tag_to_cache_repr = tag_to_cache_repr
    self.tag_sort_key = tag_sort_key
    self.format_tag = format_tag

  def fetch_elements(self):
    return bs4.BeautifulSoup(self.fetch_xml(), 'html.parser').select(self.selector)

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

  def fetch_and_update_cache_and_summarize(self, cache):
    current_elements = self.fetch_elements()
    new_elements = self.select_new_elements(cache, current_elements)
    self.update_cache(cache, current_elements)
    if self.tag_sort_key:
      new_elements.sort(key=self.tag_sort_key)

    return self.summarize(new_elements)

import datetime
RSS_TIME_FORMAT = '%a, %d %b %Y %H:%M:%S %z'
class RSSResource(Resource):
  def __init__(self, **kwargs):
    super().__init__(
      selector='item',
      tag_to_cache_repr=self._tag_to_cache_repr,
      format_tag=self._format_tag,
      tag_sort_key=self._tag_sort_key,
      **kwargs)

  @staticmethod
  def _tag_to_cache_repr(tag):
    return tag.guid.text if tag.guid is not None else tag.title

  @staticmethod
  def _format_tag(tag):
    description = ('' if tag.description is None else
                   html.unescape(''.join(str(e) for e in tag.description)))
    return '<h2><a href="{link}">{title}</a></h2> {description}'.format(
      link=tag.link.text,
      title=tag.title.text,
      description=description)

  @staticmethod
  def _tag_sort_key(tag):
    return (datetime.datetime.now() if tag.pubdate is None else
            datetime.datetime.strptime(tag.pubdate.text, RSS_TIME_FORMAT))
