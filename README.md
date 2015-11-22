A library for notifying you when web pages change.

There are things you care about on the Internet, and you want to know when they change. Some of these don't have RSS feeds or anything, so you have to manually visit the page. What a pain! If only there were a tool that would fetch the pages, extract the sections you care about, compare those sections to the previously-fetched sections, and print the changes as HTML.

Well, now there is.

Usage
=====

1. Install this package.

2. Write a short script. For example:

  ```python
    from webwatch import *

    main(
      RSSResource(name='xkcd', url='xkcd.com/rss.xml'),
      AtomResource(name='Schneier', url="https://www.schneier.com/blog/atom.xml"),
      TwitterResource(name="W|A Can't", username='wacnt'),
      Resource(
        name='Slashdot', url='slashdot.org',
        selector='.fhitem', tag_to_cache_repr=(lambda tag: tag.header.text)))
  ```

  As you see, you just call `main` on a bunch of "resources." See the [Resources](#Resources) section for details.

3. Run the script whenever you want to look for changes.

  ```language-sh
    $ python my-script.py > updates.html && open updates.html
  ```

  (Personally, I have `python my-script.py >> updates.html` in my crontab, so that new updates get pulled automatically a few times every day. To see what's new, I `mv updates.html harvested-updates.html && open harvested-updates.html`)


Resources
=========

A Resource is entirely described by:
- a unique `name` to display to you (and use as a cache key)
- a `url` to fetch
- a CSS `selector` to specify which elements should be distilled from the HTML document
- (optional) a function `format_tag`, which turns one of those HTML elements into a string (by default, it just returns the HTML)
- (optional) a function `tag_to_cache_repr`, which turns one of those HTML elements into some object that should represent it in the cache. By default, this is just the HTML, but if the tag contains something volatile that you don't care about (e.g. a number of Likes), you can use this function to filter out any static, unique part.

All of these can be provided as keyword arguments to the `Resource` constructor.

There are also Resource subclasses for some common kinds of resource:
- `RSSResource(name, url)` for RSS feeds
- `AtomResource(name, url)` for Atom feeds
- `TwitterResource(name, username)` for Twitter feeds
