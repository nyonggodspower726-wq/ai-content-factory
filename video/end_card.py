from moviepy.editor import TextClip, ColorClip, CompositeVideoClip


class EndCard:

    def __init__(self):

        self.duration = 6

    def create(self):

        background = ColorClip(
            size=(720, 1280),
            color=(15, 15, 15),
            duration=self.duration
        )

        title = TextClip(
            "Discover smarter AI tools and prompts.",
            fontsize=44,
            color="white",
            method="caption",
            size=(620, None)
        ).set_position(("center", 250)).set_duration(self.duration)

        website = TextClip(
            "🌐 promptprohub00.netlify.app",
            fontsize=36,
            color="white"
        ).set_position(("center", 520)).set_duration(self.duration)

        hashtags = TextClip(
            "#AI  #ChatGPT\n#Business  #Freelancer\n#PromptProHub",
            fontsize=28,
            color="white",
            align="center"
        ).set_position(("center", 720)).set_duration(self.duration)

        final = CompositeVideoClip(
            [
                background,
                title,
                website,
                hashtags
            ]
        )

        return final
