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

def fetch_and_summarize_in_parallel(cache, resources, **method_kwargs):
  cache = LockableMapping(cache)
  results = {}
  def do_everything_and_set_result(resource):
    results[resource.name] = resource.fetch_and_summarize(cache, **method_kwargs)

  threads = set()
  for resource in resources:
    t = threading.Thread(target=do_everything_and_set_result, args=[resource])
    t.start()
    threads.add(t)

  for thread in threads:
    thread.join()

  successful_resources = set(r for r in resources if r.name in set(results.keys()))
  failing_resources = set(r for r in resources if r.name not in set(results.keys()))
  if failing_resources:
    print('failed to fetch/summarize:', ', '.join(r.name for r in failing_resources), file=sys.stderr)
  return '\n\n'.join(results[r.name] for r in successful_resources)
