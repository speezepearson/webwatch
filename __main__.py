import os
import shelve
import argparse
import difflib
import html

from webwatch import soup, get_html, get_plain, update_cache_and_return_diff, update_cache_and_return_new_rss_items

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=os.path.join(os.environ['HOME'], '.fetchstuff-cache'))
args = parser.parse_args()

def submain(cache, name, soup):
  new_items = update_cache_and_return_new_rss_items(cache, name, soup)
  if new_items:
    print('<h1>', name, '</h1>')
    for item in new_items:
      print('<article><h2><a href="{link}">{title}</a></h2></article>'.format(
        link=item.link.text, title=item.title.text))
      print(html.unescape(''.join(str(e) for e in item.description.contents)))

with shelve.open(args.cache) as cache:
  submain(cache, 'xkcd', soup(get_html('xkcd.com', '/rss.xml')))
  submain(cache, 'Girl Genius', soup(get_html('girlgeniusonline.com', '/ggmain.rss')))
  submain(cache, 'Gunnerkrigg Court', soup(get_html('gunnerkrigg.com', '/rss.xml')))
  submain(cache, 'SMBC', soup(get_html('smbc-comics.com', '/rss.php')))
  submain(cache, 'Dinosaur Comics', soup(get_html('www.qwantz.com', '/rssfeed.php')))
  submain(cache, 'Dr. McNinja', soup(get_plain('drmcninja.com', '/feed')))

  e = soup(get_html('courses.cs.washington.edu', '/courses/cse505/15au/'))
  old_cache_value = cache.get('CS 505 Autumn 2015', '')
  if update_cache_and_return_diff(cache, 'CS 505 Autumn 2015', str(e)):
    print('<h1>CS 505 Autumn 2015</h1>')
    import difflib
    import html
    old_lines = old_cache_value.split('\n')
    new_lines = str(e).split('\n')
    diff = list(difflib.unified_diff(old_lines, new_lines))
    print('<pre>' + html.escape('\n'.join(diff)) + '</pre>')

  # NOPE! Schneier is Atom, not RSS.
  # submain(cache, 'Schneier', get_kwargs=dict(domain='www.schneier.com', path='/feed', secure=True))
  articles = soup(get_html('www.schneier.com', secure=True)).select('.article')
  articles_by_title = {article.select('h2.entry')[0].text: article for article in articles}
  new_titles = update_cache_and_return_diff(
    cache, 'Schneier', set(articles_by_title.keys()),
    diff=(lambda old_titles, current_titles: current_titles if old_titles is None else current_titles-old_titles))
  if new_titles:
    print('<h1>Schneier</h1>')
    for title in new_titles:
      print(articles_by_title[title])
