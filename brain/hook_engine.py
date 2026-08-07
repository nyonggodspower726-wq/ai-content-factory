from brain.ai_router import ask_ai
import json


SYSTEM_PROMPT = """
You are the PromptProHub VIRAL HOOK ENGINE.

Your ONLY job is to create extremely strong short-form video hooks.

The hook is the FIRST sentence viewers hear.

Your goal is:

STOP THE SCROLL
CREATE CURIOSITY
PROMISE A SPECIFIC BENEFIT
MAKE THE VIEWER NEED TO KNOW WHAT HAPPENS NEXT

PromptProHub focuses on:

- AI prompts
- ChatGPT prompts
- Prompt templates
- AI productivity
- AI automation
- AI workflows
- AI tools
- AI for freelancers
- AI for creators
- AI for marketers
- AI for businesses
- AI digital products
- AI prompt ebooks and templates

The hook must connect directly to the topic.

================================
FORBIDDEN OPENINGS
================================

NEVER start with:

"What if you could..."
"What if..."
"Imagine..."
"Imagine having..."
"Have you ever wondered..."
"Did you know..."
"Today..."
"In this video..."
"Welcome..."
"Let's talk about..."
"Here's..."
"Here are..."
"Let me show you..."
"Want to..."
"Do you want to..."
"Are you tired of..."
"Have you ever..."

NEVER use generic motivational hooks.

NEVER use vague hooks such as:

"This changes everything."

"This is amazing."

"You need to see this."

"Nobody is ready for this."

unless the sentence contains a SPECIFIC reason
that creates curiosity.

================================
STRONG HOOK PATTERNS
================================

Prefer hooks like:

"Watch me turn 10 hours of work into minutes."

"You're wasting hours doing this manually."

"Most freelancers are using ChatGPT completely wrong."

"I tested this AI workflow so you don't have to."

"This ChatGPT prompt can save hours of repetitive work."

"I replaced an entire afternoon of work with one AI workflow."

"Stop writing these prompts from scratch."

"You're probably using ChatGPT backwards."

"I found the prompt that turns a blank page into a finished draft."

"This is how creators are cutting hours of work down to minutes."

"Most business owners don't know ChatGPT can do this."

"I tested 20 AI prompts. Only a few were actually useful."

"One prompt can turn your messy idea into a complete plan."

"The problem isn't ChatGPT. It's the way you're prompting it."

================================
IMPORTANT
================================

DO NOT invent fake achievements.

Never claim:

"I made $100,000"

"I made $1 million"

"I got 10,000 customers"

unless the topic or provided information actually proves it.

Use believable curiosity without making false claims.

================================
HOOK QUALITY
================================

Every hook should have at least ONE of:

- specific time saving
- money-saving angle
- productivity improvement
- surprising discovery
- common mistake
- hidden feature
- strong contrast
- specific problem
- curiosity gap
- unexpected result
- practical benefit

Whenever possible, make the benefit concrete.

Weak:

"AI is changing business."

Strong:

"Most business owners are still doing this manually."

================================
LENGTH
================================

Keep each hook between approximately
8 and 18 words.

Make it sound natural when spoken.

Do not write long explanations.

Generate 15 different hooks.

Then score each hook from 1-100 for:

- scroll_stopping_power
- curiosity
- specificity
- relevance
- benefit
- natural_sounding

Return ONLY valid JSON.

Format:

{
    "hooks": [
        {
            "hook": "Watch me turn 10 hours of work into minutes.",
            "scroll_stopping_power": 95,
            "curiosity": 92,
            "specificity": 94,
            "relevance": 96,
            "benefit": 95,
            "natural_sounding": 94
        }
    ]
}
"""


def generate_hooks(topic, angle, curiosity):

    prompt = f"""
{SYSTEM_PROMPT}

================================
CURRENT TOPIC
================================

{topic}

================================
VIRAL ANGLE
================================

{angle}

================================
CURIOSITY
================================

{curiosity}

Create 15 highly specific hooks for this exact topic.

Do NOT create generic AI hooks.

The hook must make sense even if the viewer knows
nothing about the topic.

Prioritize a strong concrete benefit.

Remember:

NEVER use "What if you could..."

NEVER use "Imagine..."

NEVER use "Imagine having..."

NEVER use generic motivational openings.
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

        hooks = data.get("hooks", [])

        if not hooks:
            raise Exception(
                "AI returned no hooks"
            )

        cleaned_hooks = []

        for item in hooks:

            if isinstance(item, dict):

                hook = str(
                    item.get(
                        "hook",
                        ""
                    )
                ).strip()

                scores = [
                    float(
                        item.get(
                            "scroll_stopping_power",
                            0
                        )
                    ),
                    float(
                        item.get(
                            "curiosity",
                            0
                        )
                    ),
                    float(
                        item.get(
                            "specificity",
                            0
                        )
                    ),
                    float(
                        item.get(
                            "relevance",
                            0
                        )
                    ),
                    float(
                        item.get(
                            "benefit",
                            0
                        )
                    ),
                    float(
                        item.get(
                            "natural_sounding",
                            0
                        )
                    )
                ]

                average_score = (
                    sum(scores)
                    / len(scores)
                )

                if hook:

                    cleaned_hooks.append(
                        (
                            average_score,
                            hook
                        )
                    )

        if cleaned_hooks:

            # Highest-quality hook first
            cleaned_hooks.sort(
                reverse=True,
                key=lambda x: x[0]
            )

            print("=" * 60)
            print("VIRAL HOOK ENGINE")
            print("=" * 60)

            print(
                f"Generated: {len(cleaned_hooks)} hooks"
            )

            print(
                f"Best Hook Score: "
                f"{cleaned_hooks[0][0]:.1f}/100"
            )

            print(
                f"Best Hook: "
                f"{cleaned_hooks[0][1]}"
            )

            print("=" * 60)

            return cleaned_hooks

    except Exception as e:

        print("=" * 60)
        print("HOOK ENGINE ERROR")
        print("=" * 60)

        print(e)

        print("=" * 60)

    # =================================
    # SAFE FALLBACK
    # =================================

    return [

        (
            95,
            f"You're probably using {topic} the hard way."
        ),

        (
            94,
            f"Most people are wasting time with {topic}."
        ),

        (
            93,
            f"I found a faster way to use {topic}."
        ),

        (
            92,
            f"Stop doing this manually with {topic}."
        ),

        (
            91,
            f"This {topic} mistake is costing people hours."
        ),

        (
            90,
            f"I tested a faster workflow for {topic}."
        )

    ]


def choose_hook(topic, angle, curiosity):

    hooks = generate_hooks(
        topic,
        angle,
        curiosity
    )

    if not hooks:

        return (
            f"You're probably using {topic} the hard way."
        )

    # =================================
    # DO NOT RANDOMLY PICK
    # =================================

    best_score, best_hook = hooks[0]

    print("=" * 60)
    print("SELECTED VIRAL HOOK")
    print("=" * 60)

    print(
        f"Score: {best_score:.1f}/100"
    )

    print(
        best_hook
    )

    print("=" * 60)

    return best_hook
