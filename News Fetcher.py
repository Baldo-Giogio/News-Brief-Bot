import requests
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from io import BytesIO
import json
import time
import google.generativeai as genai
from gtts import gTTS

logger = logging.getLogger(__name__)

@dataclass
class News:
    title: str
    description: str
    url: str
    published_loc: str
    source: str
    author : Optional[str] = None
    content : Optional[str] = None


    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'News':
        """Create from dictionary"""
        return cls(**data)


class NewsAPI:
    def __init__(self, api_key: str):    
        """
        Arguments: 
                  api_key (str): 300fb263-b20b-40cb-bf68-8e51f8f014d6
        """
        self.api_key = api_key
        self.base_url = "https://eventregistry.org/api/v1/article/getArticles"
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'NewsBot/1.0'})

        #Rate limiting
        self.last_request_time = 0
        self.min_request_interval = 1


    def _rate_limit(self):
        curr_time = time.time()
        time_since_last = curr_time - self.last_request_time

        if time_since_last <= self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)

        
    def get_news(self, topic:str, days_back = 1, page_size: int = 20) -> List[News]:
        """
        Arguments: 
        topic (str): News topic to gather information on 
        days_back (int): Number of days to consider
        page_size (int): Number of articless to fetch

        Returns:
            List[News]: list of news articles
        """

        try: 
            self.rate_limit()
            end_date = datetime.now()
            start_date = end_date -timedelta(days = days_back)

            parameters = {
                'top': topic,
                'apiKey': self.api_key,
                'lang': 'en',
                'sortBy': 'publishedAt',
                'from': start_date.strftime('%m-%d-%Y'),
                'to': end_date.strftime('%m-%d-%Y'),
                'pagesize': min(page_size, 80)
            }

            response = self.session.get(f"{self.base_url}/everything", parameters = parameters, timeout = 10)
            response.raise_for_status

            data = response.json()

            if data.get('status')!= 'ok':
                logger.error(f"NewsAPI error: {data.get('message','unkown error')}")
                return[]
            articles = []
            for article_data in data.get('articles', []):
                if not article_data.get('title') or not article_data.get('desvription'):
                    continue

                article = News(
                        title = article_data['title'],
                        description = article_data['description'],
                        url = article_data['url'],
                        published_loc = article_data['publishedAt'],
                        source = article_data['source']['name'],
                        author = article_data.get('author'),
                        content = article_data.get('content')
                )
                articles.append(article)

            logger.info(f"Fetched {len(articles)} articles for topic: {topic}")
            return articles[:page_size]
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching news for the topic: {topic}")
            return[]
            
class GenAIAnalyzer:

    def __init__(self, api_key: str, model_name: str = 'gemini-pro'):
        """ 
        Initialize AI analyzer

        arguments:
            api_key (str): AIzaSyDjkOaviI9IV-94HUd22l9yv7Fl1ID7Rg0
            model_name (str): gemini-2.0-flash-live-001
        """
        genai.configure(api_key = api_key)
        self.model = genai.GenerativeModel(model_name)

        self.last_request_time = 0
        self.min_request_interval = 1

    def _rate_limit(self):
        curr_time = time.time()
        time_since_last = curr_time -self.last_request_time

        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)

        self.last_request_time = time.time()

    def analy_and_sum(self, articles: List[News], topic: str, analy_type: str = "comprehensive") -> str:
        """
        arguments:
            articles (List[News]): list of news articles 
            topic(str): topics being analyzed
            analy_type (str): type of analysis (comprehensive, breif)

            returns: 
                str: AI generated analysis and summary
        """
        if not articles:
            return f" No recent news found for topic: **{topic}**"
        
        try: 
            self._rate_limit()
            articles_text = self._prepare_articles_text(articles)

            prompt = self._get_analy_propmt(topic, articles_text, analy_type)

            response = self.model.generate_content(prompt)

            if response.text:
                form_response = self._format_response(response.text, topic, len(articles))
                logger.info(f"AI Analysis for topic: {topic}")
                return form_response
            
        except Exception as e:
            logger.error(f"Error generating analysis for topic {topic}: {e}")
            return self._create_fallback_summary(articles, topic)
        
