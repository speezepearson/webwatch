import os
import shelve
import argparse
import difflib
import html
import datetime

from webwatch import fetcher, Resource, RSSResource, run_resources

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=os.path.join(os.environ['HOME'], '.fetchstuff-cache'))
args = parser.parse_args()

rss_resources =[
  RSSResource(name=name, fetch_xml=fetcher(url))
  for name, url in [
    ('xkcd', 'xkcd.com/rss.xml'),
    ('Girl Genius', 'girlgeniusonline.com/ggmain.rss'),
    ('Gunnerkrigg Court', 'gunnerkrigg.com/rss.xml'),
    ('SMBC', 'smbc-comics.com/rss.php'),
    ('Dinosaur Comics', 'www.qwantz.com/rssfeed.php'),
    ('Dr. McNinja',  'drmcninja.com/feed'),
    ('Invisible Bread', 'feeds.feedburner.com/InvisibleBread'),
    ('Awkward Zombie', 'awkwardzombie.com/awkward.php'),
    ('Questionable Content', 'questionablecontent.net/QCRSS.xml'),
    ('Sam and Fuzzy',  'www.samandfuzzy.com/feed')]]

all_resources = rss_resources + [
  Resource(
    name="CS 505",
    fetch_xml=fetcher('courses.cs.washington.edu/courses/cse505/15au/'),
    selector='p'),
  Resource(
    name='Schneier on Security',
    fetch_xml=fetcher('https://www.schneier.com'),
    selector='.article',
    tag_to_cache_repr=(lambda t: t.h2.text)),
  Resource(
    name="W|A Can't",
    fetch_xml=fetcher('twitter.com/wacnt'),
    selector='.tweet-text',
    tag_to_cache_repr=(lambda t: t.text),
    format_tag=(lambda t: '<p>'+t.text+'</p>'))]

with shelve.open(args.cache) as cache:
  run_resources(cache, all_resources)
