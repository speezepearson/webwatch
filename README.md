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
      ElementSetResource(
        name='Slashdot', url='slashdot.org',
        selector='.fhitem', tag_to_cache_repr=(lambda tag: tag.header.text)))
  ```

  As you see, you just call `main` on a bunch of "resources." See the [Resources](#Resources) section for details.

3. Run the script whenever you want to look for changes. It'll print the diff to stdout. To fetch the newest changes and open them in your browser, do this:

  ```language-sh
    $ python my-script.py > updates.html && open updates.html
  ```

  Personally, I like to email the changes to myself. Using Mutt, I put the following line in my bashrc:

  ```language-sh
    alias update-me='python my-script.py | mutt -s "Updates at $(date +'%Y-%m-%d %H:%M:%S')"' -e 'set content_type=text/html' my.email.address@gmail.com
  ```

  So now I can just type `update-me` whenever I'm bored, and see what's new.

  (If you want to be like me, here is [a good `.muttrc` file](http://unix.stackexchange.com/questions/66560/mutt-smtp-tls-error-sending-mail), though I find I only need the beginning (up through "force TLS").)



Resources
=========

A Resource is entirely described by:
- a unique `name` to display to you (and use as a cache key);
- a way to fetch the current data;
- a way to diff the cache value against the current data; and
- a way to compute a new cache value.

A Resource's main workflow, `fetch_and_diff`, does the following:
- fetch the current data;
- pull the old value out of the cache;
- compute a diff, and return it;
- (but first, update the cache).

There are built-in subclasses that cover most use cases:
- `RSSResource(name, url)` for RSS feeds
- `AtomResource(name, url)` for Atom feeds
- `TwitterResource(name, username)` for Twitter feeds
- `ElementSetResource(name, url, selector, ...)`, a very general resource that does a plain HTTP get to download the resource, extracts the elements matching the given CSS selector, and when asked for a diff, returns all those elements that weren't present last time it fetched the page.

  (Optional arguments include: `tag_sort_key`, which, like `list.sort(key)`, determines the order in which the tags are printed in the diff; `format_tag`, which lets you customize how each new tag is printed; and `tag_to_cache_repr`, which should reduce a tag to some unique identifier that's robust to, e.g., the "62 comments" part at the bottom of a news story changing.)
