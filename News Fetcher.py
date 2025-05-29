import requests
import google.generativeai as genai
from gtts import gTTS
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from io import BytesIO
import json
import time

logger = logging.getLogger(__name__)

@dataclass
class News:
    title: str
    description: str
    url: str
    poublished_loc: str
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
    def __init__(self, api_key: str)    
    """
    Arguments: 
              api_key (str): 300fb263-b20b-40cb-bf68-8e51f8f014d6
    """
    self.api_key = api_key
    self.base_url = request.get(url).json
    self.session = request.Session()
    self.session.headers.update({'User-Agent': 'NewsBot/1.0'})

    #Rate limiting
    self.last_request_time = 0
    self.min_request_interval = 1


    def _rate_limit(self):
        curr_time = time.time()
        time_since_last = curr.time - self.last_request_time

        if time_since_last <= self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)

        
        def get_news(self, topic:str, days_back = 1, page_size: int = 20) -> List[News]
            """
            Arguments: 
            topic (str): News topic to gather information on 
            days_back (int): Number of days to consider
            page_size (int): Number of articless to fetch
            """