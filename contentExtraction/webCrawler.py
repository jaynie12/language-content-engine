#crawl the web for French content
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque


class WebCrawler:    
    def __init__(self, base_url, max_pages=100):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited = set()
        self.to_visit = deque([base_url])
        self.french_content = []
    
    def is_french(self, text):
        # Simple heuristic: check for common French words
        french_keywords = ['le', 'la', 'et', 'de', 'un', 'une', 'à', 'est', 'en', 'pour']
        text_lower = text.lower()
        return any(word in text_lower for word in french_keywords)
    
    #https://ai.google.dev/edge/mediapipe/solutions/text/language_detector/python

    def crawl(self):