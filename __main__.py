import argparse
import os
import shelve

from webwatch import Resource, RSSResource, unsafe_parse_config, fetch_and_update_cache_and_summarize_in_parallel

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=os.path.join(os.environ['HOME'], '.webwatch-cache'))
parser.add_argument('--resources', default=os.path.join(os.environ['HOME'], '.webwatch-resources.ini'))
args = parser.parse_args()

resources = unsafe_parse_config(args.resources)
with shelve.open(args.cache) as cache:
  print(fetch_and_update_cache_and_summarize_in_parallel(cache, resources))
