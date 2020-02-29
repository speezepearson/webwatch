import abc
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

class Resource(metaclass=abc.ABCMeta):
  def __init__(self, name, **kwargs):
    self.name = name
    super().__init__(**kwargs)

  @abc.abstractmethod
  def fetch(self, old_cache_value):
    pass

  @abc.abstractmethod
  def new_cache_value(self, old_cache_value, current_data):
    pass

  @abc.abstractmethod
  def diff(self, old_cache_value, current_data):
    pass

  def fetch_and_diff(self, cache, update_cache=True):
    old = cache.get(self.name)
    new = self.fetch(old)
    if update_cache:
      cache[self.name] = self.new_cache_value(old, new)
    diff = self.diff(old, new)
    return '<h1>{name}</h1> {diff}'.format(name=self.name, diff=diff) if diff else ''



class ElementSetResource(Resource):
  def __init__(self, url, selector, tag_to_cache_repr=str, format_tag=str, tag_sort_key=None, **kwargs):
    self.url = url
    self.selector = selector
    self.tag_to_cache_repr = tag_to_cache_repr
    self.tag_sort_key = tag_sort_key
    self.format_tag = format_tag
    super().__init__(**kwargs)

  def fetch(self, old_cache_value):
    html = fetch(self.url)
    soup = bs4.BeautifulSoup(html, 'html.parser')
    remove_global_effects(soup)
    return soup.select(self.selector)

  def new_cache_value(self, old_cache_value, new_elements):
    return set(self.tag_to_cache_repr(e) for e in new_elements)

  def diff(self, old_cache_value, current_data):
    if old_cache_value is None:
      old_cache_value = set()

    new_elements = [e for e in current_data if self.tag_to_cache_repr(e) not in old_cache_value]

    if self.tag_sort_key is not None:
      new_elements.sort(key=self.tag_sort_key)

    return '\n'.join(self.format_tag(e) for e in new_elements)

from .atom import AtomResource
from .rss import RSSResource
from .tumblr import TumblrResource
from .twitter import TwitterResource
