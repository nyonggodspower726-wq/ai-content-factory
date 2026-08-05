from promptprohub_video_engine import PromptProHubVideoEngine

engine = PromptProHubVideoEngine()


def create_video(
    prompts,
    script,
    voice_file
):
    return engine.generate(
        prompts,
        script,
        voice_file
    )
