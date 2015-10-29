import os
import shelve
import argparse
import difflib
import html

from webwatch import soup, get_html, update_cache_and_return_whether_changed

parser = argparse.ArgumentParser()
parser.add_argument('--cache', default=os.path.join(os.environ['HOME'], '.fetchstuff-cache'))
args = parser.parse_args()

with shelve.open(args.cache) as cache:
  e = soup(get_html('xkcd.com')).select('#comic img')[0]
  e['src'] = 'http:'+e['src']
  if update_cache_and_return_whether_changed(cache, 'xkcd', str(e)):
    print('<h1>xkcd</h1>')
    print(e)

  e = soup(get_html('girlgeniusonline.com', '/comic.php')).select('#comicbody img')[0]
  if update_cache_and_return_whether_changed(cache, 'Girl Genius', str(e)):
    print('<h1>Girl Genius</h1>')
    print(e)

  e = soup(get_html('gunnerkrigg.com')).select('.comic_image')[0]
  for child in list(e.children):
    child.extract()
  e['src'] = 'http://gunnerkrigg.com'+e['src']
  if update_cache_and_return_whether_changed(cache, 'Gunnerkrigg Court', str(e)):
    print('<h1>Gunnerkrigg Court</h1>')
    print(e)

  e = soup(get_html('courses.cs.washington.edu', '/courses/cse505/15au/'))
  old_cache_value = cache.get('CS 505 Autumn 2015', '')
  if update_cache_and_return_whether_changed(cache, 'CS 505 Autumn 2015', str(e)):
    print('<h1>CS 505 Autumn 2015</h1>')
    import difflib
    import html
    old_lines = old_cache_value.split('\n')
    new_lines = str(e).split('\n')
    diff = list(difflib.unified_diff(old_lines, new_lines))
    print('<pre>' + html.escape('\n'.join(diff)) + '</pre>')
