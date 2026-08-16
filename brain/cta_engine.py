from brain.ai_router import ask_ai
import json,os,re,time
from difflib import SequenceMatcher

HISTORY_FILE="data/cta_history.json"
CTA_COOLDOWN=10
MAX_HISTORY=200
SIMILARITY_THRESHOLD=0.78
PATTERN_THRESHOLD=0.88

FORBIDDEN_BIO_PATTERNS=[
    "link in my bio","link in bio","click my bio","click the link",
    "click link","check my bio","check the link in my bio",
    "visit my bio","visit the link","open the link in my bio",
    "use the link in my bio","bio link","my bio link"
]

SYSTEM_PROMPT="""
You are the PromptProHub ELITE CTA ENGINE.

Your ONLY job is to create high-converting spoken CTAs for short-form videos distributed across TikTok, Instagram Reels, YouTube Shorts and LinkedIn.

PromptProHub sells practical AI prompts, prompt templates, AI guides and digital resources for creators, freelancers, business owners, marketers and AI users.

CRITICAL CTA CAMPAIGN:
The current campaign uses COMMENT-TO-RECEIVE.

The TikTok bio link is NOT clickable.

ABSOLUTE RULE:
NEVER tell viewers to click, check, visit, open, use, access or follow any link in a bio.

NEVER mention:
"click the link in my bio"
"link in my bio"
"click link"
"link in bio"
"check my bio"
"visit my bio"
"bio link"
or ANY variation of a bio-link CTA.

The old bio-link strategy is permanently disabled.

The PRIMARY CTA ACTION is commenting the keyword:
"PROMPT"

The campaign resource is the PromptProHub AI prompt guide/library containing 1,000 AI prompts.

Every CTA MUST naturally contain the word PROMPT.

However, DO NOT make every CTA identical.

Examples:
"Comment PROMPT and I'll send you the full 1,000 AI prompts."
"Want the full prompt library? Drop PROMPT in the comments."
"Need the complete AI prompt guide? Type PROMPT below."
"Looking for more prompts like these? Comment PROMPT."
"Drop PROMPT in the comments and I'll show you the full collection."
"Want access to more ready-to-use prompts? Leave PROMPT below."
"If you want the complete prompt resource, comment PROMPT."
"Need more AI prompts like this? Just type PROMPT."

These are examples ONLY. Do not repeatedly copy them.

VARIATION:
The campaign action remains consistent, but the spoken wording must change naturally.

Do NOT make every CTA:
"Comment PROMPT and I'll send you the full 1,000 AI prompts."

Do NOT make every CTA begin with:
"Comment PROMPT".

Rotate openings such as:
"Want the full..."
"Need more..."
"If you want..."
"Looking for..."
"Drop..."
"Type..."
"Just leave..."
"Interested in..."
"The full..."
"Want access to..."
"Need the complete..."
"Trying to..."
"Want more..."
"Looking for more..."

Vary resource wording:
"1,000 AI prompts"
"full AI prompt guide"
"complete prompt library"
"AI prompt collection"
"full prompt pack"
"PromptProHub prompt guide"
"complete AI prompt resource"
"full collection of prompts"
"AI workflow prompt library"
"ready-to-use AI prompts"

Do NOT mention "1,000" in every CTA.

Do NOT mention "AI prompt guide" in every CTA.

Do NOT mention "full prompt library" in every CTA.

Do NOT mention "I'll send you" in every CTA.

The overall campaign should feel consistent without sounding robotic.

DELIVERY RULE:
Do not falsely claim an automatic message is triggered unless the delivery system actually supports it.

Use "I'll send you" only when appropriate to the actual delivery process.

CTA PSYCHOLOGY:
Rotate direct offer, benefit, curiosity, problem-solution, resource, toolkit, productivity, time-saving, discovery, challenge, identity, authority, future pacing, soft sell, full version, prompt library, AI guide, build faster, work smarter and next step.

Do not use the same archetype repeatedly.

CTA STYLE:
Short, spoken, natural, confident, human and conversational.

Target 8-25 spoken words.

Avoid robotic wording.

NEVER use:
"Dear viewer"
"Please kindly"
"Act now"
"Don't miss this incredible opportunity"
"Thanks for watching"
"Click the link in my bio"
"Link in my bio"
"Check my bio"

The CTA must match the current video topic.

If the video demonstrates a prompt, emphasize getting more prompts.

If the video demonstrates an AI workflow, emphasize the complete prompt resource.

If the video is about productivity, connect the prompt resource to saving time or working smarter.

If the video is about business, connect the resource to practical AI use without guaranteeing results.

FOLLOW RULE:
A follow request may sometimes be included, but DO NOT force "follow for more" into every CTA.

Some CTAs should focus entirely on comments.

Some can naturally combine comment + follow.

Never make the CTA overloaded.

DIVERSITY:
Generate exactly 15 CTAs.

Vary:
opening
sentence structure
CTA placement
resource wording
emotional tone
psychological trigger
sentence length
position of PROMPT
whether follow is included
whether the 1,000 number is mentioned

Every CTA MUST contain PROMPT.

Every CTA MUST be a comment-based CTA.

Every CTA MUST NOT contain any bio-link language.

Return ONLY valid JSON.

Format:
{"ctas":[{"cta":"Want the full prompt library? Drop PROMPT in the comments.","archetype":"direct_offer","conversion_potential":94,"relevance":96,"clarity":95,"curiosity":88,"urgency":80,"natural_sounding":97,"novelty":91,"credibility":99}]}
"""

