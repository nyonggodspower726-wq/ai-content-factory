from brain.ai_router import ask_ai
import json,os,re,time
from difflib import SequenceMatcher

HISTORY_FILE="data/cta_history.json"
CTA_COOLDOWN=10
MAX_HISTORY=200
SIMILARITY_THRESHOLD=0.78
PATTERN_THRESHOLD=0.88

SYSTEM_PROMPT="""
You are the PromptProHub ELITE CTA ENGINE.

Your ONLY job is to create high-converting spoken CTAs for short-form videos distributed across TikTok, Instagram Reels, YouTube Shorts and LinkedIn.

PromptProHub sells practical AI prompts, prompt templates, AI guides and digital resources for creators, freelancers, business owners, marketers and AI users.

IMPORTANT CURRENT CTA STRATEGY:
The TikTok bio link is currently NOT clickable. Therefore DO NOT tell viewers to click, check, visit, open, or use the link in the bio.

The primary CTA strategy is COMMENT-TO-RECEIVE.

The viewer should be encouraged to comment a simple keyword such as:
"PROMPT"

The promised resource is the PromptProHub AI prompt guide/library containing 1,000 AI prompts.

However, NEVER make every CTA sound identical.

The CTA should naturally communicate that commenting "PROMPT" can get the viewer the relevant AI prompt resource, guide, collection, or full prompt library.

Examples of acceptable styles:
"Comment PROMPT and I'll send you the full 1,000 AI prompts."
"Want the full prompt library? Drop PROMPT in the comments."
"Comment PROMPT if you want the complete AI prompt guide."
"If you want the full collection, just comment PROMPT below."
"Drop the word PROMPT and I'll send you the AI prompt guide."
"Need the full list? Comment PROMPT and I'll send it over."
"Want more prompts like these? Type PROMPT in the comments."
"Comment PROMPT and I'll show you where to get the complete prompt collection."

These are examples ONLY. Do not copy them repeatedly.

VARIATION IS EXTREMELY IMPORTANT.

Do NOT make every video say:
"Comment PROMPT and I'll send you the full 1,000 AI prompts."

Do NOT make every CTA begin with:
"Comment PROMPT..."

Sometimes start with:
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
"Trying to build..."
"Save this..."
"Follow..."

But the CTA must still make the comment action clear.

The keyword should normally remain "PROMPT" because it is the campaign keyword.

The CTA can vary the RESOURCE wording:
"1,000 AI prompts"
"full AI prompt guide"
"complete prompt library"
"AI prompt collection"
"full prompt pack"
"PromptProHub prompt guide"
"complete AI prompt resource"
"full collection of prompts"
"AI workflow prompt library"

Do not falsely claim that a comment automatically triggers an automated message unless the system actually supports that functionality.

Use language such as:
"I'll send you..."
"I'll show you how to get..."
"Comment PROMPT for the full..."
only when appropriate to the actual delivery system.

Do not invent earnings, customers, sales, guaranteed results, fake scarcity, fake deadlines or fake testimonials.

CTA PSYCHOLOGY:
Rotate across direct offer, benefit, curiosity, problem-solution, resource, toolkit, productivity, time-saving, discovery, challenge, identity, authority, future pacing, soft sell, full version, prompt library, AI guide, build faster, work smarter and next step.

Do not use the same archetype repeatedly.

CTA STYLE:
Short, spoken, natural, confident, human and conversational.

Target 8-25 spoken words.

The CTA must sound like something a real creator would say at the end of a video.

Avoid robotic wording.

Avoid:
"Dear viewer"
"Please kindly"
"Act now"
"Don't miss this incredible opportunity"
"Thanks for watching"
"Click the link in my bio"

The CTA should match the current video topic.

If the video demonstrates a prompt, emphasize getting more prompts.

If the video demonstrates an AI workflow, emphasize the complete prompt resource.

If the video is about productivity, connect the prompt library to saving time or working smarter.

If the video is about business, connect the resource to practical AI use without guaranteeing results.

FOLLOW CTA:
A follow request may sometimes be included, but DO NOT force "follow for more" into every CTA.

Some CTAs should focus entirely on comments.

Some can naturally combine:
comment + follow
follow + comment
comment + benefit

Never make the CTA feel overloaded.

DIVERSITY:
Generate exactly 15 CTAs.

The 15 CTAs must be genuinely different.

Vary:
- opening
- sentence structure
- CTA placement
- resource wording
- emotional tone
- psychological trigger
- sentence length
- position of "PROMPT"
- whether follow is included
- whether the 1,000 number is mentioned

IMPORTANT:
Do NOT mention "1,000" in every CTA.

Do NOT mention "AI prompt guide" in every CTA.

Do NOT mention "full prompt library" in every CTA.

Do NOT mention "I'll send you" in every CTA.

The overall campaign should feel consistent but not repetitive.

Return ONLY valid JSON.

Format:
{
  "ctas":[
    {
      "cta":"Want the full prompt library? Drop PROMPT in the comments.",
      "archetype":"direct_offer",
      "conversion_potential":94,
      "relevance":96,
      "clarity":95,
      "curiosity":88,
      "urgency":80,
      "natural_sounding":97,
      "novelty":91,
      "credibility":99
    }
  ]
}
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
        print("="*60)
        print("CTA HISTORY LOAD ERROR")
        print("="*60)
        print(e)
        return []

def save_cta_history(history):
    ensure_history_directory()
    try:
        with open(HISTORY_FILE,"w",encoding="utf-8") as file:
            json.dump(history[-MAX_HISTORY:],file,indent=2,ensure_ascii=False)
    except Exception as e:
        print("="*60)
        print("CTA HISTORY SAVE ERROR")
        print("="*60)
        print(e)

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
    history.append({
        "cta":cta,
        "score":round(float(score),2),
        "archetype":archetype,
        "pattern":get_cta_pattern(cta),
        "topic":topic,
        "timestamp":time.time()
    })
    save_cta_history(history)

def generate_cta(topic):
    history=load_cta_history()
    recent_ctas=get_recent_ctas(history)
    recent_text="\n".join(f"- {cta}" for cta in recent_ctas[-10:])
    prompt=f"""
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

