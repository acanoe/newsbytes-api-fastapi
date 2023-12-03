import glob
import importlib
import os

from ...schemas import News


class NewsSource:
    def get_name(self) -> str:
        raise NotImplementedError()

    def get_news(self) -> News:
        raise NotImplementedError()


sources = []

try:
    # Get the current file's directory
    current_directory = os.path.dirname(__file__)

    # Get all files in the directory except the current file
    files = glob.glob(f"{current_directory}/*.py")
    files.remove(__file__)

    # import all source in each file
    for file in files:
        module = importlib.import_module(
            "newsbytes_api_fastapi.sources.news_sources."
            + os.path.basename(file).split(".")[0]
        )
        source = getattr(module, "source")
        sources.append({"source": source, "name": source.get_name()})

except NameError:
    # Handle the case where __file__ is not defined
    pass
