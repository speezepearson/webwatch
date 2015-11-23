import html
from . import ElementSetResource

def entry_guid(tag):
  return tag.id.text if tag.id else tag.title.text if tag.title else str(tag)

def format_entry(tag):
    content = ('' if tag.content is None else
               html.unescape(''.join(str(e) for e in tag.content)))
    return '<h2><a href="{link}">{title}</a></h2> {content}'.format(
      link=tag.link["href"],
      title=tag.title.text,
      content=content)

def entry_published_date(tag):
  return ('' if tag.published is None else tag.published.text)

class AtomResource(ElementSetResource):
  def __init__(self, **kwargs):
    super().__init__(
      selector='entry',
      tag_to_cache_repr=entry_guid,
      format_tag=format_entry,
      tag_sort_key=entry_published_date,
      **kwargs)
