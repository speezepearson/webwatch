import http.client
import bs4
import datetime
import urllib.request

headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
}

def get_plain(domain, path, secure=False):
  protocol = 'https' if secure else 'http'
  return urllib.request.urlopen('{}://{}/{}'.format(protocol, domain, path)).read()

def get_html(domain, path='/', secure=False):
  global headers
  if secure:
    connection = http.client.HTTPSConnection(domain)
  else:
    connection = http.client.HTTPConnection(domain)
  connection.request('GET', path, headers=headers)
  response = connection.getresponse()
  return response.read()

def soup(html):
  result = bs4.BeautifulSoup(html, 'html.parser')
  for e in list(result.find_all('script')):
    e.extract()
  for tag in result.find_all(True):
    for attr in list(tag.attrs.keys()):
      if attr.startswith('on'):
        del tag.attrs[attr]
  for e in list(result.find_all('style')):
    e.extract()
  return result

def update_cache_and_return_diff(cache, key, value, diff=(lambda old, new: old != new)):
  old = cache.get(key)
  cache[key] = value
  return diff(old, value)

def update_cache_and_return_new_rss_items(cache, name, soup):
  items = soup.find_all('item')
  items_by_guid = {item.guid.text: item for item in items}
  new_guids = update_cache_and_return_diff(
    cache, name, set(items_by_guid.keys()),
    diff=(lambda old_guids, current_guids: current_guids if old_guids is None else current_guids - old_guids))
  result = [items_by_guid[guid] for guid in new_guids]
  result.sort(key=(lambda item: datetime.datetime.strptime(item.pubdate.text, '%a, %d %b %Y %H:%M:%S %z')))
  return result
