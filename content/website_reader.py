# content/website_reader.py

import requests
from bs4 import BeautifulSoup
from config import WEBSITE_URL


def get_website_content():
    """
    Reads your website homepage and returns the text.
    """

    try:
        response = requests.get(WEBSITE_URL, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts and styles
        for tag in soup(["script", "style"]):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)

        return text

    except Exception as e:
        print(f"Website Error: {e}")
        return ""
