from brain.ai_router import ask_ai
import json
import os
import re
import time
from difflib import SequenceMatcher

HISTORY_FILE = "data/cta_history.json"
CTA_COOLDOWN = 10
MAX_HISTORY = 200
SIMILARITY_THRESHOLD = 0.78
PATTERN_THRESHOLD = 0.88

SYSTEM_PROMPT = """
You are the PromptProHub ELITE CTA ENGINE.

Your ONLY job is to create high-converting spoken CTAs
for short-form videos distributed across TikTok,
Instagram Reels, YouTube Shorts and LinkedIn.

The CTA is the final conversion moment.

Your mission:
CREATE DESIRE
CREATE A CLEAR NEXT STEP
MAKE THE OFFER FEEL RELEVANT
MAKE THE ACTION FEEL EASY
AVOID SOUNDING LIKE A ROBOTIC AD

PromptProHub sells practical AI prompts, prompt templates,
AI guides and digital resources for:
- Creators
- Freelancers
- Business owners
- Marketers
- AI users

================================
CORE CTA REQUIREMENTS
================================

The CTA should normally contain:
1. A natural action to check/click the bio link.
2. A natural reason to follow for more.

Do NOT force the same sentence structure.

Vary phrases such as:
"Check the link in my bio..."
"Get the full version through my bio..."
"The complete resource is in my bio..."
"Grab the full toolkit from my bio..."
"If you want the complete system..."
"Follow for more practical AI workflows..."

Do not make every CTA say:
"Click the link in my bio and follow for more."

================================
CTA PSYCHOLOGY
================================

Rotate across these psychological archetypes:

1. DIRECT OFFER
2. BENEFIT
3. CURIOSITY
4. FOMO
5. URGENCY
6. EXCLUSIVE ACCESS
7. CHEAT-CODE ENERGY
8. PROBLEM-SOLUTION
9. CHALLENGE
10. IDENTITY
11. AUTHORITY
12. FUTURE PACING
13. DISCOVERY
14. SAVINGS
15. TIME SAVING
16. MONEY/RESULT
17. TOOLKIT
18. RESOURCE
19. NEXT STEP
20. SOFT SELL
21. HARD SELL
22. FULL VERSION
23. NEXT VIDEO
24. PRODUCTIVITY
25. BUILD FASTER
26. WORK SMARTER
27. FULL SYSTEM
28. TEMPLATE LIBRARY
29. PROMPT LIBRARY
30. JOIN THE JOURNEY

Do not use the same archetype repeatedly.

================================
MONEY CTA RULE
================================

Money/result CTAs may be used only when the video
actually supports the claim.

NEVER invent:
- earnings
- clients
- customers
- sales
- guaranteed income
- fake results
- fake scarcity

NEVER say:
"This made me $500"
unless supplied information proves it.

Use credible language instead.

================================
FOMO AND URGENCY
================================

Do not invent fake deadlines.

NEVER claim:
"48 hours only"
"price goes up tomorrow"
"this gets deleted"
"limited spots"

unless real evidence is supplied.

Use honest urgency instead.

================================
CHEAT-CODE ENERGY
================================

You may use:
"shortcut"
"cheat code"
"unfair advantage"
"secret weapon"

Do NOT falsely claim:
illegal
banned
leaked
patched
confidential
celebrity-only

unless supplied information proves it.

================================
CTA STYLE
================================

The CTA must feel like the natural conclusion
of the video.

Prefer:
specific
short
spoken
confident
human
clear

Avoid:
"Dear viewer..."
"Please kindly..."
"Act now!!!"
"Don't miss this incredible opportunity!!!"
"Like and subscribe."
"Thanks for watching."

================================
TOPIC MATCHING
================================

Match the CTA to what the video actually demonstrated.

Productivity:
"Grab the full prompt library from my bio,
and follow for more ways to work faster."

AI discovery:
"Explore the complete AI toolkit through my bio,
and follow for the next workflow."

Prompt tutorial:
"Get the full collection of ready-to-use prompts in my bio,
and follow for more."

Business:
"If you're building with AI, the full resource is in my bio.
Follow for more practical strategies."

================================
DIVERSITY
================================

Generate exactly 15 CTAs.

The 15 CTAs must feel genuinely different.

Do NOT simply replace one word.

Vary:
- sentence length
- opening
- psychological trigger
- action wording
- benefit
- emotional tone
- position of follow request
- position of product reference

================================
LENGTH
================================

Target:
10-30 spoken words.

Keep every CTA natural.

================================
SCORING
================================

Score every CTA from 1-100:

conversion_potential
relevance
clarity
curiosity
urgency
natural_sounding
novelty
credibility

Return ONLY valid JSON.

Format:

{
  "ctas": [
    {
      "cta": "Get the full prompt library through the link in my bio, and follow for more practical AI workflows.",
      "archetype": "resource",
      "conversion_potential": 94,
      "relevance": 96,
      "clarity": 95,
      "curiosity": 88,
      "urgency": 82,
      "natural_sounding": 95,
      "novelty": 91,
      "credibility": 99
    }
  ]
}
"""

