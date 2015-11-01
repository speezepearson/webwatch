import argparse
import os
import sys
import shelve

from webwatch import Resource, RSSResource, unsafe_parse_config, fetch_and_update_cache_and_summarize_in_parallel

DEFAULT_CACHE_PATH = os.path.join(os.environ['HOME'], '.webwatch-cache')
DEFAULT_CONFIG_PATH = os.path.join(os.environ['HOME'], '.webwatch-resources.ini')

example_ini = '''
[xkcd]
class = RSSResource
url = "xkcd.com/rss.xml"

[Schneier on Security]
url = "https://www.schneier.com"
selector = ".article"
tag_to_cache_repr = lambda t: t.h2.text

[W|A Can't]
url = "twitter.com/wacnt"
selector = ".tweet-text"
tag_to_cache_repr = lambda t: t.text
format_tag = lambda t: '<p>'+t.text+'</p>'
'''

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=DEFAULT_CACHE_PATH)
parser.add_argument('--resources', default=DEFAULT_CONFIG_PATH)
args = parser.parse_args()

if args.resources == DEFAULT_CONFIG_PATH and not os.path.exists(DEFAULT_CONFIG_PATH):
  print('Creating example resource-definition file in {}'.format(DEFAULT_CONFIG_PATH), file=sys.stderr)
  with open(DEFAULT_CONFIG_PATH, 'w') as f:
    f.write(example_ini)

resources = unsafe_parse_config(args.resources)
with shelve.open(args.cache) as cache:
  print(fetch_and_update_cache_and_summarize_in_parallel(cache, resources))
