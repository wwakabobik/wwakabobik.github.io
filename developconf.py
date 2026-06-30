# Local preview — relative URLs so CSS/JS load from the dev server, not GitHub Pages.
import os
import sys

sys.path.append(os.curdir)
from pelicanconf import *  # noqa: F401,F403

SITEURL = ""
RELATIVE_URLS = True
