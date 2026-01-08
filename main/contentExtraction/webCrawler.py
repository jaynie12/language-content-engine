#crawl the web for French content
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
#https://scrape.do/blog/web-crawler-python/

class WebCrawler:    
    def __init__(self, base_url, max_pages=100):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited = set()
        self.to_visit = deque([base_url])
        self.french_content = []

    def fetch(self, url):
        try:
            response = requests.get(url, timeout=5, headers={"User-Agent": "MyCrawler"})
            if response.status_code == 200:
                content_type = response.headers.get("Content-Type", "")
                if "text/html" in content_type:
                    return response.text
        except requests.RequestException:
            pass
        return ""
    
    def extract_links(html, base_url):
        soup = BeautifulSoup(html, "html.parser")
        base_parsed = urlparse(base_url)
        base_domain = ".".join(base_parsed.netloc.split(".")[-2:])  # wikipedia.org

        links = set()

        for tag in soup.find_all("a", href=True):
            href = tag["href"]
            absolute = urljoin(base_url, href)
            parsed = urlparse(absolute)

            # Allow all subdomains under the base domain (like *.wikipedia.org)
            if parsed.netloc.endswith(base_domain) and absolute.startswith("http"):
                links.add(absolute)

        return links
    
    def should_skip_url(url):
        skip_extensions = (
            ".xml", ".json", ".pdf", ".jpg", ".jpeg", ".png", ".gif",
            ".svg", ".zip", ".rar", ".mp4", ".mp3", ".ico"
        )
        return url.lower().endswith(skip_extensions)



    def crawl(seed_url, max_pages=10):
        visited = set()
        queue = deque([seed_url])

        while queue and len(visited) < max_pages:
            url = queue.popleft()
            if url in visited or should_skip_url(url):
                continue

            print(f"Crawling: {url}")
            html = fetch(url)
            if not html:
                continue

            links = extract_links(html, url)
            queue.extend(links - visited)
            visited.add(url)
        
        //