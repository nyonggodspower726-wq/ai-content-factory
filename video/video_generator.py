import os
import requests
import PIL.Image

if not hasattr(PIL.Image,"ANTIALIAS"):
    try:
        PIL.Image.ANTIALIAS=PIL.Image.Resampling.LANCZOS
    except AttributeError:
        PIL.Image.ANTIALIAS=PIL.Image.LANCZOS

from moviepy.editor import VideoFileClip,AudioFileClip,concatenate_videoclips
from moviepy.video.fx import all as vfx
from config import PEXELS_API_KEY
from video.effects import add_hook
from video.watermark import add_watermark
from video.background_music import add_background_music

# (keep your search_pexels_videos and download_videos functions unchanged)

def build_background_video(video_paths,duration):
    clips=[]
    if not video_paths:
        return None
    seconds_per_clip=max(2,duration/len(video_paths))
    for path in video_paths:
        clip=VideoFileClip(path).resize(height=1280).crop(x_center=VideoFileClip(path).w/2,y_center=VideoFileClip(path).h/2,width=720,height=1280).subclip(0,min(seconds_per_clip,VideoFileClip(path).duration))
        clips.append(clip)
    for i,clip in enumerate(clips):
        clips[i]=clip.fx(vfx.fadein,0.3).fx(vfx.fadeout,0.3)
    final_background=concatenate_videoclips(clips,method="compose")
    final_background=final_background.set_duration(duration)
    return final_background
