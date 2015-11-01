import threading
import collections.abc
import sys

class LockableMapping(collections.abc.MutableMapping):
  def __init__(self, cache):
    self.cache = cache
    self.lock = threading.Lock()

  def __getitem__(self, key):
    with self.lock:
      return self.cache[key]

  def __setitem__(self, key, value):
    with self.lock:
      self.cache[key] = value

  def __delitem__(self, key):
    with self.lock:
      del self.cache[key]

  def __iter__(self):
    with self.lock:
      return iter(self.cache)

  def __len__(self):
    with self.lock:
      return len(self.cache)

def fetch_and_update_cache_and_summarize_in_parallel(cache, resources):
  cache = LockableMapping(cache)
  results = {}
  def do_everything_and_set_result(resource):
    results[resource.name] = resource.fetch_and_update_cache_and_summarize(cache)

  threads = set()
  for resource in resources:
    t = threading.Thread(target=do_everything_and_set_result, args=[resource])
    t.start()
    threads.add(t)

  for thread in threads:
    thread.join()

  return '\n\n'.join(results[resource.name] for resource in resources)
