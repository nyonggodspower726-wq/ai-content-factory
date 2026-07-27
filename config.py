from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Website
WEBSITE_URL = os.getenv("WEBSITE_URL")

# Brand
BRAND_NAME = os.getenv("BRAND_NAME")

# Social Media
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")

# Settings
VIDEOS_PER_DAY = 2
VIDEO_LENGTH = 30
