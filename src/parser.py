from bs4 import BeautifulSoup

from src.urlfrontier import Frontier, url_frontier
from urllib.parse import urljoin, unquote
import aiohttp


class Fetcher:
    @staticmethod
    async def fetch(frontier: Frontier = url_frontier):
        while frontier.len() != 0:
            base_url = frontier.remove_url()
            async with aiohttp.ClientSession() as session:
                async with session.get(base_url) as response:
                    page_text = await response.text()
            url_for_frontier = UrlExtractor.extract_url(page_text, base_url)
            for j in url_for_frontier:
                frontier.add_url(j)
            TextExtractor.extract_text(page_text)
            print(base_url + "Спаршено")


class UrlExtractor:
    @staticmethod
    def extract_url(page_text: str, base_url):
        soup = BeautifulSoup(page_text, 'lxml')
        ugly_urls = []
        for link in soup.find_all('a'):
            url = link.get('href')
            if url:
                ugly_urls.append(url)
        normalized_urls = UrlExtractor.normalize_url(ugly_urls, base_url)
        return normalized_urls

    @staticmethod
    def normalize_url(ugly_urls: list, base_url):
        for url in ugly_urls:
            if url:
                url = unquote(url)
                if not url.startswith('http'):
                    absolute_url = urljoin(base_url, url)
                else:
                    absolute_url = url
                yield absolute_url


class TextExtractor:
    @staticmethod
    def extract_text(page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        text = soup.get_text(strip=True)
        return text
