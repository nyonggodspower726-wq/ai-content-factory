from dotenv import load_dotenv
import os

load_dotenv()


# =====================================
# AI
# =====================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

AI_VIDEO_API_URL = os.getenv("AI_VIDEO_API_URL")

AI_VIDEO_API_KEY = os.getenv("AI_VIDEO_API_KEY")


# =====================================
# COVERR VIDEO PROVIDER
# =====================================

COVERR_API_KEY = os.getenv(
    "COVERR_API_KEY"
)

COVERR_API_URL = os.getenv(
    "COVERR_API_URL",
    "https://api.coverr.co/videos"
)


# =====================================
# BRAND
# =====================================

BRAND_NAME = os.getenv(
    "BRAND_NAME",
    "PromptProHub"
)

WEBSITE_URL = os.getenv(
    "WEBSITE_URL",
    "https://promptprohub.com"
)


# =====================================
# SOCIAL MEDIA
# =====================================

# TikTok

TIKTOK_USERNAME = os.getenv(
    "TIKTOK_USERNAME"
)

TIKTOK_ACCESS_TOKEN = os.getenv(
    "TIKTOK_ACCESS_TOKEN"
)


# Facebook

FACEBOOK_PAGE_ID = os.getenv(
    "FACEBOOK_PAGE_ID"
)

FACEBOOK_ACCESS_TOKEN = os.getenv(
    "FACEBOOK_ACCESS_TOKEN"
)


# Instagram

INSTAGRAM_USERNAME = os.getenv(
    "INSTAGRAM_USERNAME"
)

INSTAGRAM_ACCOUNT_ID = os.getenv(
    "INSTAGRAM_ACCOUNT_ID"
)

INSTAGRAM_ACCESS_TOKEN = os.getenv(
    "INSTAGRAM_ACCESS_TOKEN"
)


# YouTube

YOUTUBE_CHANNEL_ID = os.getenv(
    "YOUTUBE_CHANNEL_ID"
)

YOUTUBE_CLIENT_ID = os.getenv(
    "YOUTUBE_CLIENT_ID"
)

YOUTUBE_CLIENT_SECRET = os.getenv(
    "YOUTUBE_CLIENT_SECRET"
)

YOUTUBE_REFRESH_TOKEN = os.getenv(
    "YOUTUBE_REFRESH_TOKEN"
)



# =====================================
# CONTENT SETTINGS
# =====================================

VIDEOS_PER_DAY = 3


POSTING_TIMES = [

    "morning",

    "afternoon",

    "evening"

]


VIDEO_LENGTH = 30



# =====================================
# OUTPUT
# =====================================

OUTPUT_FOLDER = "output"

VIDEO_FOLDER = "output/videos"

AUDIO_FOLDER = "output/audio"

IMAGE_FOLDER = "output/images"



# =====================================
# VIDEO ASSETS
# =====================================

CLIP_FOLDER = "assets/clips"

CACHE_FOLDER = "assets/cache"



# =====================================
# AI STUDIO
# =====================================

DEFAULT_ASPECT_RATIO = "9:16"

DEFAULT_VIDEO_QUALITY = "cinematic"

DEFAULT_VIDEO_DURATION = 5



# =====================================
# PROMPTPROHUB
# =====================================

MISSION = (

    "Help freelancers, creators, marketers and business owners "

    "save time, grow faster and earn more using AI."

)
