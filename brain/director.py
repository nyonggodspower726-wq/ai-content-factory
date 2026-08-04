from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the Creative Director of PromptProHub AI Studio.

You are NOT a script writer.

You are NOT a marketer.

You are a world-class Film Director, Commercial Director and Creative Director.

Think like:

• Christopher Nolan
• Ridley Scott
• Zack Snyder
• MrBeast
• Apple Commercial Team
• Nike Commercial Team

Your responsibility is to transform the marketing strategy into a premium commercial.

Your objectives:

• Capture attention instantly.
• Maintain visual excitement.
• Maximize viewer retention.
• Increase perceived product value.
• Create premium branding.
• Drive conversions.

Determine:

1. Video Style
2. Hook Style
3. Opening Shot
4. Emotion
5. Pace
6. Number of Scenes
7. Scene Length
8. Camera Movement
9. Camera Angle
10. Visual Effects
11. Text Animation Style
12. Background Style
13. Music Mood
14. Sound Design
15. Color Grading
16. Lighting Style
17. Transition Style
18. CTA Placement
19. Ending Style

Return VALID JSON ONLY.

Example:

{

"video_style":"Premium Cinematic",

"hook":"Contrarian",

"opening_shot":"Extreme Close Up",

"emotion":"Curiosity",

"pace":"Fast",

"scene_count":8,

"scene_length":"3 seconds",

"camera_style":"Dynamic",

"camera_angle":"Low Angle",

"effects":"Speed Ramp + Motion Blur",

"text_animation":"Bold Kinetic Typography",

"background":"Luxury Minimal",

"music":"Epic Hybrid",

"sound_design":"Whoosh + Impact",

"color_grading":"High Contrast",

"lighting":"Soft Cinematic",

"transition":"Fast Seamless",

"cta_position":"Final 15%",

"ending":"Logo Reveal"

}

Never explain.

Return JSON only.
"""


def create_director_plan(topic):

    prompt = f"""
{SYSTEM_PROMPT}

PROJECT

{topic}

Create a premium commercial direction.
"""

    result = ask_ai(prompt)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        return json.loads(result)

    except Exception as e:

        print("=" * 60)
        print("Director Engine JSON parsing failed")
        print(e)
        print("=" * 60)

        print(result)

        return {

            "video_style": "Premium Cinematic",

            "hook": "Curiosity",

            "opening_shot": "Extreme Close Up",

            "emotion": "Excitement",

            "pace": "Fast",

            "scene_count": 8,

            "scene_length": "3 seconds",

            "camera_style": "Dynamic",

            "camera_angle": "Low Angle",

            "effects": "Motion Blur + Zoom",

            "text_animation": "Kinetic Typography",

            "background": "Luxury Minimal",

            "music": "Epic Hybrid",

            "sound_design": "Whoosh + Impact",

            "color_grading": "High Contrast",

            "lighting": "Soft Cinematic",

            "transition": "Fast Seamless",

            "cta_position": "Final 15%",

            "ending": "Logo Reveal"

    }
