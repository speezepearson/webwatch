import urllib.request
import urllib.parse
import urllib.error
import http.client

def set_default_scheme(url, default='http'):
  if '://' not in url:
    url = '{}://{}'.format(default, url)
  return url

def simple_fetch(url):
  url = set_default_scheme(url)
  return urllib.request.urlopen(url).read()

def fetch_spoofing_browser_headers(url):
  url = set_default_scheme(url)
  scheme, netloc, path, params, query, fragment = urllib.parse.urlparse(url)
  if scheme not in ('http', 'https'):
    raise ValueError('spoofy fetch only supports HTTP and HTTPS schemes')

  connection = (http.client.HTTPSConnection(netloc) if scheme=='https' else http.client.HTTPConnection(netloc))
  connection.request('GET', path, body=query, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36'})
  response = connection.getresponse()
  return response.read()

def fetch(url):
  try:
    return simple_fetch(url)
  except urllib.error.HTTPError:
    return fetch_spoofing_browser_headers(url)

def fetcher(url):
  return (lambda: fetch(url))