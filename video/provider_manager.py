from video.wan_worker import generate_wan_video
from video.ltx_worker import generate_ltx_video
from video.cogvideo_worker import generate_cogvideo_video


class VideoProviderManager:

    def __init__(self):

        self.providers = [

            {
                "name": "Wan 2.2",
                "function": generate_wan_video
            },

            {
                "name": "LTX Video",
                "function": generate_ltx_video
            },

            {
                "name": "CogVideoX",
                "function": generate_cogvideo_video
            }

        ]
