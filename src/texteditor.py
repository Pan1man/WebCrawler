import nltk
from sklearn.feature_extraction.text import TfidfVectorizer

from src.db.db import get_async_session
from src.schemas.pages import PageBase

from bs4 import BeautifulSoup

from nltk.corpus import stopwords
class TextEditor:

    def compile_tags(self, text, n_keywords=5):
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
        text = soup.get_text(strip=True)
        return text

    def compile_description(self, text):
        extracted_text = self.extract_text(text)
        return "Какое то описание"

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