def ensure_history_directory():
    directory=os.path.dirname(HISTORY_FILE)
    if directory:
        os.makedirs(directory,exist_ok=True)

def load_cta_history():
    ensure_history_directory()
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE,"r",encoding="utf-8") as file:
            data=json.load(file)
        return data if isinstance(data,list) else []
    except Exception as e:
        print("CTA HISTORY LOAD ERROR:",e)
        return []

def save_cta_history(history):
    ensure_history_directory()
    try:
        with open(HISTORY_FILE,"w",encoding="utf-8") as file:
            json.dump(history[-MAX_HISTORY:],file,indent=2,ensure_ascii=False)
    except Exception as e:
        print("CTA HISTORY SAVE ERROR:",e)

def normalize_text(text):
    text=str(text or "").lower()
    text=re.sub(r"[^a-z0-9\s]"," ",text)
    return re.sub(r"\s+"," ",text).strip()

def similarity_score(first,second):
    first=normalize_text(first)
    second=normalize_text(second)
    if not first or not second:
        return 0.0
    return SequenceMatcher(None,first,second).ratio()

def contains_forbidden_bio_cta(cta):
    text=normalize_text(cta)
    return any(pattern in text for pattern in FORBIDDEN_BIO_PATTERNS)

def contains_campaign_keyword(cta):
    return bool(re.search(r"\bPROMPT\b",str(cta or ""),re.IGNORECASE))

def is_valid_cta(cta):
    if not cta:
        return False
    if contains_forbidden_bio_cta(cta):
        return False
    if not contains_campaign_keyword(cta):
        return False
    return True

def get_cta_pattern(cta):
    words=normalize_text(cta).split()
    return " ".join(words[:5]) if words else ""

def get_recent_ctas(history):
    return [item.get("cta","") for item in history[-CTA_COOLDOWN:] if isinstance(item,dict) and item.get("cta")]

def get_recent_archetypes(history):
    return {str(item.get("archetype","")).lower() for item in history[-8:] if isinstance(item,dict) and item.get("archetype")}

def is_recent_duplicate(cta,recent_ctas):
    for old_cta in recent_ctas:
        if normalize_text(cta)==normalize_text(old_cta):
            return True
        if similarity_score(cta,old_cta)>=SIMILARITY_THRESHOLD:
            return True
    return False

def same_cta_pattern(first,second):
    first_words=normalize_text(first).split()
    second_words=normalize_text(second).split()
    if len(first_words)<3 or len(second_words)<3:
        return False
    first_prefix=" ".join(first_words[:4])
    second_prefix=" ".join(second_words[:4])
    if first_prefix==second_prefix:
        return True
    return similarity_score(" ".join(first_words[:3])," ".join(second_words[:3]))>=PATTERN_THRESHOLD

def has_recent_pattern_repeat(cta,recent_ctas):
    return any(same_cta_pattern(cta,old_cta) for old_cta in recent_ctas)

def record_cta_usage(history,cta,score,archetype,topic):
    history.append({"cta":cta,"score":round(float(score),2),"archetype":archetype,"pattern":get_cta_pattern(cta),"topic":topic,"timestamp":time.time()})
    save_cta_history(history)

def fallback_ctas():
    return [
        {"score":95,"cta":"Want the full prompt library? Drop PROMPT in the comments.","archetype":"prompt_library"},
        {"score":94,"cta":"Need more AI prompts like these? Type PROMPT below.","archetype":"resource"},
        {"score":93,"cta":"Comment PROMPT if you want the complete AI prompt guide.","archetype":"full_version"},
        {"score":92,"cta":"Looking for more ready-to-use prompts? Leave PROMPT in the comments.","archetype":"toolkit"},
        {"score":91,"cta":"Want the complete collection? Just comment PROMPT.","archetype":"direct_offer"},
        {"score":90,"cta":"If you want more practical AI prompts, drop PROMPT below.","archetype":"benefit"},
        {"score":89,"cta":"Need the full AI prompt resource? Comment PROMPT.","archetype":"resource"},
        {"score":88,"cta":"Want to build faster with AI? Type PROMPT in the comments.","archetype":"productivity"},
        {"score":87,"cta":"If this prompt helped, comment PROMPT for more like it.","archetype":"curiosity"},
        {"score":86,"cta":"Want access to the full prompt collection? Drop PROMPT below.","archetype":"access"}
    ]

