import toml
from retrieve_db import get_cache_by_video
from create_cache import Caching
import logging

# Set up basic configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

with open("config.toml", "r") as f:
    config = toml.load(f)

def llm_response(video_id: str, text_query: str, image_query: bytes = None) -> str:

    # logging.info("Starts to look for cache for video_id: %s", video_id)
    # cache_id = get_cache_by_video(video_id)

    caching = Caching(video_file_name=video_id, model=config['model'], ttl=config['ttl'])

    logging.info("Caching object created")
    response = caching.model_response(video_uri=video_id, text_query=text_query, image_query=image_query, cache_id="cache_id")
    return response