def ensure_history_directory():
    directory = os.path.dirname(HISTORY_FILE)
    if directory:
        os.makedirs(directory, exist_ok=True)

def load_cta_history():
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
        print("CTA HISTORY LOAD ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)
        return []

def save_cta_history(history):
    ensure_history_directory()
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(
                history[-MAX_HISTORY:],
                file,
                indent=2,
                ensure_ascii=False
            )
    except Exception as e:
        print("=" * 60)
        print("CTA HISTORY SAVE ERROR")
        print("=" * 60)
        print(e)
        print("=" * 60)

def normalize_text(text):
    text = str(text or "").lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def similarity_score(first, second):
    first = normalize_text(first)
    second = normalize_text(second)
    if not first or not second:
        return 0.0
    return SequenceMatcher(
        None,
        first,
        second
    ).ratio()

def get_cta_pattern(cta):
    words = normalize_text(cta).split()
    if not words:
        return ""
    return " ".join(words[:5])

def get_recent_ctas(history):
    return [
        item.get("cta", "")
        for item in history[-CTA_COOLDOWN:]
        if isinstance(item, dict) and item.get("cta")
    ]

def get_recent_archetypes(history):
    return {
        str(item.get("archetype", "")).lower()
        for item in history[-8:]
        if isinstance(item, dict) and item.get("archetype")
    }

def is_recent_duplicate(cta, recent_ctas):
    for old_cta in recent_ctas:
        if normalize_text(cta) == normalize_text(old_cta):
            return True
        if similarity_score(cta, old_cta) >= SIMILARITY_THRESHOLD:
            return True
    return False

def same_cta_pattern(first, second):
    first_words = normalize_text(first).split()
    second_words = normalize_text(second).split()
    if len(first_words) < 3 or len(second_words) < 3:
        return False
    first_prefix = " ".join(first_words[:4])
    second_prefix = " ".join(second_words[:4])
    if first_prefix == second_prefix:
        return True
    first_stem = " ".join(first_words[:3])
    second_stem = " ".join(second_words[:3])
    return similarity_score(
        first_stem,
        second_stem
    ) >= PATTERN_THRESHOLD

def has_recent_pattern_repeat(cta, recent_ctas):
    return any(
        same_cta_pattern(cta, old_cta)
        for old_cta in recent_ctas
    )

def record_cta_usage(history, cta, score, archetype, topic):
    history.append({
        "cta": cta,
        "score": round(float(score), 2),
        "archetype": archetype,
        "pattern": get_cta_pattern(cta),
        "topic": topic,
        "timestamp": time.time()
    })
    save_cta_history(history)
def generate_cta(topic):
    history = load_cta_history()
    recent_ctas = get_recent_ctas(history)
    recent_archetypes = get_recent_archetypes(history)
    recent_text = "\n".join(
        f"- {cta}"
        for cta in recent_ctas[-10:]
    )
    prompt = f"""
{SYSTEM_PROMPT}
================================
CURRENT VIDEO TOPIC
================================
{topic}
================================
RECENTLY USED CTAs
================================
Do NOT copy, lightly rewrite, or repeat the structure of these:
{recent_text}
================================
FINAL GENERATION RULE
================================
Generate exactly 15 genuinely different CTAs for this topic.
Mix psychological archetypes.
Do not make all CTAs mention the same benefit.
Do not make every CTA begin with "Click", "Check", "Get", or "Want".
Keep the CTA natural when spoken by an AI voice.
Remember: never invent earnings, scarcity, deadlines, customers,
celebrity claims, bans, leaks, or guaranteed results.
Return ONLY valid JSON.
"""
    try:
        response = ask_ai(prompt)
        response = response.replace("```json","").replace("```","").strip()
        data = json.loads(response)
        ideas = data.get("ctas",[])
        if not ideas:
            raise Exception("AI returned no CTAs")
        cleaned = []
        for item in ideas:
            if not isinstance(item,dict):
                continue
            cta = str(item.get("cta","")).strip()
            if not cta:
                continue
            try:
                scores = {
                    "conversion":float(item.get("conversion_potential",0)),
                    "relevance":float(item.get("relevance",0)),
                    "clarity":float(item.get("clarity",0)),
                    "curiosity":float(item.get("curiosity",0)),
                    "urgency":float(item.get("urgency",0)),
                    "natural":float(item.get("natural_sounding",0)),
                    "novelty":float(item.get("novelty",0)),
                    "credibility":float(item.get("credibility",0))
                }
            except (TypeError,ValueError):
                continue
            weighted_score=(
                scores["conversion"]*0.24+
                scores["relevance"]*0.16+
                scores["clarity"]*0.13+
                scores["curiosity"]*0.10+
                scores["urgency"]*0.08+
                scores["natural"]*0.11+
                scores["novelty"]*0.10+
                scores["credibility"]*0.08
            )
            archetype=str(item.get("archetype","unknown")).strip().lower()
            cleaned.append({
                "score":weighted_score,
                "cta":cta,
                "archetype":archetype
            })
        if not cleaned:
            raise Exception("No valid CTAs remained after parsing.")
        cleaned.sort(
            reverse=True,
            key=lambda item:item["score"]
        )
        print("="*60)
        print("PROMPTPROHUB ELITE CTA ENGINE")
        print("="*60)
        print(f"Generated: {len(cleaned)}")
        print(f"Recent CTAs: {len(recent_ctas)}")
        print("="*60)
        return cleaned
    except Exception as e:
        print("="*60)
        print("CTA ENGINE FAILED")
        print("="*60)
        print(type(e).__name__)
        print(str(e))
        print("="*60)
        return [
            {
                "score":95,
                "cta":"Get the full prompt library through the link in my bio, and follow for more.",
                "archetype":"prompt_library"
            },
            {
                "score":94,
                "cta":"The complete PromptProHub resource is in my bio. Follow for more practical AI workflows.",
                "archetype":"resource"
            },
            {
                "score":93,
                "cta":"Want the full version? Check my bio, then follow for the next AI strategy.",
                "archetype":"full_version"
            },
            {
                "score":92,
                "cta":"Grab the templates from my bio and follow for more ways to build faster with AI.",
                "archetype":"templates"
            },
            {
                "score":91,
                "cta":"If this helped, the complete toolkit is in my bio. Follow for more useful AI ideas.",
                "archetype":"benefit"
            },
            {
                "score":90,
                "cta":"Take the shortcut from my bio, and follow for more practical AI systems.",
                "archetype":"shortcut"
            }
        ]

def choose_cta(topic):
    candidates=generate_cta(topic)
    history=load_cta_history()
    recent_ctas=get_recent_ctas(history)
    recent_archetypes=get_recent_archetypes(history)
    fresh=[]
    blocked=[]
    for item in candidates:
        cta=item["cta"]
        if is_recent_duplicate(cta,recent_ctas):
            blocked.append((cta,"duplicate"))
            continue
        if has_recent_pattern_repeat(cta,recent_ctas):
            blocked.append((cta,"pattern"))
            continue
        fresh.append(item)
    if not fresh:
        non_exact=[
            item
            for item in candidates
            if normalize_text(item["cta"]) not in {
                normalize_text(old)
                for old in recent_ctas
            }
        ]
        fresh=non_exact if non_exact else candidates
    def final_score(item):
        bonus=4 if item.get("archetype","") not in recent_archetypes else 0
        return item["score"]+bonus
    fresh.sort(
        reverse=True,
        key=final_score
    )
    selected=fresh[0]
    selected_cta=selected["cta"]
    selected_score=selected["score"]
    selected_archetype=selected.get("archetype","unknown")
    record_cta_usage(
        history,
        selected_cta,
        selected_score,
        selected_archetype,
        topic
    )
    print("="*60)
    print("SELECTED CTA")
    print("="*60)
    print(f"Score: {selected_score:.1f}/100")
    print("Archetype:",selected_archetype)
    print("CTA:",selected_cta)
    print("Cooldown:",f"{CTA_COOLDOWN} videos")
    print("Blocked:",len(blocked))
    print("="*60)
    return selected_cta
