# -*- coding: utf-8 -*- #
from __future__ import unicode_literals


AUTHOR = 'Iliya Vereshchagin'
SITENAME = "wwakabobik's lair"
SITEURL = 'https://wwakabobik.github.io'
GOOGLE_ANALYTICS = "G-MVTS1WKZ1T"

PATH = 'content'
TIMEZONE = 'Europe/Belgrade'
DEFAULT_LANG = u'en'
DEFAULT_PAGINATION = 5
PAGINATION_PATTERNS = (
    (1, '{base_name}/', '{base_name}/index.html'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)
DEFAULT_DATE = 'fs'
DEFAULT_DATE_FORMAT = '%d %b %Y'


# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins']
PLUGINS = [
  'i18n_subsites',
  'sitemap',
  'neighbors',
  'assets',
  'post_stats',
]

BOOTSTRAPIFY = {
    'table': ['table', 'table-striped', 'table-hover'],
    'img': ['img-fluid'],
    'blockquote': ['blockquote'],
}

THEME = 'themes/dark_python'

# Atilla-only settings
HOME_COVER = 'assets/images/bg/main.png'
HOME_COLOR = 'black'

# Feed generation is usually not desired when developing
FEED_ATOM = 'feeds/atom.xml'
FEED_RSS = 'feeds/rss.xml'
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_ATOM = 'feeds/{slug}.atom.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'
TAG_FEED_ATOM = 'feeds/{slug}.tag.atom.xml'
TAG_FEED_RSS = 'feeds/{slug}.tag.rss.xml'
AUTHOR_FEED_ATOM = 'feeds/{slug}.author.atom.xml'
AUTHOR_FEED_RSS = 'feeds/{slug}.author.rss.xml'

# Blogroll
LINKS = (('Github', 'https://github.com/wwakabobik'),
         ('PyPi', 'https://pypi.org/user/wwakabobik/'),
         ('Habr', 'https://habr.com/ru/users/wwakabobik'),)


# Social widget
SOCIAL = (('facebook', 'https://www.facebook.com/wwakabobik'),
          ('linkedIn', 'https://www.linkedin.com/in/wwakabobik'),
          ('instagram', 'https://www.instagram.com/i_ver')
          )

STATIC_PATHS = ['assets']

EXTRA_PATH_METADATA = {
    'assets/robots.txt': {'path': 'robots.txt'},
    'assets/favicon/favicon.ico': {'path': 'favicon.ico'},
    'assets/CNAME': {'path': 'CNAME'},
    'assets/favicon/site.webmanifest': {'path': 'site.webmanifest'}
}

# Post and Pages path
ARTICLE_URL = '{date:%Y}/{date:%m}/{slug}/'
ARTICLE_SAVE_AS = '{date:%Y}/{date:%m}/{slug}/index.html'
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
YEAR_ARCHIVE_URL = '{date:%Y}/'
YEAR_ARCHIVE_SAVE_AS = '{date:%Y}/index.html'
MONTH_ARCHIVE_URL = '{date:%Y}/{date:%m}/'
MONTH_ARCHIVE_SAVE_AS = '{date:%Y}/{date:%m}/index.html'

# Tags and Category path
CATEGORY_URL = 'category/{slug}/'
CATEGORY_SAVE_AS = 'category/{slug}/index.html'
CATEGORIES_URL = 'category/'
CATEGORIES_SAVE_AS = 'category/index.html'
TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'
TAGS_URL = 'tag/'
TAGS_SAVE_AS = 'tag/index.html'

# Author
AUTHOR_URL = 'author/{slug}/'
AUTHOR_SAVE_AS = 'author/{slug}/index.html'
AUTHORS_URL = 'author/'
AUTHORS_SAVE_AS = 'author/index.html'

# Archives
ARCHIVES_URL = 'archive/'
ARCHIVES_SAVE_AS = 'archive/index.html'

# Sitemap
SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

AUTHORS_BIO = {
  "wwakabobik": {
    "name": "Iliya Vereshchagin",
    "cover": "assets/images/bg/personal.png",
    "image": "assets/images/authors/wwakabobik.png",
    "linkedin": "wwakabobik",
    "github": "wwakabobik",
    "pypi": "wwakabobik",
    "instagram": "i_ver",
    "location": "Serbia, Novi Sad",
    "bio": "Quality is not an act, it's habit"
  }
}

AUTHOR_META = {
  "wwakabobik": {
    "name": "Iliya Vereshchagin",
    "cover": "assets/images/bg/personal.png",
    "image": "assets/images/authors/wwakabobik.png",
    "linkedin": "wwakabobik",
    "github": "wwakabobik",
    "pypi": "wwakabobik",
    "instagram": "i_ver",
    "location": "Serbia, Novi Sad",
    "bio": "Quality is not an act, it's habit"
  }
}

TAG_META = {
  "qa": {
    "cover": "assets/images/bg/qa.png",
    "description": "qa related cover",
  },
  "python": {
    "cover": "assets/images/bg/main4.png",
    "description": "python related cover"
  },
  "immigration": {
    "cover": "assets/images/bg/immigration.png",
    "description": "immigration related cover"
  },
  "ai": {
    "cover": "assets/images/bg/ai.png",
    "description": "ai related cover"
  },
  "personal": {
    "cover": "assets/images/bg/ai.png",
    "description": "personal related cover"
  },
  "rocketry": {
    "cover": "assets/images/bg/rocketry.png",
    "description": "rocketry related cover"
  },
  "games": {
    "cover": "assets/images/bg/games.png",
    "description": "games related cover"
  },
  "travel": {
    "cover": "assets/images/bg/travel.png",
    "description": "travel related cover"
  },
  "cooking": {
    "cover": "assets/images/bg/cooking.png",
    "description": "cooking related cover"
  }
}

CATEGORY_META = {
  "qa": {
    "cover": "assets/images/bg/qa.png",
    "description": "qa related cover",
  },
  "python": {
    "cover": "assets/images/bg/main4.png",
    "description": "python related cover"
  },
  "immigration": {
    "cover": "assets/images/bg/immigration.png",
    "description": "immigration related cover"
  },
  "ai": {
    "cover": "assets/images/bg/ai.png",
    "description": "ai related cover"
  },
  "personal": {
    "cover": "assets/images/bg/ai.png",
    "description": "personal related cover"
  },
  "rocketry": {
    "cover": "assets/images/bg/rocketry.png",
    "description": "rocketry related cover"
  },
  "games": {
    "cover": "assets/images/bg/games.png",
    "description": "games related cover"
  },
  "travel": {
    "cover": "assets/images/bg/travel.png",
    "description": "travel related cover"
  },
  "cooking": {
    "cover": "assets/images/bg/cooking.png",
    "description": "cooking related cover"
  }
}

HEADER_COVERS_BY_CATEGORY = {'python': 'assets/images/bg/python.png',
                             'ai': 'assets/images/bg/ai.png',
                             'qa': 'assets/images/bg/qa.png',
                             'travel': 'assets/images/bg/travel.png',
                             'immigration': 'assets/images/bg/immigration.png',
                             'cooking': 'assets/images/bg/cooking.png',
                             'games': 'assets/images/bg/games.png',
                             'rocketry': 'assets/images/bg/rocketry.png',
                             'personal': 'assets/images/bg/immigration.png',
                             }

MENUITEMS = (('Home', '/'),
             ('Tags', '/tag/index.html'),
             ('Categories', '/category/index.html'),
             ('Archives', '/archive/index.html'),)

SHOW_CREDITS = False
SHOW_ARTICLE_MODIFIED_TIME = True
SHOW_AUTHOR_BIO_IN_ARTICLE = False
SHOW_CATEGORIES_ON_MENU = False
SHOW_COMMENTS_COUNT_IN_ARTICLE_SUMMARY = True
SHOW_FULL_ARTICLE_IN_SUMMARY = False
SHOW_PAGES_ON_MENU = False
SHOW_SITESUBTITLE_IN_HTML_TITLE = False
SHOW_TAGS_IN_ARTICLE_SUMMARY = True

# Jinja config - Pelican 4
JINJA_ENVIRONMENT = {
  'extensions': [
    'jinja2.ext.loopcontrols',
    'jinja2.ext.i18n',
    'jinja2.ext.do',
  ]
}
