from . import ElementSetResource

def tweet_text(tag):
  return tag.text

def format_tweet(tag):
  return '<p>{}</p>'.format(tag.text)

class TwitterResource(ElementSetResource):
  def __init__(self, username, **kwargs):
    super().__init__(
      url='twitter.com/{}'.format(username),
      selector='.tweet-text',
      tag_to_cache_repr=tweet_text,
      format_tag=format_tweet,
      **kwargs)
