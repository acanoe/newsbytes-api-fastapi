import logging

import requests
from requests.exceptions import HTTPError

from ...dependencies import get_db
from ...models import stories
from ...schemas import News

logger = logging.getLogger(__name__)


class Progscrape:
    def get_name(self) -> str:
        return "Progscrape"

    def __create_request(self) -> News | None:
        try:
            response = requests.get("https://www.progscrape.com/feed.json")
            response.raise_for_status()

            return News(**response.json())

        except HTTPError as e:
            logger.error(f"HTTP Error getting news from Progscrape: {str(e)}")
        except Exception as e:
            logger.exception(f"Error getting news from Progscrape: {str(e)}")

        return None

    def __write_db(self, news: News) -> None:
        db = get_db()
        db = next(db)
        stories.create_all(db, obj_in=news.stories)

    def get_news(self) -> News | None:
        news = self.__create_request()
        if news is not None:
            self.__write_db(news)
        return news


source = Progscrape()
