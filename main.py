import toml
from retrieve_db import get_cache_by_video
from create_cache import Caching

with open("config.toml", "r") as f:
    config = toml.load(f)

def llm_response(video_id: str, text_query: str, image_query: str = None) -> str:
    cache_id = get_cache_by_video(video_id)

    caching = Caching(video_file_name=video_id, model=config['model'], ttl=config['ttl'])

    response = caching.model_response(cache_id = cache_id, text_query=text_query, image_query=image_query)
    return response