Every CTA must support the COMMENT "PROMPT" strategy, but do not make every CTA use identical wording.

Keep the campaign keyword consistent while making the spoken language naturally different.

Do not make every CTA mention 1,000 prompts.

Do not make every CTA mention the full prompt guide.

Do not make every CTA say "I'll send you."

Do not make every CTA include a follow request.

Do not use the old bio-link strategy.

Keep every CTA natural for AI voice narration.

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
            if not cta:
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
            cleaned.append({"score":weighted_score,"cta":cta,"archetype":archetype})
        if not cleaned:
            raise Exception("No valid CTAs remained after parsing.")
        cleaned.sort(reverse=True,key=lambda item:item["score"])
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
            {"score":95,"cta":"Want the full prompt library? Drop PROMPT in the comments.","archetype":"prompt_library"},
            {"score":94,"cta":"Comment PROMPT if you want the complete AI prompt guide.","archetype":"resource"},
            {"score":93,"cta":"Need more prompts like these? Type PROMPT below.","archetype":"curiosity"},
            {"score":92,"cta":"Drop PROMPT and I'll send you the full collection of AI prompts.","archetype":"direct_offer"},
            {"score":91,"cta":"If you want the 1,000-prompt AI guide, comment PROMPT.","archetype":"full_version"},
            {"score":90,"cta":"The full AI prompt resource is waiting for you. Just comment PROMPT.","archetype":"resource"},
            {"score":89,"cta":"Want to build faster with AI? Leave PROMPT in the comments.","archetype":"productivity"},
            {"score":88,"cta":"Comment PROMPT and get access to more ready-to-use AI prompts.","archetype":"toolkit"},
            {"score":87,"cta":"If this prompt helped, type PROMPT and I'll show you the full collection.","archetype":"benefit"},
            {"score":86,"cta":"Looking for more AI shortcuts? Comment PROMPT below.","archetype":"shortcut"}
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
        non_exact=[item for item in candidates if normalize_text(item["cta"]) not in {normalize_text(old) for old in recent_ctas}]
        fresh=non_exact if non_exact else candidates
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
    print("Cooldown:",f"{CTA_COOLDOWN} videos")
    print("Blocked:",len(blocked))
    print("="*60)
    return selected_cta
