from brain.ai_router import ask_ai
import json,os,re,time
from difflib import SequenceMatcher

HISTORY_FILE="data/cta_history.json"
CTA_COOLDOWN=10
MAX_HISTORY=200
SIMILARITY_THRESHOLD=0.78
PATTERN_THRESHOLD=0.88

FORBIDDEN_BIO_PATTERNS=[
"link in my bio","link in bio","click my bio","click the link","click link",
"check my bio","check the link","visit my bio","visit the link","open my bio",
"open the link","use my bio","use the link","access my bio","access the link",
"bio link","my bio link","link from my bio","link through my bio","link via my bio",
"tap my bio","tap the link","go to my bio","go through my bio","website in my bio",
"website link","bio website"
]

FORBIDDEN_BIO_REGEX=[
r"\b(click|tap|check|visit|open|use|access|go\s+to|go\s+through)\b.{0,35}\b(bio|link)\b",
r"\b(bio|profile)\b.{0,35}\b(link|website|url)\b",
r"\b(link|website|url)\b.{0,35}\b(bio|profile)\b"
]

SYSTEM_PROMPT="""
You are the PromptProHub ELITE COMMENT CTA ENGINE.

Your ONLY job is to create high-converting spoken CTAs for short-form videos.

PromptProHub sells practical AI prompts, prompt templates, AI guides and digital resources for creators, freelancers, business owners, marketers and AI users.

CRITICAL CAMPAIGN:
The current campaign is COMMENT-TO-RECEIVE.

The TikTok bio link is NOT clickable.

ABSOLUTE PERMANENT RULE:
NEVER tell viewers to click, tap, check, visit, open, use, access or follow ANY link, website or URL in a bio or profile.

NEVER mention:
"click the link in my bio"
"link in my bio"
"click link"
"link in bio"
"check my bio"
"visit my bio"
"bio link"
"my bio link"
or ANY similar bio-link CTA.

The old bio-link strategy is permanently disabled.

DO NOT generate ANY bio-link CTA under ANY circumstance.

PRIMARY ACTION:
The viewer should comment the keyword:
"PROMPT"

Every CTA MUST contain the word PROMPT.

The campaign resource is the PromptProHub AI prompt guide/library containing 1,000 AI prompts.

IMPORTANT:
Every CTA must be comment-based.
Every CTA must contain PROMPT.
Every CTA must avoid all bio-link language.
Every CTA should sound natural and different.

DO NOT repeat:
"Comment PROMPT and I'll send you the full 1,000 AI prompts."

Do NOT make every CTA begin with "Comment PROMPT".

Vary openings:
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

Do NOT mention 1,000 in every CTA.
Do NOT mention the full prompt guide in every CTA.
Do NOT say "I'll send you" in every CTA.
Do NOT include a follow request in every CTA.

Some CTAs should focus only on comments.
Some may naturally combine comment + follow.
Never overload the CTA.

Match the CTA to the video topic.

If the video demonstrates a prompt, emphasize more prompts.
If the video demonstrates an AI workflow, emphasize the complete prompt resource.
If the video is about productivity, connect the resource to saving time or working smarter.
If the video is about business, connect it to practical AI use without guaranteeing results.

Never invent earnings, customers, sales, guarantees, fake scarcity, fake deadlines or fake testimonials.

DELIVERY RULE:
Do not falsely claim that commenting automatically triggers a message unless the delivery system actually supports it.

CTA STYLE:
Short, spoken, natural, confident, human and conversational.
Target 8-25 spoken words.

NEVER use:
"Dear viewer"
"Please kindly"
"Act now"
"Don't miss this incredible opportunity"
"Thanks for watching"
"Click the link in my bio"
"Link in my bio"
"Check my bio"
"Bio link"

DIVERSITY:
Generate exactly 15 genuinely different CTAs.

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
whether 1,000 is mentioned

EVERY CTA MUST:
1. Contain PROMPT.
2. Be comment-based.
3. NOT contain bio-link language.
4. Sound natural when spoken.
5. Match the video topic.

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
    if any(pattern in text for pattern in FORBIDDEN_BIO_PATTERNS):
        return True
    return any(re.search(pattern,text,re.IGNORECASE) for pattern in FORBIDDEN_BIO_REGEX)

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
        {"score":93,"cta":"Want the complete AI prompt guide? Comment PROMPT.","archetype":"full_version"},
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

FINAL GENERATION RULES:
Generate exactly 15 genuinely different CTAs.

EVERY CTA MUST contain PROMPT.
EVERY CTA MUST be comment-based.
EVERY CTA MUST NOT contain bio-link language.
NEVER mention a link, website or URL in a bio or profile.
NEVER generate "click the link in my bio" or any variation.
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
        print("BIO-LINK CTA: PERMANENTLY DISABLED")
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
    print("Campaign: COMMENT PROMPT")
    print("Bio-link CTA: PERMANENTLY DISABLED")
    print("Cooldown:",f"{CTA_COOLDOWN} videos")
    print("Blocked:",len(blocked))
    print("="*60)
    return selected_cta
