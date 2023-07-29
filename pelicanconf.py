AUTHOR = 'Iliya Vereshchagin'
SITENAME = "wwakabobik's lair"
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Belgrade'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Github', 'https://github.com/wwakabobik'),
         ('PyPi', 'https://pypi.org/user/wwakabobik/'),
         ('Habr', 'https://habr.com/ru/users/wwakabobik'),)

# Social widget
SOCIAL = (('Facebook', 'https://www.facebook.com/wwakabobik'),
          ('LinkedIn', 'https://www.linkedin.com/in/wwakabobik'),
          ('Instagram', 'https://www.instagram.com/i_ver'))


DEFAULT_PAGINATION = 5

THEME = 'notmyidea'

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['/Users/ilyavereshchagin/Work/pelican-themes/pelican-plugins', ]
PLUGINS = ['i18n_subsites', ]
JINJA_ENVIRONMENT = {
    'extensions': ['jinja2.ext.i18n'],
}
