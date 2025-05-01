import time
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os, toml
load_dotenv()
import logging

# Set up basic configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

with open("config.toml", "r") as f:
    config = toml.load(f)

class Caching:
    def __init__(self, video_file_name: str, model: str, ttl: str):
        self.video_file_name = video_file_name
        self.model = model
        self.client = genai.Client(api_key=os.getenv('GOOGLE_API_KEY'))
        self.ttl = ttl
        self.video_file = None
        self.cache=None

    def upload_video_file(self):
        try:
            logging.info("Starting to create cache for video")
            self.video_file = self.client.files.upload(file=self.video_file_name)
            logging.info('Video file uploaded')
        except Exception as e:
            print(f"Error uploading video file: {e}")

        try:
            logging.info("Waiting for video to be processed")
            while self.video_file.state.name == "PROCESSING":
                print('Waiting for video to be processed.')
                time.sleep(2)
                self.video_file = self.client.files.get(name = self.video_file.name)
            print('Video file processed: ', self.video_file.uri)

        except Exception as e:
            print(f"Error processing video file: {e}")

    def create_cache(self):
        try:
            self.cache = self.client.caches.create(
                model=self.model,
                config=types.CreateCachedContentConfig(
                display_name=self.video_file_name, # used to identify the cache
                system_instruction=(
                    'You are an expert video analyzer, and your job is to answer '
                    'the user\'s query based on the video file you have access to.'
                ),
                contents=[self.video_file],
                ttl=self.ttl,
                )
            )
            print('Cache created: ', self.cache.name)
            return self.cache.name

        except Exception as e:
            print(f"Error creating cache: {e}")
    
    def model_response(self, cache_id: str, text_query: str, image_query: str = None) -> str:
        try:
            contents = [text_query]
            if image_query:
                contents.append(
                    types.Part.from_bytes(data=image_query, mime_type="image/png")
                )

            response = self.client.models.generate_content(
                model = self.model,
                contents = contents,
                # config=types.GenerateContentConfig(cached_content=cache_id)
            )

            return response.text
        
        except Exception as e:
            print(f"Error generating response: {e}")


# cache_handler = Caching(
#     video_file_name=config['video_file_name'],
#     model=config['model'],
#     ttl=config['ttl']
# )

# response = cache_handler.model_response(
#     cache_id="cachedContents/lwyavvattg0b",
#     text_query="What is the name of the rabbit?",
#     image_query=None
# )

# print(response)

# cache_handler.upload_video_file()
# cache_id = cache_handler.create_cache()
# print(cache_id)

