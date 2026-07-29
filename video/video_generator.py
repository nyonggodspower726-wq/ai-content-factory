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