def generate_cta(topic):
    history=load_cta_history()
    recent_ctas=get_recent_ctas(history)
    recent_text="\n".join(f"- {cta}" for cta in recent_ctas[-10:])
    prompt=f"""
{SYSTEM_PROMPT}

CURRENT VIDEO TOPIC:
{topic}

RECENTLY USED CTAs:
{recent_text}

FINAL RULES:
Generate exactly 15 genuinely different CTAs for this topic.
EVERY CTA MUST contain the word PROMPT.
EVERY CTA MUST use the comment-based strategy.
EVERY CTA MUST NOT contain any bio-link wording.
NEVER mention a link in a bio.
Do not make every CTA mention 1,000 prompts.
Do not make every CTA mention the full prompt guide.
Do not make every CTA say "I'll send you."
Do not make every CTA include a follow request.
Keep the campaign consistent but conversational.
Return ONLY valid JSON.
"""
    try:
        response=ask_ai(prompt)
        response=response.replace("```json","").replace("```","").strip()
        data=json.loads(response)
        ideas=data.get("ctas",[])
        if not ideas:
            raise Exception("AI returned no CTAs")
        cleaned=[]
        for item in ideas:
            if not isinstance(item,dict):
                continue
            cta=str(item.get("cta","")).strip()
            if not is_valid_cta(cta):
                print("CTA BLOCKED:",cta)
                continue
            try:
                scores={
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
            weighted_score=scores["conversion"]*0.24+scores["relevance"]*0.16+scores["clarity"]*0.13+scores["curiosity"]*0.10+scores["urgency"]*0.08+scores["natural"]*0.11+scores["novelty"]*0.10+scores["credibility"]*0.08
            archetype=str(item.get("archetype","unknown")).strip().lower()
            cleaned.append({"score":weighted_score,"cta":cta,"archetype":archetype})
        if not cleaned:
            raise Exception("No valid comment CTAs remained after filtering.")
        cleaned.sort(reverse=True,key=lambda item:item["score"])
        print("="*60)
        print("PROMPTPROHUB COMMENT CTA ENGINE")
        print("="*60)
        print(f"Generated: {len(cleaned)}")
        print(f"Recent CTAs: {len(recent_ctas)}")
        print("BIO-LINK CTA: DISABLED")
        print("COMMENT KEYWORD: PROMPT")
        print("="*60)
        return cleaned
    except Exception as e:
        print("="*60)
        print("CTA ENGINE FAILED")
        print("="*60)
        print(type(e).__name__)
        print(str(e))
        print("="*60)
        return fallback_ctas()

def choose_cta(topic):
    candidates=generate_cta(topic)
    history=load_cta_history()
    recent_ctas=get_recent_ctas(history)
    recent_archetypes=get_recent_archetypes(history)
    fresh=[]
    blocked=[]
    for item in candidates:
        cta=item["cta"]
        if not is_valid_cta(cta):
            blocked.append((cta,"invalid_campaign"))
            continue
        if is_recent_duplicate(cta,recent_ctas):
            blocked.append((cta,"duplicate"))
            continue
        if has_recent_pattern_repeat(cta,recent_ctas):
            blocked.append((cta,"pattern"))
            continue
        fresh.append(item)
    if not fresh:
        fresh=[item for item in fallback_ctas() if is_valid_cta(item["cta"]) and not is_recent_duplicate(item["cta"],recent_ctas)]
    if not fresh:
        fresh=fallback_ctas()
    def final_score(item):
        bonus=4 if item.get("archetype","") not in recent_archetypes else 0
        return item["score"]+bonus
    fresh.sort(reverse=True,key=final_score)
    selected=fresh[0]
    selected_cta=selected["cta"]
    selected_score=selected["score"]
    selected_archetype=selected.get("archetype","unknown")
    record_cta_usage(history,selected_cta,selected_score,selected_archetype,topic)
    print("="*60)
    print("SELECTED CTA")
    print("="*60)
    print(f"Score: {selected_score:.1f}/100")
    print("Archetype:",selected_archetype)
    print("CTA:",selected_cta)
    print("Campaign: COMMENT PROMPT")
    print("Bio-link CTA: PERMANENTLY DISABLED")
    print("Cooldown:",f"{CTA_COOLDOWN} videos")
    print("Blocked:",len(blocked))
    print("="*60)
    return selected_cta
