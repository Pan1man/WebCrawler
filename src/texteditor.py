from src.models.pages import Page

from sklearn.feature_extraction.text import TfidfVectorizer

from src.db.db import get_async_session
from src.schemas.pages import PageBase

from fastapi import Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from bs4 import BeautifulSoup


class TextEditor:

    def extract_text(self, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        text = soup.get_text(strip=True)
        return text

    def compile_description(self, text):
        extracted_text = self.extract_text(text)
        return "Какое то описание"

    def compile_tags(self, text, n_keywords=5):
        extracted_text = self.extract_text(text)
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_matrix = tfidf_vectorizer.fit_transform([extracted_text])
        feature_names = tfidf_vectorizer.get_feature_names_out()
        sorted_indices = tfidf_matrix.toarray().argsort()[0][::-1]
        keywords = [feature_names[idx] for idx in sorted_indices[:n_keywords]]
        return keywords

    @staticmethod
    def compile_title(page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        title = soup.title.string
        if soup.title:
            return title
        else:
            return "Нет названия"



class EntryCreation:
    @staticmethod
    async def create_entry(page: PageBase, session: get_async_session):
        try:
            session.add(page)
            await session.commit()
        finally:
            pass

