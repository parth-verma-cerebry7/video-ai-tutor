from google import genai
from google.genai.types import Part
import os 

PROJECT_ID = "cerebryai"
REGION = "us-central1"

os.environ["GOOGLE_CLOUD_PROJECT"] = PROJECT_ID
os.environ["GOOGLE_CLOUD_LOCATION"] = REGION
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\parth\Desktop\Cerebry\video-ai-tutor\backend\credentials\cerebryai-1cf9ad8980f2.json"

def model_response(cache_id, text_query, image_query):

    client = genai.Client()
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=[
            # "What is shown in this image?",
            Part.from_uri(
                file_uri="gs://cloud-samples-data/generative-ai/image/scones.jpg",
                mime_type="image/jpeg",
            ),
        ],
    )
    print(response.text)

    return response.text

# model_response(
#     cache_id="cachedContents/lwyavvattg0b",
#     text_query="hey",
#     image_query=None
# )
# Example response:
# The image shows a flat lay of blueberry scones arranged on parchment paper. There are ...