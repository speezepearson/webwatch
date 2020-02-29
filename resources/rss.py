import html
import dateutil.parser
from . import ElementSetResource

RSS_TIME_FORMAT = '%a, %d %b %Y %H:%M:%S %z'

def item_guid(tag):
  return tag.guid.text if tag.guid else tag.title.text if tag.title else str(tag)

def format_item(tag):
    content = ('' if tag.description is None else
               html.unescape(''.join(str(e) for e in tag.description)))
    return '<h2><a href="{link}">{title}</a></h2> {content}'.format(
      link=tag.link.text,
      title=tag.title.text,
      content=content)

def item_published_date(tag):
  if tag.pubdate is None:
    return datetime.datetime.now()
  return dateutil.parser.parse(tag.pubdate.text)

class RSSResource(ElementSetResource):
  def __init__(self, **kwargs):
    super().__init__(
      selector='item',
      tag_to_cache_repr=item_guid,
      format_tag=format_item,
      tag_sort_key=item_published_date,
      **kwargs)
