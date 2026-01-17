import urllib.robotparser
from urllib.parse import urlparse


class robotsTxt:

    def __init__(self,url):
        self.url = url

    def is_allowed(url, user_agent="MyCrawler", fallback=True):
        rp = urllib.robotparser.RobotFileParser()
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"

        try:
            rp.set_url(robots_url)
            rp.read()
            return rp.can_fetch(user_agent, url)
        except:
            print(f"[robots.txt not accessible] Proceeding with: {url}")
            return fallback
    
    