import os, time, toml, logging
PROJECT_ID = "cerebryai"
REGION = "us-central1"
from google.cloud import storage

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = REGION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

if os.environ.get("K_SERVICE"):  # Running on Cloud Run
    print("Running on Cloud Run - using default service account")
    # No need to set GOOGLE_APPLICATION_CREDENTIALS
elif os.path.exists("/app/credentials"):
    print("Running in Docker - setting credentials")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/app/credentials/cerebryai-1cf9ad8980f2.json"
else:
    print("Running locally - setting credentials")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./credentials/cerebryai-1cf9ad8980f2.json"
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\parth\Desktop\Cerebry\video-ai-tutor\backend\cerebryai-b45725179a93.json"

client = storage.Client()

import prompts
from google import genai
from google.genai import types
from google.genai.types import Content, CreateCachedContentConfig, Part, HttpOptions
# from dotenv import load_dotenv
# load_dotenv()

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
        self.client = genai.Client(http_options=HttpOptions(api_version="v1"))
        self.chat = self.client.chats.create(model=model, config=types.GenerateContentConfig(system_instruction=prompts.SystemPrompt))
        self.ttl = ttl
        self.video_file = None
        self.cache=None
        self.system_instruction = prompts.SystemPrompt


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

        contents = [
            Content(
                role="user",
                parts=[
                    Part.from_uri(
                        file_uri="https://storage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
                        mime_type="video/mp4",
                    )
                ],
            )
        ]

        content_cache = self.client.caches.create(
            model=self.model,
            config=CreateCachedContentConfig(
                contents=contents,
                system_instruction=self.system_instruction,
                display_name=self.video_file_name,
                ttl=self.ttl,
            ),
        )
        print('Cache created: ', content_cache.name)
        return content_cache.name
        # try:
        #     self.cache = self.client.caches.create(
        #         model=self.model,
        #         config=types.CreateCachedContentConfig(
        #         display_name=self.video_file_name, # used to identify the cache
        #         system_instruction=(
        #             'You are an expert video analyzer, and your job is to answer '
        #             'the user\'s query based on the video file you have access to.'
        #         ),
        #         contents=[self.video_file],
        #         ttl=self.ttl,
        #         )
        #     )
        #     print('Cache created: ', self.cache.name)
        #     return self.cache.name

        # except Exception as e:
        #     print(f"Error creating cache: {e}")



    
    def model_response(self, video_uri: str, text_query: str, image_query: bytes = None, cache_id: str = None) -> str:
        try:
            contents = [text_query]
            contents.append(Part.from_uri(
                file_uri=video_uri,
                mime_type="video/mp4"
            ))
            if image_query:
                contents.append(types.Part.from_bytes(data=image_query, mime_type='image/png'))

            response = self.chat.send_message(contents)
            # response = self.client.models.generate_content(
            #     model=self.model,
            #     contents = contents,
            #     config=types.GenerateContentConfig(system_instruction=self.system_instruction),
            #     # config=types.GenerateContentConfig(cached_content=cache_id)
            # )

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
#     text_query="hey",
#     image_query=None
# )

# print(response)

# cache_handler.upload_video_file()
# cache_id = cache_handler.create_cache()
# print(cache_id)

