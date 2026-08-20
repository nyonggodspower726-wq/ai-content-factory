from brain.ai_router import ask_ai
FORBIDDEN=["click the link in my bio","link in my bio","click link","link in bio","check my bio","visit my bio","bio link","my bio link"]
def bad_cta(x):
    x=str(x or "").lower()
    return any(p in x for p in FORBIDDEN)
def generate_script(project,selected_cta=None):
    topic=project.get("topic","")
    product=project.get("product",{})
    angle=project.get("marketing",{})
    if selected_cta:
        final_cta=str(selected_cta).strip()
    else:
        final_cta="Comment PROMPT and I'll send you the full AI prompt guide."
    if bad_cta(final_cta) or "prompt" not in final_cta.lower():
        final_cta="Comment PROMPT and I'll send you the full AI prompt guide."
    prompt=f"""You are PromptProHub's professional short-form video scriptwriter.
Create ONE highly engaging 30-45 second spoken script for TikTok, YouTube Shorts, Instagram Reels and Facebook Reels.
TOPIC:
{topic}
PRODUCT:
{product}
MARKETING:
{angle}
CTA:
{final_cta}
IMPORTANT CTA RULES:
The final spoken words MUST be exactly the CTA above.
Never change the CTA.
Never add anything after it.
Never mention a bio link.
Never say click the link in my bio.
Never say link in bio.
Never say click link.
Never say check my bio.
Never say visit my bio.
The CTA must be comment-based and contain PROMPT.
STRUCTURE:
1. HARD HOOK
2. PROBLEM
3. DISCOVERY
4. PRACTICAL SOLUTION
5. BENEFIT
6. CTA
Start immediately with a specific curiosity-driven hook.
Never start with What if, Imagine, Have you ever, Did you know, Today, In this video, Welcome or Let's talk about.
Use simple conversational English.
Target 75-95 spoken words.
No emojis.
No hashtags.
No stage directions.
No titles.
No bullet points.
No quotation marks.
Do not invent income, customers, achievements or guaranteed results.
Output ONLY the spoken script."""
    try:
        script=ask_ai(prompt)
        if not script:
            raise Exception("AI returned empty script")
        script=str(script).replace("```","").strip()
        for phrase in ["Click the link in my bio","click the link in my bio","Link in my bio","link in bio","Click link","Check my bio","Visit my bio","Bio link"]:
            script=script.replace(phrase,"").strip()
        pos=script.lower().find(final_cta.lower())
        if pos>=0:
            script=script[:pos].rstrip()+" "+final_cta
        else:
            script=script.rstrip()+" "+final_cta
        if bad_cta(script):
            raise Exception("Forbidden bio-link CTA detected")
        print("="*60)
        print("SCRIPT ENGINE")
        print("="*60)
        print("Topic:",topic)
        print("CTA:",final_cta)
        print("BIO-LINK CTA: BLOCKED")
        print("="*60)
        return script
    except Exception as e:
        print("="*60)
        print("SCRIPT ENGINE FAILED")
        print(type(e).__name__,e)
        print("="*60)
        return f"You're probably using {topic} the hard way. Here's a practical AI workflow that can help reduce repetitive work and make the process easier. Instead of doing everything manually, use the right prompts to speed up the repetitive parts. {final_cta}"
