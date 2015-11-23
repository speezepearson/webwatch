import shelve
import argparse
import os

from .threadsafe import fetch_and_diff_in_parallel

DEFAULT_CACHE_PATH = '~/.webwatch-cache'

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=os.path.expanduser(DEFAULT_CACHE_PATH), help='file to store old versions of resources in')
parser.add_argument('--only', default=None, type=(lambda s: set(s.split(','))), help='comma-separated list of resources; exclude unnamed resources')
parser.add_argument('--no-cache-write', action="store_false", dest="update_cache")


def main(*resources, command_line_args=None):
  args = parser.parse_args(command_line_args)

  if args.only is not None:
    resources = [r for r in resources if r.name in args.only]

  with shelve.open(args.cache) as cache:
    print(fetch_and_diff_in_parallel(cache, resources, update_cache=args.update_cache))
