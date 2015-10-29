import http.client
import bs4

headers = {
  'Accept': 'text/html,application/xhtml+xml,application/xml',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'
}

def get_html(domain, resource='/'):
  global headers
  connection = http.client.HTTPConnection(domain)
  connection.request('GET', resource, headers=headers)
  response = connection.getresponse()
  return response.read()

def soup(html):
  result = bs4.BeautifulSoup(html, 'html.parser')
  for e in list(result.find_all('script')):
    e.extract()
  for e in list(result.find_all('style')):
    e.extract()
  return result

def update_cache_and_return_whether_changed(cache, key, value):
  if cache.get(key) != value:
    cache[key] = value
    return True
  return False

