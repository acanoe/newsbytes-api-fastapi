import logging

from .main import celery_app

logger = logging.getLogger(__name__)


@celery_app.task(name="get_news")
def get_news():
    from newsbytes_api_fastapi.sources.news_sources import sources

    for news_source in sources:
        source, name = news_source.values()
        logger.info(f"getting news from {name}")
        try:
            news = source.get_news()
            print(news)
        except Exception as e:
            logger.exception(f"Error getting news from {name}: {str(e)}")
