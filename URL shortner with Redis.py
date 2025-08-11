import redis
import string
import random
from urllib.parse import urlparse

class UrlShortener():

    def __init__(self):
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.base_url = 'http://short.ly/'

    def generate_short_code(self, length = 6):
        char = string.ascii_letters + string.digits
        return ''.join(random.choice(char) for _ in range(length))

    def _is_valid_url(self, url):
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])

        except:
            return False

    def shorten_url(self, original_url, length=6, expire=None):
        if not self._is_valid_url(original_url):
            return None, 'Invalid URL Format'

        short_code = self.generate_short_code(length)

        if expire:
            self.redis.set(short_code, original_url, ex=expire)
        else:
            self.redis.set(short_code, original_url)

        short_url = self.base_url + short_code
        return short_url, None




