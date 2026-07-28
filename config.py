from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()


# AI
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


# Media / Video Creation
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")


# Website
WEBSITE_URL = os.getenv("WEBSITE_URL")


# Brand
BRAND_NAME = os.getenv("BRAND_NAME", "PromptProHub")


# Social Media

# TikTok
TIKTOK_USERNAME = os.getenv("TIKTOK_USERNAME")
TIKTOK_ACCESS_TOKEN = os.getenv("TIKTOK_ACCESS_TOKEN")


# Facebook
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")


# Instagram
INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID")
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN")


# YouTube
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
YOUTUBE_REFRESH_TOKEN = os.getenv("YOUTUBE_REFRESH_TOKEN")


# Content Schedule
VIDEOS_PER_DAY = 3

POSTING_TIMES = [
    "morning",
    "afternoon",
    "evening"
]


# Video Settings
VIDEO_LENGTH = 30  # seconds
