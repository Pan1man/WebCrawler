from bs4 import BeautifulSoup
from typing_extensions import Generator

from src.urlfrontier import Frontier
from urllib.parse import urljoin, unquote
import aiohttp





class Fetcher:
    @staticmethod
    async def fetch(frontier: Frontier):
        while frontier.len() != 0:
            try:
                url = frontier.remove_url()
                async with aiohttp.ClientSession() as session:
                    response = await session.get(url)
                    page_body = await response.text()
                    url_for_frontier = UrlExtractor.extract_url(page_body, url)
                    for j in url_for_frontier:
                        frontier.add_url(j)
                    TextEditor.extract_text(page_body)
                print(url + "Спаршено")
            except Exception as e:
                print(e)



class UrlExtractor:
    @staticmethod
    def extract_url(page_text: str, base_url) -> Generator:
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


class TextEditor:
    @staticmethod
    def extract_text(page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        text = soup.get_text(strip=True)
        return text
    
