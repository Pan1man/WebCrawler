from bs4 import BeautifulSoup
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import AsyncGenerator

from src.urlfrontier import Frontier, url_frontier
from urllib.parse import urljoin, unquote
import aiohttp
import re


class SessionMaker:
    root_domains = []

    @staticmethod
    def is_same_root(url) -> str | None:
        r = re.compile(r'.*\.([^.]*[^0-9][^.]*\.[^.]*[^.0-9][^.]*$)')
        root_domain = r.sub(r'\1', url)
        if root_domain not in SessionMaker.root_domains:
            SessionMaker.root_domains.append(root_domain)
            return None
        else:
            return root_domain

    async def get_aiohttp_session(self, url):
        if not self.is_same_root(url):
            async with aiohttp.ClientSession() as session:
                try:
                    yield session
                finally:
                    await session.close()
                    SessionMaker.root_domains.remove(SessionMaker.is_same_root(url))


class Fetcher:
    session_maker = SessionMaker()

    @staticmethod
    async def fetch(frontier: Frontier = url_frontier):
        try:
            while frontier.len() != 0:
                url = frontier.remove_url()
                async for session in Fetcher.session_maker.get_aiohttp_session(url):
                    async with session.get(url) as response:
                        page_text = await response.text()
                    url_for_frontier = UrlExtractor.extract_url(page_text, url)
                    for j in url_for_frontier:
                        frontier.add_url(j)
                    text = Text()
                    print(url + "Спаршено")

        except Exception as e:
            print("какая я хуйня ", e)
        finally:
            await Fetcher.fetch(frontier)


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



class Text:
    def __init__(self, page_text):
        self.page_text = page_text
        self.key_words = None
        self.extract_text(page_text)



    def extract_text(self, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        text = soup.get_text(strip=True)
        self.find_key_words(text)

    def find_key_words(self, text):
        #Логика извлечения ключевых слов

        self.key_words = []



class TextExtractor:
    @staticmethod
    def extract_text(page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        text = soup.get_text(strip=True)
        return text


