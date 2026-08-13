from brain.ai_router import ask_ai
import json
import os
import re
from difflib import SequenceMatcher

HISTORY_FILE = "data/hook_history.json"
HOOK_COOLDOWN = 20
MAX_HISTORY = 100
SIMILARITY_THRESHOLD = 0.78

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
HOOK PATTERN DIVERSITY
================================

DO NOT repeatedly use the same opening structure.

Avoid repeatedly starting hooks with structures such as:
"You're wasting..."
"Most people..."
"Stop..."
"I tested..."
"I found..."
"This..."
"The problem..."

These structures may be used occasionally,
but do NOT let a batch become dominated by
one structure.

Across the 15 hooks, deliberately mix:
- pain
- curiosity
- contrast
- experiment
- mistake
- warning
- result
- specific audience
- challenge
- unexpected discovery
- practical shortcut
- hidden capability
- before/after
- specific time-saving
- specific business outcome

The hooks must feel like DIFFERENT ideas,
not the same sentence rewritten 15 times.

================================
STRONG HOOK PATTERNS
================================

Prefer hooks like:
"Watch me turn 10 hours of work into minutes."
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

Generate 15 DIFFERENT hooks.

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

def ensure_history_directory():
    directory = os.path.dirname(HISTORY_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)

def load_hook_history():
    ensure_history_directory()
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            return []
        return data
    except Exception as e:
        print("=" * 60)
        print("HOOK HISTORY LOAD ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)
        return []

def save_hook_history(history):
    ensure_history_directory()
    try:
        history = history[-MAX_HISTORY:]
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print("=" * 60)
        print("HOOK HISTORY SAVE ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)

def normalize_text(text):
    text = str(text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def word_list(text):
    return normalize_text(text).split()

def similarity_score(first, second):
    first_normalized = normalize_text(first)
    second_normalized = normalize_text(second)
    if not first_normalized or not second_normalized:
        return 0.0
    return SequenceMatcher(None, first_normalized, second_normalized).ratio()

def get_hook_pattern(hook):
    words = word_list(hook)
    if not words:
        return ""
    return " ".join(words[:4])

def same_opening_pattern(first, second):
    first_words = word_list(first)
    second_words = word_list(second)
    if len(first_words) < 3 or len(second_words) < 3:
        return False
    first_prefix = " ".join(first_words[:4])
    second_prefix = " ".join(second_words[:4])
    if first_prefix == second_prefix:
        return True
    first_stem = " ".join(first_words[:3])
    second_stem = " ".join(second_words[:3])
    if similarity_score(first_stem, second_stem) >= 0.90:
        return True
    return False

def get_recent_hooks(history):
    return [
        item.get("hook", "")
        for item in history[-HOOK_COOLDOWN:]
        if isinstance(item, dict) and item.get("hook")
    ]

def is_recent_duplicate(hook, recent_hooks):
    normalized_hook = normalize_text(hook)
    for old_hook in recent_hooks:
        old_normalized = normalize_text(old_hook)
        if normalized_hook == old_normalized:
            return True
        if similarity_score(hook, old_hook) >= SIMILARITY_THRESHOLD:
            return True
    return False

def has_recent_pattern_repeat(hook, recent_hooks):
    for old_hook in recent_hooks:
        if same_opening_pattern(hook, old_hook):
            return True
    return False

def record_hook_usage(history, hook, score):
    import time
    history.append({
        "hook": hook,
        "score": round(float(score), 2),
        "pattern": get_hook_pattern(hook),
        "timestamp": time.time()
    })
    save_hook_history(history)
