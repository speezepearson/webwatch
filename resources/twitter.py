from . import Resource

class TwitterResource(Resource):
  def __init__(self, username, **kwargs):
    super().__init__(
      url='twitter.com/{}'.format(username),
      selector='.tweet-text',
      tag_to_cache_repr=(lambda t: t.text),
      format_tag=(lambda t: '<p>{}</p>'.format(t.text)),
      **kwargs)
