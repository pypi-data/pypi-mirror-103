from google.cloud import translate_v2 as translate
from google.cloud import language_v1 as lang
from typing import Dict
from google.cloud.language_v1.types.language_service import AnalyzeEntitiesResponse
import os

class NewsNLP(object):

    def __init__(self, cred_path: str):

        if not os.path.exists(cred_path):
            raise FileNotFoundError(f"Please provide a valid Google Credentials.")

        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = cred_path
        self.translate_client = translate.Client()
        self.client = lang.LanguageServiceClient()
        self.type_ = lang.Document.Type.PLAIN_TEXT
        self.encoding_type = lang.EncodingType.UTF8
        self.document: Dict = {}
        self.detected_language: str = ""

    def __get_document__(self) -> Dict:
        return self.document

    def __get_encoding__(self):
        return self.encoding_type

    def google_cloud_tag_entities(self, news_article: str, doc_lang: str = 'en',
                                  detect_lang: bool = False) -> AnalyzeEntitiesResponse:

        if not news_article:
            raise ValueError("Please provide a valid news article.")

        if detect_lang:
            self.detected_language: str = self.detect_language(news_article=news_article)

        self.document = {"content": news_article,
                         "type_": self.type_,
                         "language": self.detected_language if detect_lang else doc_lang
                         }

        response = self.client.analyze_entities(request={'document': self.document,
                                                         'encoding_type': self.encoding_type})

        return response

    def detect_language(self, news_article: str) -> str:

        if not news_article:
            raise AttributeError("Please provide a valid news article.")

        return self.translate_client.detect_language(news_article).get('language', '')