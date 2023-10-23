# pelican-blog

Personal site driven by __pelican__.

## Content

### Theme

You can use any theme you want, but I recommend to store it locally at themes folder. Don't forget to update it in _pelicanconf.py_.

### Google Analytics

You can use Google Analytics to track your site. Obtain _Google analytics_ token and pass it to _pelican_. To do so, you need to add to _pelicanconf.py_:

```python
GOOGLE_ANALYTICS = 'UA-XXXXXXXX-X'
```

### Content generation

You can use _md_ and _rst_ formats to write pages and articles. To generate new page, place new rst or md file into __content/pages__ folder. To generate article, place new _rst_ or _md_ file into content folder directly. Store any asset you use under __content/assets__ folder.

## Publishing

### Local usage

```python
# Setup virtualenv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# Build suite
invoke build
# Rebuild suite
invoke rebuild
# Serve locally
invoke serve
```

### GitHub Pages

1. Create a new branch called `gh-pages` in the repo.
2. Crate `GH_TOKEN` secret in the repo _Settings_ -> _Secrets_.
3. Open the repo settings -> Pages and set the GitHub Pages source to the `gh-pages` branch.
4. Now, you need to ensure that GA _publish.yml_ will be executed when pushed to master branch.

## Notes:

- Never store GA token in the repo. Use GitHub secrets instead. 
- Never commit venv and output file directly to GitHub.

Please note, that publishing may take some time. If you decided to change the privacy of your repo, you need to regenerate pages and ensure that it will be published using GA.