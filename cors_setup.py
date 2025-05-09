from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\Users\parth\Desktop\Cerebry\video-ai-tutor\backend\cerebryai-1cf9ad8980f2.json"
def cors_configuration(bucket_name):
    """Set a bucket's CORS policies configuration."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    bucket.cors = [
        {
            "origin": [
                "http://localhost:3000",
                "http://127.0.0.1:3000",
                "http://localhost:8000",
                "http://127.0.0.1:8000",
                "https://v0-video-ai-tutor-1m98.vercel.app/"
            ],
            "responseHeader": [
                "Content-Type",
                "x-goog-resumable",
                "Access-Control-Allow-Origin"
            ],
            "method": ['GET', 'PUT', 'POST'],
            "maxAgeSeconds": 3600
        }
    ]
    bucket.patch()

    print(f"Set CORS policies for bucket {bucket.name} is {bucket.cors}")
    return bucket

# Usage:
cors_configuration("video_ai_tutor")