    return downloaded


# ==========================================
# BUILD BACKGROUND VIDEO
# ==========================================

def build_background_video(video_paths, duration):

    clips = []

    if len(video_paths) == 0:
        return None

    seconds_per_clip = max(
        2,
        duration / len(video_paths)
    )

    for path in video_paths:

        try:
            clip = VideoFileClip(path)
        except Exception:
            print(f"Skipping bad video: {path}")
            continue

        clip = clip.resize(
            height=1280
        )

        clip = clip.crop(
            x_center=clip.w / 2,
            y_center=clip.h / 2,
            width=720,
            height=1280
        )

        clip = clip.subclip(
            0,
            min(seconds_per_clip, clip.duration)
        )

        clips.append(clip)

    final_background = concatenate_videoclips(
        clips,
        method="compose"
    )

    final_background = apply_zoom(
        final_background
    )

    final_background = final_background.set_duration(
        duration
    )

    return final_background
# ==========================================
# CREATE FINAL VIDEO
# ==========================================

def create_video(script, voice_file):

    print("Creating professional AI video...")

    keywords = [
        word
        for word in script.split()
        if len(word) > 4
    ]

    search_term = " ".join(
        keywords[:4]
    )

    video_urls = search_pexels_videos(
        search_term
    )

    if len(video_urls) == 0:

        print("No background videos found.")

        return None

    video_paths = download_videos(
        video_urls
    )

    try:

        audio = AudioFileClip(
            voice_file
        )

        background = build_background_video(
            video_paths,
            audio.duration
        )

        if background is None:

            print("Background creation failed.")

            return None

        final = background.set_audio(
            audio
        )

        music_file = "assets/music/background.mp3"

        final = add_background_music(
            final,
            music_file
        )

        # ==========================================
        # EXPORT VIDEO
        # ==========================================

        output = "output/final_video.mp4"
