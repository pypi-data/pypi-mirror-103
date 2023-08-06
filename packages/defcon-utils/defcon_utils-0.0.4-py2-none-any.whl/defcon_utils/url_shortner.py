class Cuttly:

    def __init__(self, api_key):
        self.API_KEY = api_key

    def shorten_url(self, url):
        from django.conf import settings
        import urllib
        import requests
        key = self.API_KEY
        url = urllib.parse.quote(long_url)
        r = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(key, url))

        return r.json()['url']['shortLink']
