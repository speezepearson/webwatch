from . import RSSResource

class TumblrResource(RSSResource):
  def __init__(self, username, **kwargs):
    self.username = username
    super().__init__(
      name='{}.tumblr.com'.format(username),
      url='http://{}.tumblr.com/rss'.format(username),
      **kwargs)
