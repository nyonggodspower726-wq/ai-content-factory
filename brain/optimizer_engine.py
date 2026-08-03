from brain.ai_router import ask_ai


SYSTEM_PROMPT = """
You are PromptProHub Optimizer AI.

Your job is to improve an already-generated project.

Optimize:

1. Hook
2. Viewer retention
3. Story flow
4. Emotional impact
5. Curiosity
6. Marketing
7. CTA
8. SEO friendliness

Do NOT rewrite everything.

Improve only weak parts.

Return JSON only.

Example:

{
  "optimized": true,
  "changes": [
    "Improved hook",
    "Stronger CTA",
    "Better curiosity"
  ],
  "project": {}
}
"""


def optimize(project):

    prompt = f"""
{SYSTEM_PROMPT}

Optimize this project:

{project}
"""

    return ask_ai(prompt)
