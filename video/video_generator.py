import os
import requests

from moviepy.editor import (
    VideoFileClip,
    AudioFileClip,
    CompositeAudioClip,
    concatenate_videoclips,
)

from video.ai_video_worker import generate_all_scenes

from video.effects import (
    add_hook,
    apply_camera_effects
)

from video.subtitles import add_subtitles

from audio.music import get_music


# ============================================================
# PROMPTPROHUB AI VIDEO STUDIO
# ============================================================

"""
Pipeline

Brain
    ↓
Scene Generator
    ↓
Download Scenes
    ↓
Camera Engine
    ↓
Timeline Builder
    ↓
Voice
    ↓
Music
    ↓
Subtitles
    ↓
Branding
    ↓
Final Export
"""


# ============================================================
# DOWNLOAD AI GENERATED SCENES
# ============================================================
