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
class = TwitterResource
username = 'wacnt'
'''

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=DEFAULT_CACHE_PATH, help='file to store old versions of resources in')
parser.add_argument('--resources', default=DEFAULT_CONFIG_PATH, help='config file describing resources to fetch')
parser.add_argument('--only', default=None, type=(lambda s: set(s.split(','))), help='comma-separated list of resources; exclude unnamed resources')
args = parser.parse_args()

if args.resources == DEFAULT_CONFIG_PATH and not os.path.exists(DEFAULT_CONFIG_PATH):
  print('Creating example resource-definition file in {}'.format(DEFAULT_CONFIG_PATH), file=sys.stderr)
  with open(DEFAULT_CONFIG_PATH, 'w') as f:
    f.write(example_ini)

resources = unsafe_parse_config(args.resources)
if args.only is not None:
  resources = [r for r in resources if r.name in args.only]

with shelve.open(args.cache) as cache:
  print(fetch_and_update_cache_and_summarize_in_parallel(cache, resources))
