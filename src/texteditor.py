import html2text as html2text
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import select

from src.db.db import get_async_session
from src.models.pages import Page
from src.schemas.pages import PageBase

from bs4 import BeautifulSoup

from nltk.corpus import stopwords

from sqlalchemy.orm import Session
from db.db import engine
from sqlalchemy.ext.asyncio import AsyncSession
class TextEditor:

    def compile_tags(self, text, n_keywords=10):
        stop_words = set(stopwords.words('russian'))

        extracted_text = self.extract_text(text)

        stop_words_list = list(stop_words)
        tfidf_vectorizer = TfidfVectorizer(stop_words=stop_words_list)
        tfidf_matrix = tfidf_vectorizer.fit_transform([extracted_text])

        feature_names = tfidf_vectorizer.get_feature_names_out()
        sorted_indices = tfidf_matrix.toarray().argsort()[0][::-1]

        keywords = [feature_names[idx] for idx in sorted_indices if feature_names[idx] not in stop_words_list][
                   :n_keywords]
        return keywords

    def extract_text(self, page_text):
        soup = BeautifulSoup(page_text, 'html.parser')
        text = html2text.html2text(soup.get_text())
        return text

    def compile_description(self, text):
        extracted_text = self.extract_text(text)
        description = extracted_text[0:200]
        return description

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
    async def create_entry(url, page: PageBase, db_session: AsyncSession):
        try:
            existing_page = await db_session.execute(select(Page).filter_by(url=url))
            existing_page = existing_page.scalar_one_or_none()

            if existing_page is None:
                db_session.add(page)
                await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e
        finally:
            await db_session.close()


