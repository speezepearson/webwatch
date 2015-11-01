import os
import shelve
import argparse
import difflib
import html
import datetime

from webwatch import soup, get_html, get_plain, update_cache_and_return_diff, update_cache_and_return_new_set_items

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=os.path.join(os.environ['HOME'], '.fetchstuff-cache'))
args = parser.parse_args()

def main_for_set(cache, name, items, cache_repr=None, sort_key=None, format=None):
  if format is None:
    format = (lambda x: x)
  new_items = list(update_cache_and_return_new_set_items(cache, name, items, cache_repr=cache_repr))
  if sort_key is not None:
    new_items.sort(key=sort_key)
  if new_items:
    print('<h1>', name, '</h1>')
    for item in new_items:
      print(format(item))

def main_for_rss(cache, name, soup, limit=10):
  main_for_set(
    cache, name, soup.select('item')[:limit],
    cache_repr=(lambda item: (item.guid.text if item.guid else item.title.text)),
    sort_key=(lambda item: datetime.datetime.strptime(item.pubdate.text, '%a, %d %b %Y %H:%M:%S %z') if item.pubdate else datetime.datetime.now()),
    format=(lambda item: '<h2><a href="{link}">{title}</a></h2> {body}'.format(
      link=item.link.text, title=item.title.text, body=html.unescape(''.join(str(e) for e in item.description.children)) if item.description else '')))

with shelve.open(args.cache) as cache:
  main_for_rss(cache, 'xkcd', soup(get_html('xkcd.com', '/rss.xml')))
  main_for_rss(cache, 'Girl Genius', soup(get_html('girlgeniusonline.com', '/ggmain.rss')))
  main_for_rss(cache, 'Gunnerkrigg Court', soup(get_html('gunnerkrigg.com', '/rss.xml')))
  main_for_rss(cache, 'SMBC', soup(get_html('smbc-comics.com', '/rss.php')))
  main_for_rss(cache, 'Dinosaur Comics', soup(get_html('www.qwantz.com', '/rssfeed.php')))
  main_for_rss(cache, 'Dr. McNinja', soup(get_plain('drmcninja.com', '/feed')))
  main_for_rss(cache, 'Invisible Bread', soup(get_plain('feeds.feedburner.com', '/InvisibleBread')))
  main_for_rss(cache, 'Awkward Zombie', soup(get_html('awkwardzombie.com', '/awkward.php')))
  main_for_rss(cache, 'Questionable Content', soup(get_html('questionablecontent.net', '/QCRSS.xml')))
  main_for_rss(cache, 'Sam And Fuzzy', soup(get_html('www.samandfuzzy.com', '/feed')))

  ps = soup(get_html('courses.cs.washington.edu', '/courses/cse505/15au/')).select('p')
  main_for_set(
    cache, 'CS 505 Autumn 2015', ps,
    cache_repr=str,
    sort_key=ps.index)

  articles = soup(get_html('www.schneier.com', secure=True)).select('.article')
  main_for_set(
    cache, 'Schneier', articles,
    cache_repr=(lambda article: article.select('h2.entry')[0].text))

  texts = [
    element.text for element in
    soup(get_plain('twitter.com', '/wacnt')).select('.tweet-text')]
  main_for_set(
    cache, "W|A Can't", texts,
    format=(lambda text: '<p>{}</p>'.format(html.escape(text))))
