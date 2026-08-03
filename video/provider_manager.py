from video.minimax_worker import generate_minimax_video
from video.fal_worker import generate_fal_video


class VideoProviderManager:

    def __init__(self):

        self.providers = [

            {
                "name": "MiniMax",
                "function": generate_minimax_video
            },

            {
                "name": "Fal AI",
                "function": generate_fal_video
            }

        ]
