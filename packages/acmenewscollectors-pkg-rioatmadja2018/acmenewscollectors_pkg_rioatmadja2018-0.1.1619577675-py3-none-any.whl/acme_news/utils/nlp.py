from google.cloud import translate_v2 as translate
from google.cloud import language_v1 as lang
from typing import Dict, List
from pandas.core.frame import DataFrame
from google.cloud.language_v1.types.language_service import AnalyzeEntitiesResponse
import pandas as pd
import numpy as np
import os

class NewsNLP(object):
    """
    DESCRIPTION
        This is a helper class to perform entity tagging, as well as POS-tag

    PARAMTERS
        :cred_path: given a valid Google credentials

    FUNCTIONS
        __init__
        __get_document__
        __get_encoding__
        google_cloud_tag_entities
        google_pos_tag
        detect_language
    """
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

    def google_pos_tag(self, news_article: str, doc_lang: str = "en", detect_lang: bool = False) -> Dict:
        if not news_article:
            raise ValueError("Please provide a valid news article.")

        document: Dict = {"content": news_article,
                          "type_": self.type_,
                          "language": self.detected_language if detect_lang else doc_lang
                          }

        response = self.client.analyze_syntax(request={'document': document,
                                                       'encoding_type': self.encoding_type})

        speech_tokens: List = []
        for token in response.tokens:
            tag_name = lang.PartOfSpeech.Tag(token.part_of_speech.tag).name
            sent_tense = lang.PartOfSpeech.Tense(token.part_of_speech.tense).name
            person = lang.PartOfSpeech.Person(token.part_of_speech.person).name
            voice = lang.PartOfSpeech.Voice(token.part_of_speech.voice).name
            case = lang.PartOfSpeech.Case(token.part_of_speech.case).name
            mood = lang.PartOfSpeech.Mood(token.part_of_speech.mood).name
            gender = lang.PartOfSpeech.Gender(token.part_of_speech.gender).name
            aspect = lang.PartOfSpeech.Aspect(token.part_of_speech.aspect).name

            content = token.text.content

            speech_tokens.append({'tag_name': tag_name,
                                  'sent_tense': sent_tense if "UNKNOWN" not in sent_tense else np.nan,
                                  'person': person if "UNKNOWN" not in person else np.nan,
                                  'voice': voice if "UNKNOWN" not in voice else np.nan,
                                  'case': case if "UNKNOWN" not in case else np.nan,
                                  'mood': mood if "UNKNOWN" not in mood else np.nan,
                                  'aspect': aspect if "UNKNOWN" not in aspect else np.nan,
                                  'gender': gender if "UNKNOWN" not in gender else np.nan,
                                  'content': content
                                  })

        speech_df: DataFrame = pd.DataFrame(speech_tokens)
        return speech_df.to_dict(orient='records')

    def detect_language(self, news_article: str) -> str:

        if not news_article:
            raise AttributeError("Please provide a valid news article.")

        return self.translate_client.detect_language(news_article).get('language', '')
