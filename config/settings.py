import os


class Settings:

    # Production
    DEBUG = os.getenv("DEBUG", "False") == "True"

    # Scheduler
    RUNS_PER_DAY = 3

    # Video
    MAX_SCENES = 6
    VIDEO_FPS = 30

    # AI
    DEFAULT_PROVIDER = "groq"
    AI_TIMEOUT = 120

    # Voice
    DEFAULT_VOICE = "en-US-GuyNeural"

    # Uploads
    AUTO_UPLOAD_YOUTUBE = True
    AUTO_UPLOAD_TIKTOK = True

    # Queue
    MAX_QUEUE_SIZE = 100


settings = Settings()
