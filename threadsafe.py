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

class LockableFile:
  def __init__(self, file):
    self.file = file
    self.lock = threading.Lock()

  def read(self, *args, **kwargs):
    with self.lock:
      return self.file.read(*args, **kwargs)

  def write(self, *args, **kwargs):
    with self.lock:
      return self.file.write(*args, **kwargs)

  def flush(self, *args, **kwargs):
    with self.lock:
      return self.file.flush(*args, **kwargs)

  def seek(self, *args, **kwargs):
    with self.lock:
      return self.file.seek(*args, **kwargs)

def run_resources(cache, resources, file=sys.stdout):
  cache = LockableMapping(cache)
  file = LockableFile(file)
  threads = set()
  for resource in resources:
    t = threading.Thread(target=resource.main, args=[cache], kwargs={'file': file})
    t.start()
    threads.add(t)
  for thread in threads:
    thread.join()
