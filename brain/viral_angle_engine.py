from brain.ai_router import ask_ai
import json
import random


SYSTEM_PROMPT = """
You are PromptProHub Viral Angle Engine.

Your ONLY job is to turn a normal topic into irresistible viral content angles.

Think like:

- MrBeast
- Alex Hormozi
- Gary Halbert
- Russell Brunson

Rules:

Generate 15 completely different viral angles.

Every angle must create curiosity.

Avoid:

- Top 10...
- Best...
- Tutorial...
- Guide...
- Welcome...

Instead use:

- I tried...
- Nobody knows...
- This mistake...
- Stop doing...
- What happened...
- The truth about...
- You're losing...
- Don't make this mistake...
- I wish I knew...

Return ONLY JSON.

Example:

{
  "angles":[
    "I tested this AI tool for 30 days",
    "The mistake every freelancer makes",
    "Nobody should know this AI trick"
  ]
}
"""


def generate_viral_angles(topic):

    prompt = f"""
{SYSTEM_PROMPT}

Topic:

{topic}
"""

    try:

        response = ask_ai(prompt)

        response = (
            response
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        data = json.loads(response)

        angles = data.get("angles", [])

        if angles:

            print("=" * 60)
            print("VIRAL ANGLE ENGINE")
            print("=" * 60)
            print(f"Generated {len(angles)} angles")
            print("=" * 60)

            return angles

    except Exception as e:

        print(e)

    print("=" * 60)
    print("Using Viral Angle fallback")
    print("=" * 60)

    return [

        f"I tested {topic} for 30 days",

        f"The truth about {topic}",

        f"Nobody talks about {topic}",

        f"The biggest mistake in {topic}",

        f"Stop doing this with {topic}",

        f"What happened when I tried {topic}",

        f"You're using {topic} the wrong way",

        f"Things I wish I knew about {topic}",

        f"The hidden side of {topic}",

        f"Why most people fail with {topic}"

    ]


def choose_best_angle(topic):

    angles = generate_viral_angles(topic)

    angle = random.choice(angles)

    print("=" * 60)
    print("SELECTED VIRAL ANGLE")
    print("=" * 60)
    print(angle)
    print("=" * 60)

    return angle
