import datetime
import html
from . import Resource

_RSS_TIME_FORMAT = '%a, %d %b %Y %H:%M:%S %z'

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
    return tag.guid.text if tag.guid is not None else tag.title.text

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
            datetime.datetime.strptime(tag.pubdate.text, _RSS_TIME_FORMAT))
