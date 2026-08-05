from video.scene_engine import SceneEngine
from video.clip_engine import ClipEngine


print("=" * 60)
print("PROMPTPROHUB PIPELINE TEST")
print("=" * 60)


# 1. Create scenes

scene_engine = SceneEngine()


scenes = scene_engine.generate(

    [
        "AI entrepreneur working on laptop in modern office",
        "business owner using artificial intelligence technology"
    ],

    ""

)


print("SCENES:")
print(scenes)



# 2. Get clips from Coverr

clip_engine = ClipEngine()


clips = clip_engine.generate(

    scenes

)


print("=" * 60)
print("RESULT:")
print(clips)
print("=" * 60)
