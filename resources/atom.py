import html
from . import Resource

class AtomResource(Resource):
  def __init__(self, **kwargs):
    super().__init__(
      selector='entry',
      tag_to_cache_repr=self._tag_to_cache_repr,
      format_tag=self._format_tag,
      tag_sort_key=self._tag_sort_key,
      **kwargs)

  @staticmethod
  def _tag_to_cache_repr(tag):
    return tag.id.text if tag.id is not None else tag.title.text

  @staticmethod
  def _format_tag(tag):
    content = ('' if tag.content is None else
               html.unescape(''.join(str(e) for e in tag.content)))
    return '<h2><a href="{link}">{title}</a></h2> {content}'.format(
      link=tag.link["href"],
      title=tag.title.text,
      content=content)

  @staticmethod
  def _tag_sort_key(tag):
    return ('' if tag.published is None else tag.published.text)
