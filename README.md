In the era of Machine Learning (ML) the web is an endless source of
data. For this reason, there are plenty of good tools/frameworks to
perform _scraping_ of web pages.

So, I guess, in an ideal world, there should be no need of a new
framework for scraping the web. Nevertheless, there are always subtle
differences between theory and practice. The case of web scraping made
no exceptions.

Real world web pages are often full of javascript code, that alter the
DOM as the user requests/navigates the page. Consequently, scraping
javascript intensive web pages could be impossible.

Such considerations were the sparks that gave birth to *CHeSF*, the
Chrome Headless Scraping Framework. To make a long story short, CHeSF
rely on both
[selenium-python](https://github.com/baijum/selenium-python) and
[ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/)
to perform scraping of webpages also when javascript makes it
impossible.

I know that already exists solutions to this problems, but in my point
of view CHeSF is simpler: you just create a class that inherits from
it, define the parse method and launch it with a start url.

The framework is still very alpha, expect that things could change
rapidly. Currently, there is no documentation, nor packaging. There is
just an example of how you could use the framework to easily scrape
TripAdvisor reviews.

The framework works, but don't expect it to be fast.



